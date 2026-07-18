import sys
import os
import re
import ollama
import chromadb
from sentence_transformers import SentenceTransformer

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
sys.path.insert(0, os.path.dirname(__file__))

from fetch_cotacoes import get_cotacao, buscar_empresas
from fetch_noticias import get_noticias
from classify_sentiment import classificar
from config import CHROMA_PATH, CHROMA_COLLECTION, MODELO_LLM, MODELO_EMBEDDING, carregar_system_prompt

_embedder = None
_colecao = None


def _get_rag():
    global _embedder, _colecao
    if _embedder is None:
        _embedder = SentenceTransformer(MODELO_EMBEDDING)
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        _colecao = client.get_or_create_collection(name=CHROMA_COLLECTION)
    return _embedder, _colecao


TICKER_REGEX = re.compile(r'\b[A-Z]{4}\d{1,2}\b')


def classificar_pergunta(pergunta):
    if TICKER_REGEX.search(pergunta.upper()):
        return "cotacao"

    palavras_listagem = ["liste", "listar", "quais ações", "qual empresa", "que empresa", "lista de ações", "lista das ações", "todas as ações"]
    if any(p in pergunta.lower() for p in palavras_listagem):
        return "busca_empresa"

    palavras_noticia = ["notícia", "noticia", "aconteceu", "hoje", "recente", "atualidade"]
    if any(p in pergunta.lower() for p in palavras_noticia):
        return "noticia"

    return "educativa"

def buscar_contexto_educativo(pergunta):
    embedder, colecao = _get_rag()
    if colecao.count() == 0:
        return "BASE_CONHECIMENTO_NAO_INDEXADA"

    embedding = embedder.encode([pergunta]).tolist()
    resultado = colecao.query(query_embeddings=embedding, n_results=min(4, colecao.count()))

    if not resultado["documents"][0]:
        return None

    trechos = []
    for doc, meta in zip(resultado["documents"][0], resultado["metadatas"][0]):
        tipo = meta.get("tipo", "sem_tipo")
        if tipo == "evento_historico_verificado":
            rotulo = "evento historico P0"
        elif tipo == "glossario":
            rotulo = "glossario financeiro"
        else:
            rotulo = tipo
        trechos.append(f"[{rotulo}] {doc}")
    return "\n".join(trechos)


def buscar_contexto_cotacao(pergunta):
    tickers = TICKER_REGEX.findall(pergunta.upper())
    tickers = list(dict.fromkeys(tickers))  # remove duplicados, mantém ordem

    if not tickers:
        return None

    linhas = []
    algum_encontrado = False

    for ticker in tickers:
        dado = get_cotacao(ticker)
        if "erro" in dado:
            linhas.append(f"- {ticker}: NÃO ENCONTRADO na base de dados. NÃO invente um valor para este ticker — diga explicitamente que não foi encontrado.")
        else:
            algum_encontrado = True
            aviso = " ⚠️ Dado pode estar desatualizado (mercado possivelmente fechado)." if dado["possivelmente_desatualizado"] else ""
            linhas.append(
                f"- {dado['ticker']}: R$ {dado['preco']} ({dado['variacao_percent']}% no dia). "
                f"Fonte: {dado['fonte']}, horário do dado: {dado['horario_do_dado']}.{aviso} "
                f"Link para o usuário conferir: {dado['url_verificacao']}"
            )

    if not algum_encontrado:
        return "NENHUM_DADO_ENCONTRADO"

    return "\n".join(linhas)

def buscar_contexto_noticia():
    try:
        noticias = get_noticias(limite_por_fonte=3)
    except Exception:
        return "NOTICIAS_INDISPONIVEIS"
    if not noticias:
        return "NOTICIAS_INDISPONIVEIS"

    trechos = []
    for n in noticias[:5]:
        try:
            sentimento = classificar(n["titulo"])
            rotulo_sentimento = sentimento.get("label", "indisponivel")
        except Exception:
            rotulo_sentimento = "indisponivel"

        publicado_em = n.get("publicado_em") or "data nao informada"
        link = n.get("link") or "link nao informado"
        trechos.append(
            f"[{n['fonte']}] {n['titulo']} — Publicado em: {publicado_em}. "
            f"Link: {link}. Sentimento: {rotulo_sentimento}"
        )
    return "\n".join(trechos) if trechos else "NOTICIAS_INDISPONIVEIS"

