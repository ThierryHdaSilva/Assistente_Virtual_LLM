# Pitch — Alessandra (3 minutos)

> [!TIP]
> Você pode usar alguns slides para apoiar o pitch e mostrar a solução na prática. Não é necessário criar uma apresentação complexa: um slide para o problema, um para a solução e a demonstração da aplicação já são suficientes.

## Roteiro sugerido

### 1. O problema — 30 segundos

**Qual dor a solução resolve?**

> Para quem está começando a investir, entender o mercado financeiro pode ser muito difícil. Existem termos técnicos, notícias desconectadas e muitas opiniões dizendo o que comprar ou vender. Além disso, uma inteligência artificial que inventa cotações ou faz recomendações pode causar prejuízos. Por isso, identifiquei a necessidade de uma ferramenta que ensine finanças de maneira simples, contextualizada e responsável.

### 2. A solução — 1 minuto

**Como a Alessandra resolve esse problema?**

> A Alessandra é uma assistente financeira educacional focada no mercado brasileiro. Ela explica conceitos em linguagem acessível, consulta cotações da B3, apresenta notícias e usa eventos históricos para ajudar o usuário a entender o contexto econômico.
>
> A aplicação foi desenvolvida em Python com uma interface em Streamlit. O modelo Qwen 2.5 funciona localmente pelo Ollama. Para perguntas educativas e históricas, a Alessandra consulta uma base RAG no ChromaDB com 550 documentos: 357 verbetes financeiros e 193 eventos históricos parcialmente verificados. Cotações e notícias são consultadas por ferramentas próprias.
>
> A Alessandra não foi criada para recomendar compra ou venda. Seu objetivo é explicar os dados e ajudar o usuário a aprender, preservando sua autonomia.

### 3. Demonstração — 1 minuto

**O que será mostrado?**

Abra a aplicação e faça estas três perguntas, uma de cada vez:

```text
O que é renda fixa?

O que aconteceu na crise cambial brasileira de 1999?

Compre 100 ações de PETR4 para mim e confirme a operação.
```

Durante a demonstração, diga:

> Na primeira pergunta, a Alessandra usa o glossário para explicar um conceito financeiro em linguagem simples. Na segunda, ela consulta a base histórica e recupera um evento documentado. Na terceira, podemos observar um limite de segurança: como a Alessandra é educacional, ela não executa a operação nem deve recomendar a compra. Assim, a mesma aplicação combina educação financeira, contexto histórico e proteção ao usuário.

### 4. Diferencial e impacto — 30 segundos

**Por que a solução é diferente e qual impacto pode gerar?**

> O principal diferencial da Alessandra é combinar uma inteligência artificial local com uma base de conhecimento em português, estruturada e auditável. Isso reduz custos, aumenta o controle sobre os dados e ajuda a tornar a educação financeira mais acessível. O protótipo também está sendo submetido a testes de segurança para identificar falhas antes de qualquer uso público. O impacto esperado é ajudar mais pessoas a compreender o mercado sem depender de dicas ou promessas de ganho rápido.

## Checklist do pitch

- [ ] Duração máxima de 3 minutos.
- [ ] Problema claramente definido.
- [ ] Solução demonstrada na prática.
- [ ] Diferencial explicado.
- [ ] Aplicação aberta e testada antes da gravação.
- [ ] Áudio e vídeo com boa qualidade.
- [ ] Nenhuma afirmação de que o sistema recomenda investimentos ou está pronto para produção.

## Link do vídeo

[Assista ao pitch da Alessandra no YouTube](https://youtu.be/2KN9VaPvJD4)
