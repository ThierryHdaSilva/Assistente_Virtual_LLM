import requests
import sqlite3
import os
from datetime import datetime, timedelta

# Caminho do banco de cache (sempre relativo à raiz do projeto)
CACHE_DB = os.path.join(os.path.dirname(__file__), "..", "cache", "cotacoes_cache.db")
CACHE_MINUTOS_VALIDADE = 10  # depois desse tempo, busca de novo na API


def criar_tabela():
    os.makedirs(os.path.dirname(CACHE_DB), exist_ok=True)
    conn = sqlite3.connect(CACHE_DB)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cotacoes (
            ticker TEXT PRIMARY KEY,
            preco REAL,
            variacao_percent REAL,
            consultado_em TEXT,
            mercado_em TEXT
        )
    """)
    conn.commit()
    conn.close()


def get_cotacao(ticker):
    criar_tabela()
    conn = sqlite3.connect(CACHE_DB)
    cursor = conn.cursor()

    cursor.execute("SELECT preco, variacao_percent, consultado_em, mercado_em FROM cotacoes WHERE ticker = ?", (ticker,))
    linha = cursor.fetchone()

    if linha:
        preco, variacao, consultado_em_str, mercado_em_str = linha
        try:
            consultado_em = datetime.fromisoformat(consultado_em_str)
            if datetime.now() - consultado_em < timedelta(minutes=CACHE_MINUTOS_VALIDADE):
                conn.close()
                return _montar_resposta(ticker, preco, variacao, mercado_em_str, "cache")
        except (TypeError, ValueError):
            pass

    url = f"https://brapi.dev/api/quote/{ticker}"
    try:
        resposta = requests.get(url, timeout=10)
        resposta.raise_for_status()
        dados = resposta.json()
    except (requests.RequestException, ValueError):
        conn.close()
        return {"erro": "Servico de cotacoes indisponivel", "ticker": ticker}

    resultados = dados.get("results") if isinstance(dados, dict) else None
    if not isinstance(resultados, list) or not resultados:
        conn.close()
        return {"erro": f"Ticker {ticker} não encontrado", "ticker": ticker}

    resultado = resultados[0]
    if not isinstance(resultado, dict):
        conn.close()
        return {"erro": "Resposta invalida do servico de cotacoes", "ticker": ticker}

    preco = resultado.get("regularMarketPrice")
    variacao = resultado.get("regularMarketChangePercent")
    if not isinstance(preco, (int, float)) or not isinstance(variacao, (int, float)):
        conn.close()
        return {"erro": "Resposta incompleta do servico de cotacoes", "ticker": ticker}

    mercado_em = str(resultado.get("regularMarketTime") or "")
    nome_empresa = resultado.get("longName") or resultado.get("shortName") or ""
    agora = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO cotacoes (ticker, preco, variacao_percent, consultado_em, mercado_em)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(ticker) DO UPDATE SET preco=excluded.preco, variacao_percent=excluded.variacao_percent,
            consultado_em=excluded.consultado_em, mercado_em=excluded.mercado_em
    """, (ticker, preco, variacao, agora, mercado_em))
    conn.commit()
    conn.close()

    return _montar_resposta(ticker, preco, variacao, mercado_em, "brapi.dev", nome_empresa)


def _montar_resposta(ticker, preco, variacao, mercado_em_str, fonte, nome_empresa=""):
    url_verificacao = f"https://www.google.com/finance/quote/{ticker}:BVMF"

    desatualizado = False
    if mercado_em_str:
        try:
            mercado_em = datetime.fromisoformat(mercado_em_str.replace("Z", "+00:00"))
            idade = datetime.now(mercado_em.tzinfo) - mercado_em
            if idade > timedelta(hours=20):
                desatualizado = True
        except (ValueError, TypeError):
            pass

    return {
        "ticker": ticker,
        "nome_empresa": nome_empresa,
        "preco": preco,
        "variacao_percent": variacao,
        "fonte": fonte,
        "horario_do_dado": mercado_em_str,
        "url_verificacao": url_verificacao,
        "possivelmente_desatualizado": desatualizado
    }


def buscar_empresas(termo_busca=None, limite=10):
    url = "https://brapi.dev/api/quote/list"
    params = {"limit": limite}
    if termo_busca:
        params["search"] = termo_busca

    try:
        resposta = requests.get(url, params=params, timeout=10)
        resposta.raise_for_status()
        dados = resposta.json()
    except (requests.RequestException, ValueError):
        return []

    stocks = dados.get("stocks") if isinstance(dados, dict) else None
    if not isinstance(stocks, list):
        return []

    resultado = []
    for item in stocks[:limite]:
        if not isinstance(item, dict):
            continue
        resultado.append({
            "ticker": item.get("stock", ""),
            "nome": item.get("name", ""),
        })
    return resultado


if __name__ == "__main__":
    resultado = get_cotacao("VALE3")
    print(resultado)