def buscar_contexto_empresa(pergunta):
    resultados = buscar_empresas(limite=15)
    if not resultados:
        return None

    linhas = [f"- {r['ticker']}: {r['nome']}" for r in resultados]
    return (
        "IMPORTANTE: esta é uma lista PARCIAL e REAL de ações da B3, obtida agora via API. "
        "NÃO invente tickers ou nomes fora desta lista. Se o usuário pedir a lista completa, "
        "explique que esta é uma amostra e sugira consultar o site da B3 (www.b3.com.br) para a lista integral:\n"
        + "\n".join(linhas)
    )


def montar_prompt(pergunta, contexto):
    system_prompt = carregar_system_prompt()

    if contexto:
        mensagem_usuario = f"""Contexto disponível para esta pergunta (use como base factual, mas NUNCA cole trechos entre colchetes ou o formato bruto abaixo — reescreva tudo com suas próprias palavras, no seu tom natural. Se houver um link de verificação no contexto, inclua ele na sua resposta para o usuário poder conferir o dado. Se houver aviso de dado desatualizado, mencione isso ao usuário):
{contexto}
...

Pergunta do usuário: {pergunta}

Responda usando os dados acima quando aplicável, no tom da Alessandra, sem recomendar compra ou venda, e sem repetir o formato do contexto literalmente."""
    else:
        mensagem_usuario = pergunta

    return system_prompt, mensagem_usuario


def chamar_llm(system_prompt, mensagem_usuario):
    resposta = ollama.chat(
        model=MODELO_LLM,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": mensagem_usuario}
        ]
    )
    return resposta["message"]["content"]


FRASES_PROIBIDAS = [
    "você deveria comprar", "você deveria vender", "recomendo comprar",
    "recomendo vender", "compre agora", "venda agora", "é um bom momento para comprar",
    "é um bom momento para vender"
]


def validar_resposta(texto):
    texto_lower = texto.lower()
    for frase in FRASES_PROIBIDAS:
        if frase in texto_lower:
            return "Como sua amiga aqui, eu não posso te dizer se você deve ou não comprar ou vender um ativo. Posso te mostrar dados e notícias pra você decidir com mais segurança — quer tentar reformular sua pergunta?"
    return texto


def responder(pergunta):
    tipo = classificar_pergunta(pergunta)

    if tipo == "cotacao":
        contexto = buscar_contexto_cotacao(pergunta)

        if contexto is None or contexto == "NENHUM_DADO_ENCONTRADO":
            resposta_fallback = "Poxa, não encontrei essa cotação na minha base de dados agora. Pode conferir se digitou o código certo da ação (ex: VALE3, PETR4)? Se quiser, posso te ajudar com outra ação ou com uma pergunta sobre o mercado em geral."
            return {"tipo_pergunta": tipo, "contexto_usado": None, "resposta": resposta_fallback}
    elif tipo == "busca_empresa":
        contexto = buscar_contexto_empresa(pergunta)
        if contexto is None:
            return {
                "tipo_pergunta": tipo,
                "contexto_usado": None,
                "resposta": "Não consegui consultar a lista de empresas da B3 agora. Tente novamente mais tarde ou consulte diretamente o site da B3.",
            }
    elif tipo == "noticia":
        contexto = buscar_contexto_noticia()
        if contexto == "NOTICIAS_INDISPONIVEIS":
            return {
                "tipo_pergunta": tipo,
                "contexto_usado": None,
                "resposta": "Não consegui acessar as fontes de notícias agora. Tente novamente mais tarde ou confira diretamente os portais InfoMoney, Valor Econômico e G1 Economia.",
            }
    else:
        contexto = buscar_contexto_educativo(pergunta)

    if contexto == "BASE_CONHECIMENTO_NAO_INDEXADA":
        return {
            "tipo_pergunta": tipo,
            "contexto_usado": None,
            "resposta": (
                "Minha base local ainda nao foi indexada. Execute "
                "`python scripts/build_index.py` na pasta do projeto e tente novamente."
            ),
        }

    system_prompt, mensagem_usuario = montar_prompt(pergunta, contexto)
    resposta_bruta = chamar_llm(system_prompt, mensagem_usuario)
    resposta_final = validar_resposta(resposta_bruta)

    return {"tipo_pergunta": tipo, "contexto_usado": contexto, "resposta": resposta_final}

if __name__ == "__main__":
    perguntas_teste = [
        "O que é renda fixa?",
        "Qual a cotação da VALE3 hoje?",
    ]

    for p in perguntas_teste:
        print(f"\n{'='*60}")
        print(f"PERGUNTA: {p}")
        resultado = responder(p)
        print(f"TIPO DETECTADO: {resultado['tipo_pergunta']}")
        print(f"RESPOSTA: {resultado['resposta']}")
