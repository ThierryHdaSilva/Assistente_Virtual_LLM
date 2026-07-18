import argparse
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data"
CACHE_DIR = PROJECT_DIR / "cache"
CHROMA_PATH = CACHE_DIR / "chroma_db"
COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "base_conhecimento_v2")
HISTORICAL_EVENTS_DIR = Path(
    os.getenv("HISTORICAL_EVENTS_DIR", str(DATA_DIR / "base_historica"))
)


def load_json(path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_jsonl(path):
    with path.open("r", encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_file_root(outputs_dir, paths):
    lines = []
    for path in sorted(paths, key=lambda item: item.as_posix()):
        relative_path = path.relative_to(outputs_dir).as_posix()
        lines.append(f"{relative_path}\t{sha256_file(path)}\n")
    return hashlib.sha256("".join(lines).encode("utf-8")).hexdigest()


def slugify(value):
    value = re.sub(r"[^a-z0-9]+", "-", value.lower())
    return value.strip("-") or "sem-termo"


def text_from_value(value):
    if value is None:
        return ""
    if isinstance(value, list):
        return "; ".join(str(item) for item in value if item)
    return str(value)


def build_glossary_document(item):
    sections = [
        ("Definicao", item.get("definicao")),
        ("Explicacao simples", item.get("explicacao_simples")),
        ("Explicacao tecnica", item.get("explicacao_tecnica")),
        ("Como funciona", item.get("como_funciona")),
        ("Objetivo", item.get("objetivo")),
        ("Aplicacoes", item.get("aplicacoes")),
        ("Riscos", item.get("riscos")),
        ("Exemplo pratico", item.get("exemplo_pratico")),
    ]
    body = [
        "Base: glossario financeiro offline.",
        f"Termo: {item.get('termo', 'Sem termo')}.",
        f"Capitulo: {item.get('capitulo_nome', 'Nao informado')}.",
    ]
    body.extend(f"{label}: {text_from_value(value)}" for label, value in sections if value)
    return "\n".join(body)


def load_glossary_documents():
    glossary = load_json(DATA_DIR / "glossario_financeiro.json")
    entries = glossary.get("verbetes", []) if isinstance(glossary, dict) else glossary
    if not isinstance(entries, list) or not entries:
        raise ValueError("O arquivo do glossario nao possui uma lista valida em 'verbetes'.")

    documents, metadatas, ids = [], [], []
    for position, item in enumerate(entries, start=1):
        if not isinstance(item, dict) or not item.get("termo"):
            raise ValueError(f"Verbete invalido na posicao {position} do glossario.")
        documents.append(build_glossary_document(item))
        metadatas.append(
            {
                "tipo": "glossario",
                "categoria": "glossario",
                "termo": item["termo"],
                "capitulo": item.get("capitulo_nome", "Nao informado"),
            }
        )
        ids.append(f"glossario-{position:04d}-{slugify(item['termo'])}")
    return documents, metadatas, ids


def load_sources(outputs_dir, batch_count):
    source_paths = [
        outputs_dir / "database" / "sources" / "batches" / f"sources_p0_batch_{number:03d}.jsonl"
        for number in range(1, batch_count + 1)
    ]
    base_registry = outputs_dir / "database" / "sources" / "sources.jsonl"
    missing_paths = [path for path in [*source_paths, base_registry] if not path.exists()]
    if missing_paths:
        raise ValueError(f"Arquivos de fontes ausentes: {', '.join(map(str, missing_paths))}")

    source_records = {}
    for path in [*source_paths, base_registry]:
        for source in load_jsonl(path):
            source_id = source.get("source_id")
            if source_id:
                source_records[source_id] = source
    return source_records, source_paths, base_registry


def load_canonical_p0_events(historical_events_dir):
    outputs_dir = historical_events_dir / "outputs"
    freeze_path = outputs_dir / "indexes" / "p0_canonical_frozen_manifest.json"
    if not freeze_path.exists():
        raise ValueError(f"Manifesto P0 congelado nao encontrado: {freeze_path}")

    freeze = load_json(freeze_path)
    if freeze.get("certification_status") != "certificado":
        raise ValueError("O manifesto P0 nao esta certificado para uso downstream.")
    if not freeze.get("validation", {}).get("ready_for_downstream_use"):
        raise ValueError("O manifesto P0 nao autoriza uso downstream.")

    chain = freeze["numbered_chain"]
    reconstruction = freeze["canonical_reconstruction"]
    repair = freeze["repair_overlay"]
    batch_count = chain["batch_count"]
    event_paths = [
        outputs_dir / "database" / "events" / "batches" / f"p0_batch_{number:03d}.jsonl"
        for number in range(1, batch_count + 1)
    ]
    missing_paths = [path for path in event_paths if not path.exists()]
    if missing_paths:
        raise ValueError(f"Lotes de eventos ausentes: {', '.join(map(str, missing_paths))}")

    frozen_hashes = freeze.get("frozen_hashes", {})
    expected_event_root_hash = frozen_hashes.get("numbered_event_files_root_sha256")
    if expected_event_root_hash and sha256_file_root(outputs_dir, event_paths) != expected_event_root_hash:
        raise ValueError("Os lotes de eventos P0 divergem do hash registrado no freeze.")

    events = []
    for path in event_paths:
        events.extend(load_jsonl(path))

    repair_path = outputs_dir / repair["event_file"].removeprefix("outputs/")
    if not repair_path.exists():
        raise ValueError(f"Overlay de reparo nao encontrado: {repair_path}")
    expected_repair_hash = frozen_hashes.get("repair_event_file_sha256")
    if expected_repair_hash and sha256_file(repair_path) != expected_repair_hash:
        raise ValueError("O overlay de reparo diverge do hash registrado no freeze.")
    repair_records = load_jsonl(repair_path)
    if len(repair_records) != 1 or repair_records[0].get("event_id") != repair["event_id"]:
        raise ValueError("O overlay de reparo nao corresponde ao manifesto congelado.")

    event_ids = [event.get("event_id") for event in events]
    if len(event_ids) != len(set(event_ids)):
        raise ValueError("Foram encontrados IDs duplicados nos lotes P0.")
    after_id = repair["insert_after_event_id"]
    before_id = repair["insert_before_event_id"]
    try:
        insert_at = event_ids.index(after_id) + 1
    except ValueError as error:
        raise ValueError("A ancora anterior do reparo nao foi encontrada.") from error
    if insert_at >= len(event_ids) or event_ids[insert_at] != before_id:
        raise ValueError("As ancoras do reparo nao estao consecutivas na cadeia P0.")

    events[insert_at:insert_at] = repair_records
    canonical_ids = [event["event_id"] for event in events]
    if len(events) != reconstruction["event_count"] or len(canonical_ids) != len(set(canonical_ids)):
        raise ValueError("A reconstrucao P0 nao possui a contagem ou unicidade esperada.")
    canonical_hash = hashlib.sha256(
        "".join(f"{event_id}\n" for event_id in canonical_ids).encode("utf-8")
    ).hexdigest()
    if canonical_hash != reconstruction["event_ids_sha256"]:
        raise ValueError("A ordem canonica de IDs P0 diverge do manifesto congelado.")

    sources, source_paths, base_registry = load_sources(outputs_dir, batch_count)
    expected_source_root_hash = frozen_hashes.get("numbered_source_files_root_sha256")
    if expected_source_root_hash and sha256_file_root(outputs_dir, source_paths) != expected_source_root_hash:
        raise ValueError("Os lotes de fontes P0 divergem do hash registrado no freeze.")
    expected_registry_hash = frozen_hashes.get("base_source_registry_sha256")
    if expected_registry_hash and sha256_file(base_registry) != expected_registry_hash:
        raise ValueError("O registro-base de fontes diverge do hash registrado no freeze.")
    return events, sources, freeze


def format_source(source):
    publisher = source.get("publisher") or "Fonte institucional"
    title = source.get("title") or "Documento sem titulo"
    url = source.get("url")
    return f"{publisher} - {title}" + (f". URL: {url}" if url else "")


def build_event_document(event, source_records):
    claims = [claim.get("text") for claim in event.get("claims", []) if claim.get("text")]
    claim_source_ids = []
    for claim in event.get("claims", []):
        claim_source_ids.extend(claim.get("source_ids", []))
    claim_source_ids = list(dict.fromkeys(claim_source_ids))
    sources = [format_source(source_records[source_id]) for source_id in claim_source_ids if source_id in source_records]

    time_info = event.get("time", {})
    period = " a ".join(part for part in [time_info.get("start_local"), time_info.get("end_local")] if part)
    rag = event.get("rag", {})
    limits = text_from_value(rag.get("do_not_answer_without_live_data"))
    body = [
        "Base: evento historico P0 offline.",
        f"Evento: {event.get('canonical_name_pt', 'Sem nome')}.",
        f"ID: {event.get('event_id', 'Nao informado')}.",
        f"Status do registro: {event.get('record_status', 'Nao informado')}.",
        f"Periodo: {period or 'Nao informado'}.",
        f"Categorias: {text_from_value(event.get('categories'))}.",
        "Fatos verificados:",
        *(f"- {claim}" for claim in claims),
        "Fontes dos fatos verificados:",
        *(f"- {source}" for source in sources),
    ]
    if rag.get("summary_250_words"):
        body.append(f"Contexto e limites do registro: {rag['summary_250_words']}")
    if limits:
        body.append(f"Nao responder sem dado atualizado para: {limits}.")
    return "\n".join(body)


def load_event_documents():
    events, sources, freeze = load_canonical_p0_events(HISTORICAL_EVENTS_DIR)
    documents, metadatas, ids = [], [], []
    for event in events:
        event_id = event["event_id"]
        documents.append(build_event_document(event, sources))
        metadatas.append(
            {
                "tipo": "evento_historico_verificado",
                "categoria": "evento_historico",
                "event_id": event_id,
                "evento": event.get("canonical_name_pt", "Sem nome"),
                "prioridade": event.get("priority", "P0"),
                "status": event.get("record_status", "nao informado"),
            }
        )
        ids.append(f"evento-{event_id}")
    return documents, metadatas, ids, freeze


def build_index(validate_only=False):
    glossary_documents, glossary_metadatas, glossary_ids = load_glossary_documents()
    event_documents, event_metadatas, event_ids, freeze = load_event_documents()
    documents = [*glossary_documents, *event_documents]
    metadatas = [*glossary_metadatas, *event_metadatas]
    ids = [*glossary_ids, *event_ids]
    if len(ids) != len(set(ids)):
        raise ValueError("Foram gerados IDs duplicados para o indice.")

    summary = {
        "collection": COLLECTION_NAME,
        "glossary_documents": len(glossary_documents),
        "historical_event_documents": len(event_documents),
        "total_documents": len(documents),
        "p0_freeze_id": freeze["freeze_id"],
        "p0_event_ids_sha256": freeze["canonical_reconstruction"]["event_ids_sha256"],
    }
    if validate_only:
        return summary

    from chromadb import PersistentClient
    from chromadb.errors import NotFoundError
    from sentence_transformers import SentenceTransformer

    print("Carregando modelo de embeddings...")
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    print("Gerando embeddings...")
    embeddings = embedder.encode(documents, show_progress_bar=True).tolist()

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    client = PersistentClient(path=str(CHROMA_PATH))
    try:
        client.delete_collection(name=COLLECTION_NAME)
    except (ValueError, NotFoundError):
        pass
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    collection.add(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas)

    summary["indexed_at"] = datetime.now(timezone.utc).isoformat()
    summary["indexed_documents"] = collection.count()
    (CACHE_DIR / "index_manifest.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return summary


def main():
    parser = argparse.ArgumentParser(description="Constroi o indice RAG offline da Alessandra.")
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    try:
        summary = build_index(validate_only=args.validate_only)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        raise SystemExit(f"Erro ao construir o indice: {error}") from error
    action = "Validacao concluida" if args.validate_only else "Indice criado"
    print(f"{action}: {json.dumps(summary, ensure_ascii=False)}")


if __name__ == "__main__":
    main()
