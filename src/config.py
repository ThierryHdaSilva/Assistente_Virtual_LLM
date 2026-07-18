import os

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")

# Caminhos de dados e cache
DATA_DIR = os.path.join(BASE_DIR, "data")
CACHE_DIR = os.path.join(BASE_DIR, "cache")
CHROMA_PATH = os.path.join(CACHE_DIR, "chroma_db")
HISTORICO_DB = os.path.join(CACHE_DIR, "historico_conversa.db")
CHROMA_COLLECTION = "base_conhecimento_v2"

# Arquivos gerados em runtime ficam fora do Git e a pasta nasce no primeiro uso.
os.makedirs(CACHE_DIR, exist_ok=True)

# A base P0 acompanha o projeto. O caminho ainda pode ser sobrescrito por variavel de ambiente.
HISTORICAL_EVENTS_DIR = os.getenv(
    "HISTORICAL_EVENTS_DIR",
    os.path.join(DATA_DIR, "base_historica"),
)

# Modelo LLM (Ollama)
MODELO_LLM = "qwen2.5:7b-instruct"

# Modelo de embeddings (RAG)
MODELO_EMBEDDING = "all-MiniLM-L6-v2"

# Modelo de classificação de sentimento
MODELO_SENTIMENTO = "lucas-leme/FinBERT-PT-BR"


def carregar_system_prompt():
    caminho = os.path.join(DATA_DIR, "system_prompt.txt")
    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()
