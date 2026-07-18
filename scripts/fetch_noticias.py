import feedparser
import requests

FEEDS = {
    "InfoMoney": "https://www.infomoney.com.br/feed/",
    "Valor Econômico": "https://valor.globo.com/rss/valor/",
    "G1 Economia": "https://g1.globo.com/rss/g1/economia/",
}


def get_noticias(limite_por_fonte=5):
    todas_noticias = []

    for nome_fonte, url in FEEDS.items():
        try:
            resposta = requests.get(
                url,
                timeout=10,
                headers={"User-Agent": "Alessandra/1.0 (leitor RSS educacional)"},
            )
            resposta.raise_for_status()
            feed = feedparser.parse(resposta.content)
        except Exception as erro:
            # Cada feed e isolado para que uma fonte indisponivel nao derrube as demais.
            print(f"[AVISO] Falha ao acessar o feed de {nome_fonte}: {erro}")
            continue

        entradas = getattr(feed, "entries", [])
        if not isinstance(entradas, list):
            print(f"[AVISO] Resposta invalida no feed de {nome_fonte}")
            continue
        if getattr(feed, "bozo", False) and not entradas:
            detalhe = getattr(feed, "bozo_exception", "resposta invalida")
            print(f"[AVISO] Problema ao ler o feed de {nome_fonte}: {detalhe}")
            continue

        for entrada in entradas[:limite_por_fonte]:
            if not hasattr(entrada, "get"):
                continue
            titulo = str(entrada.get("title") or "").strip()
            if not titulo:
                continue
            todas_noticias.append({
                "fonte": nome_fonte,
                "titulo": titulo,
                "resumo": str(entrada.get("summary") or ""),
                "link": str(entrada.get("link") or ""),
                "publicado_em": str(entrada.get("published") or "")
            })

    return todas_noticias


if __name__ == "__main__":
    noticias = get_noticias(limite_por_fonte=3)
    print(f"Total de notícias encontradas: {len(noticias)}\n")
    for n in noticias:
        print(f"[{n['fonte']}] {n['titulo']}")
