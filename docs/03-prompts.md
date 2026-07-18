# Prompts do Agente - Alessandra

Documentação da camada de instruções e do contexto dinâmico usados pela implementação atual.

## Fonte de verdade

O prompt fixo executado pela aplicação está em `data/system_prompt.txt`. Este documento explica como ele é consumido, mas não substitui esse arquivo.

`src/config.py` lê o conteúdo com `carregar_system_prompt()`. Depois, `src/agente.py` acrescenta somente o contexto necessário para a pergunta atual.

## Objetivos do prompt fixo

O prompt de sistema define:

- identidade e tom da Alessandra;
- escopo educacional ligado a finanças e mercado brasileiro;
- proibição de recomendação direta e execução de operações;
- proibição de previsão de preço;
- cuidado com dados pessoais e perfil de risco;
- necessidade de usar dados recebidos pelas ferramentas;
- transparência quando a fonte não fornece informação suficiente;
- tratamento conservador dos eventos históricos parcialmente verificados.

## Roteamento atual

Antes de montar o prompt, `classificar_pergunta()` escolhe uma rota simples:

| Condição | Rota | Contexto usado |
|---|---|---|
| Ticker no formato `VALE3`, `PETR4` etc. | `cotacao` | `brapi.dev` ou cache local |
| Pedido de lista/empresas | `busca_empresa` | Lista parcial da `brapi.dev` |
| Termos como notícia, hoje ou recente | `noticia` | Feeds RSS e sentimento |
| Demais perguntas | `educativa` | RAG local com glossário e eventos P0 |

BCB, CVM e GDELT não possuem rota nem chamada de ferramenta na versão atual. São fontes planejadas.

## Contexto dinâmico

Quando há contexto, `montar_prompt()` adiciona três partes:

1. orientação para usar o material como base factual;
2. dados recuperados pela rota escolhida;
3. pergunta original do usuário e reforço para não recomendar compra ou venda.

O modelo é instruído a reformular o conteúdo no tom da Alessandra, sem reproduzir os rótulos técnicos brutos. Links de verificação presentes no contexto devem ser incluídos na resposta.

### RAG educativo e histórico

O ChromaDB retorna até quatro documentos. Cada trecho recebe um rótulo técnico:

```text
[glossario financeiro] ...
[evento historico P0] ...
```

Os eventos contêm somente claims e fontes existentes na base P0. O fato de a cadeia estar congelada e auditada não transforma campos ausentes em fatos verificados.

### Cotação

Formato aproximado enviado ao modelo:

```text
- VALE3: R$ <preco> (<variacao>% no dia).
  Fonte: brapi.dev, horario do dado: <timestamp>.
  Link para o usuario conferir: <url>
```

Se o cache estiver válido, a fonte técnica pode aparecer como `cache`, preservando o horário original do mercado. Um aviso é acrescentado quando o dado pode estar desatualizado.

### Notícias

Formato aproximado enviado ao modelo:

```text
[InfoMoney] <titulo> - Publicado em: <data do feed>.
Link: <url>. Sentimento: <rotulo automatico>
```

Até cinco notícias válidas entram no contexto. A data e o link vêm do próprio feed. O sentimento é calculado pelo `FinBERT-PT-BR` e deve ser tratado como classificação automática do título.

As notícias não são indexadas no RAG e não são persistidas em banco local.

### Lista de empresas

A listagem é explicitamente apresentada ao modelo como parcial. O prompt dinâmico proíbe inventar tickers fora do retorno e orienta o usuário a consultar a B3 para a lista integral.

## Fallbacks atuais

Quando uma integração externa falha, o dado incompleto não é enviado ao LLM:

- cotação indisponível ou inválida: informa que a cotação não foi encontrada e sugere conferir o ticker;
- lista da B3 indisponível: informa a falha e aponta o site da B3;
- todos os feeds indisponíveis ou inválidos: informa a falha e aponta os portais originais;
- falha apenas na classificação de sentimento: mantém a notícia e marca o sentimento como indisponível;
- índice vazio: orienta executar `python scripts/build_index.py`.

## Validação pós-geração

`validar_resposta()` procura um conjunto pequeno de frases literais de recomendação, como “recomendo comprar” ou “compre agora”. Quando encontra uma delas, substitui a saída por uma recusa educativa.

Esse filtro é complementar e simples. Ele não comprova fatos, não valida todos os números e não cobre toda reformulação possível. As regras do prompt e a qualidade do contexto continuam essenciais.

## Exemplos coerentes com a implementação

### Conceito financeiro

```text
O que é renda fixa?
```

Rota esperada: `educativa`, com trechos do glossário local.

### Evento histórico

```text
O que aconteceu na crise cambial brasileira de 1999?
```

Rota esperada: `educativa`, com recuperação do evento P0 e somente dos claims presentes na base.

### Cotação

```text
Qual a cotação da PETR4 hoje?
```

Rota esperada: `cotacao`, com valor retornado pela `brapi.dev` ou pelo cache válido, horário e link de conferência.

### Notícias

```text
Quais são as notícias recentes do mercado?
```

Rota esperada: `noticia`, com títulos, veículos, datas, links e sentimentos automáticos disponíveis naquele momento.

### Fonte ainda não implementada

```text
Qual é a Selic atual segundo o Banco Central?
```

Não existe integração BCB no código atual. A Alessandra não deve fingir que consultou o SGS. Essa capacidade permanece planejada.

## Limites técnicos relevantes

- A conversa visível vive no `session_state` do Streamlit.
- O SQLite registra mensagens, mas não é carregado como memória do modelo.
- O agente não combina automaticamente cotação, notícia e evento histórico na mesma pergunta; ele escolhe uma rota principal.
- O classificador de rota é baseado em regex e palavras-chave, não em um modelo dedicado.
- Falhas do Ollama, ChromaDB ou carregamento dos modelos locais podem aparecer como erro de execução; os fallbacks implementados aqui cobrem as fontes HTTP.

## Fontes planejadas

| Fonte | Estado no prompt atual |
|---|---|
| BCB/SGS | Planejada; não afirmar consulta |
| CVM | Planejada; não afirmar consulta |
| GDELT | Planejada; não afirmar consulta |

Ao implementar uma dessas integrações, devem ser atualizados `src/agente.py`, a documentação da base, os exemplos deste arquivo e as regras de citação da fonte.

## Checklist manual de revisão

- A resposta usa apenas dados presentes no contexto?
- Cotações e notícias trazem fonte e horário/data disponível?
- Notícias trazem link quando o feed o fornece?
- Falhas externas resultam em mensagem clara, não em valor inventado?
- Eventos históricos respeitam a verificação parcial?
- A resposta evita recomendação, previsão e execução de operação?
- A aplicação não afirma consultar BCB, CVM ou GDELT?

