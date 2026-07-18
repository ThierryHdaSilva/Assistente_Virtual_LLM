from transformers import AutoTokenizer, BertForSequenceClassification, pipeline

MODELO = "lucas-leme/FinBERT-PT-BR"

print(f"Carregando modelo {MODELO}... (primeira vez pode demorar, ele baixa o modelo)")

tokenizer = AutoTokenizer.from_pretrained(MODELO)
model = BertForSequenceClassification.from_pretrained(MODELO)
classifier = pipeline(task="text-classification", model=model, tokenizer=tokenizer)


def classificar(texto):
    resultado = classifier(texto)
    return resultado[0]  # {'label': 'POSITIVE'/'NEGATIVE'/'NEUTRAL', 'score': 0.xx}


if __name__ == "__main__":
    frases_teste = [
        "Hoje a bolsa caiu",
        "Hoje a bolsa subiu",
        "O Ibovespa fechou estável nesta terça-feira"
    ]

    for frase in frases_teste:
        r = classificar(frase)
        print(f'"{frase}" -> {r["label"]} (confiança: {r["score"]:.2%})')