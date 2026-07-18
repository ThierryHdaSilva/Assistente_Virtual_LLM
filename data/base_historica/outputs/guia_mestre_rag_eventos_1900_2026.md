# GUIA MESTRE PARA CONSTRUÇÃO DE UM BANCO DE DADOS RAG
## Eventos históricos, econômicos, políticos, geopolíticos, tecnológicos, sanitários e geográficos

**Escopo principal:** 1º de janeiro de 2000 a 13 de julho de 2026  
**Precedentes estruturais:** 1900 a 1999, selecionados por relevância econômica  
**Âncora temporal absoluta:** 13 de julho de 2026, 23h59, horário de Brasília  
**Público-alvo:** investidores brasileiros e agentes financeiros educacionais  
**Formato recomendado de saída:** JSONL particionado, com índices auxiliares em JSON e documentação em Markdown  
**Natureza do conteúdo:** histórico, factual, educacional e não prescritivo

---

# 1. MISSÃO DO PROJETO

Construir uma base histórica e geoeconômica extensa, auditável e preparada para recuperação aumentada por geração (RAG), capaz de responder não apenas “o que aconteceu?”, mas também:

- qual foi o gatilho verificável;
- por quais canais o choque chegou à economia real e aos mercados;
- quais ativos reagiram, em qual janela temporal e com qual intensidade;
- o que foi reação contemporânea e o que só ficou claro retrospectivamente;
- quais efeitos atingiram especificamente o Brasil;
- quais consequências fiscais, regulatórias, jurídicas, sociais, securitárias e logísticas permaneceram;
- quais eventos anteriores constituem precedentes úteis;
- quais afirmações são fatos, estimativas, interpretações ou alegações ainda em investigação.

A base deve funcionar como “memória de mercado” e não como coleção de narrativas soltas. Cada registro precisa ser rastreável até fontes, comparável com outros eventos e recuperável por data, região, classe de ativo, setor, empresa, canal de transmissão e grau de severidade.

## 1.1 Meta de cobertura

O catálogo deste guia contém aproximadamente 700 itens priorizados, incluindo precedentes e algumas referências cruzadas. Depois da deduplicação canônica, escolher um dos perfis:

- **Edição essencial:** 150 a 220 eventos, concentrada em P0;
- **Edição estendida:** 350 a 500 eventos, adequada à meta de 300 a 800 páginas;
- **Edição integral:** 600 a 750 eventos, provavelmente exigindo mais de 800 páginas ou múltiplos volumes.

Para uma versão estendida ou integral, usar como referência:

- 800 a 2.500 subeventos ou marcos de linha do tempo;
- 2.000 a 8.000 observações de mercado;
- 5 a 12 fontes por evento de prioridade máxima;
- 3 a 8 fontes por evento de prioridade média;
- 1 a 3 fontes para itens contextuais de baixa materialidade.

Essas quantidades são metas de cobertura, não autorização para preencher lacunas com conteúdo inventado.

## 1.2 O que esta base não deve fazer

- Não recomendar compra, venda, proteção ou alocação.
- Não transformar correlação em causalidade.
- Não atribuir crime, fraude ou responsabilidade sem qualificar o estágio processual.
- Não usar uma manchete como prova suficiente de impacto econômico.
- Não apresentar estimativas antigas como números definitivos.
- Não tratar um movimento diário de mercado como consequência exclusiva do evento se houve choques concorrentes.
- Não incorporar fatos ocorridos depois da âncora temporal.
- Não produzir “status atual” a partir de memória sem consulta datada.

---

# 2. DECISÕES DE ARQUITETURA

## 2.1 Não usar um único JSON gigantesco

Para uma base de centenas de páginas, um único array JSON é frágil: um erro de sintaxe pode invalidar o arquivo inteiro, atualizações ficam custosas e a proveniência se perde. O formato preferido é JSONL, um objeto por linha, particionado por entidade.

Estrutura recomendada:

    database/
      events/
        events_1900_1999.jsonl
        events_2000_2009.jsonl
        events_2010_2019.jsonl
        events_2020_2023.jsonl
        events_2024_2026-07-13.jsonl
      episodes/
        episodes.jsonl
      observations/
        market_observations.jsonl
        macro_observations.jsonl
        fiscal_observations.jsonl
        insurance_loss_observations.jsonl
      entities/
        people.jsonl
        institutions.jsonl
        companies.jsonl
        countries_regions.jsonl
        assets_instruments.jsonl
      sources/
        sources.jsonl
      relations/
        event_relations.jsonl
      indexes/
        chronology.json
        taxonomy.json
        aliases.json
      docs/
        methodology.md
        data_dictionary.md
        source_policy.md
        changelog.md

## 2.2 Unidades de informação

**Episódio:** processo amplo e prolongado, como “Crise Financeira Global de 2007–2009”.

**Evento:** choque delimitável e recuperável, como “pedido de falência do Lehman Brothers”.

**Subevento:** etapa relevante, como “rejeição inicial do TARP pela Câmara”.

**Observação:** medida de uma variável em data e horário determinados, como o fechamento do Ibovespa, a taxa do DI ou o preço do Brent.

**Entidade:** pessoa, órgão, empresa, país, índice, commodity ou instrumento.

**Relação:** vínculo tipado entre registros, como “precede”, “agrava”, “desencadeia”, “responde a”, “é parte de” ou “é comparável a”.

## 2.3 Regra de granularidade

Criar registros separados quando houver pelo menos um dos seguintes elementos:

- gatilhos diferentes;
- datas de mercado diferentes;
- instrumentos de política distintos;
- consequências regulatórias próprias;
- fontes e controvérsias próprias;
- utilidade provável como pergunta independente no RAG.

Exemplo: “COVID-19” deve ser um episódio. Declaração de pandemia, circuit breakers da B3, corte emergencial do Fed, auxílio emergencial brasileiro, WTI negativo, início da vacinação e crise global de semicondutores devem ser eventos relacionados, e não um verbete monolítico.

---

# 3. DIRETRIZES INEGOCIÁVEIS PARA A IA CONSTRUTORA

## 3.1 Âncora temporal e controle de versão

1. O presente absoluto da base é **13 de julho de 2026, 23h59, horário de Brasília**.
2. Fatos posteriores não podem aparecer nem como desdobramentos.
3. Toda fonte deve registrar data de publicação e, quando disponível, data de atualização.
4. Diferenciar “data do evento”, “data em que o mercado tomou conhecimento” e “data de publicação da fonte”.
5. O campo de status deve informar: confirmado, provisório, contestado, sob investigação, decidido judicialmente, revertido, encerrado ou em curso.
6. Toda revisão posterior da base deve gerar novo número de versão e changelog.

## 3.2 Disciplina de evidência

1. Nenhum número financeiro sem fonte, unidade, data-base e metodologia.
2. Nenhuma cotação “aproximada” apresentada como fechamento oficial.
3. Nenhuma acusação apresentada como fato consumado.
4. Se duas fontes confiáveis divergirem, registrar a divergência.
5. Se o horário exato não for conhecido, usar precisão “dia”, “mês” ou “intervalo”; nunca inventar hora.
6. Coordenadas exatas só são obrigatórias para um local físico delimitável. Para guerras, secas, pandemias e políticas públicas, usar países, regiões, bacias, corredores logísticos ou polígonos aproximados.
7. Toda frase de causalidade deve receber um nível de confiança e uma justificativa.

## 3.3 Abordagem “follow the money”

Para cada evento, mapear os canais aplicáveis:

- crescimento e atividade;
- inflação;
- câmbio;
- política monetária;
- curva de juros e crédito soberano;
- ações e fatores de estilo;
- crédito corporativo;
- commodities;
- comércio exterior;
- transporte e fretes;
- energia;
- seguros e resseguros;
- orçamento e dívida pública;
- emprego e renda;
- cadeia de suprimentos;
- regulação e compliance;
- confiança, liquidez e aversão a risco;
- fluxos de capital e balanço de pagamentos.

O texto deve mostrar a cadeia causal proposta. Exemplo:

    seca → menor calado → menos trânsitos → frete mais caro →
    prazo de entrega maior → pressão de custos → margem setorial menor

## 3.4 Imparcialidade e linguagem jurídica

Usar linguagem compatível com o estágio do caso:

- “alegação” quando ainda não verificada;
- “suspeita” ou “investigado” quando houver apuração formal;
- “denunciado” quando houver acusação formal;
- “réu” quando a denúncia tiver sido recebida;
- “condenado” com indicação de instância e possibilidade de recurso;
- “absolvido”, “anulado”, “arquivado” ou “prescrito” quando aplicável;
- “acordo”, “leniência”, “delação”, “NPA” ou “DPA” com seus efeitos exatos.

Evitar adjetivos editoriais como “calote”, “rombo”, “motosserra”, “farra”, “derretimento” e “explosão” nos campos canônicos. Eles podem constar como aliases de imprensa, com aspas e fonte.

## 3.5 Sem previsões e sem aconselhamento

Paralelos históricos são permitidos. Previsões, preços-alvo e recomendações são proibidos. O campo “lições” deve explicar mecanismos observados, limites da comparação e sinais que analistas historicamente monitoraram, sem indicar operação.

## 3.6 Correlação não é causalidade

Classificar cada relação causal:

- **direta_documentada:** mecanismo e evidência explícitos;
- **forte_inferência:** mecanismo plausível e evidência convergente;
- **correlação_temporal:** ocorreu na mesma janela, mas há fatores concorrentes;
- **contestada:** há interpretações materiais divergentes;
- **não_determinada:** evidência insuficiente.

## 3.7 Janelas de mercado

Sempre que houver dados, coletar:

- T-20, T-5 e T-1;
- intradia imediatamente anterior ao gatilho;
- T0;
- T+1, T+5, T+20, T+60 e T+252;
- máximo drawdown e tempo de recuperação;
- retorno em moeda local e, quando relevante, em dólar;
- benchmark apropriado;
- volume, volatilidade implícita, spreads ou CDS;
- informação sobre mercado fechado, feriado, leilão, limite de oscilação ou circuit breaker.

Não usar “dia seguinte” se o dia seguinte não foi pregão.

## 3.8 Valores monetários

Cada valor deve registrar:

- moeda;
- valor nominal;
- data-base;
- conversão cambial, se houver;
- valor real opcional;
- índice de inflação usado;
- natureza: dano direto, perda econômica, perda segurada, provisão, multa, resgate, valor de mercado perdido ou custo fiscal;
- estimativa inicial, revisada ou final.

“Perda de valor de mercado” não equivale a “dinheiro perdido pela economia”. “Dano econômico” não equivale a “perda segurada”. “Crédito autorizado” não equivale a “despesa executada”.

## 3.9 Brasil como camada obrigatória

Mesmo em eventos externos, verificar:

- Ibovespa e índices setoriais;
- EWZ e ADRs brasileiras;
- USD/BRL;
- DXY como controle externo;
- curva DI por vértices;
- NTN-B e prefixados;
- CDS Brasil de 5 anos, quando disponível;
- fluxo estrangeiro na B3;
- minério, petróleo, soja, milho, café, açúcar, boi, celulose e fertilizantes;
- balança comercial e termos de troca;
- setores e empresas brasileiras expostos;
- reação do BCB, Tesouro, CMN, CVM, B3, SUSEP, CADE, Congresso, STF ou Executivo;
- impacto federativo quando houver.

## 3.10 Eventos concorrentes

Registrar choques que contaminem a leitura. Uma queda de bolsa no mesmo dia de decisão do Fed, divulgação de inflação e crise política doméstica não pode ser atribuída integralmente a apenas um deles.

---

# 4. POLÍTICA DE FONTES

## 4.1 Hierarquia recomendada

**Nível A — fontes primárias e registros oficiais**

- Banco Central do Brasil, Tesouro Nacional, IBGE, Ipea, MDIC/Comex Stat;
- CVM, B3, SUSEP, CADE, TCU, CGU, AGU, STF e tribunais;
- Diário Oficial e textos legais;
- SEC, CFTC, Federal Reserve, Treasury, FDIC, OCC, ECB, BoE, BoJ;
- bolsas, câmaras de compensação e administradores oficiais de índices;
- filings, fatos relevantes, balanços e documentos judiciais;
- ONU, FMI, Banco Mundial, BIS, OCDE, OMC, OMS, FAO, IEA e agências técnicas;
- USGS, NOAA, Copernicus, INMET, Cemaden, ANA e Defesa Civil.

**Nível B — fontes institucionais e bases especializadas**

- relatórios de bancos multilaterais;
- centros acadêmicos e artigos revisados;
- Swiss Re, Munich Re e bases de catástrofes;
- relatórios setoriais com metodologia pública;
- provedores de dados financeiros licenciados.

**Nível C — jornalismo de alta reputação**

- agências e veículos com data, autoria, correções e fontes identificáveis.

**Nível D — fontes auxiliares**

- agregadores, enciclopédias e bancos comunitários, usados apenas para descoberta;
- redes sociais, apenas como registro do pronunciamento original, nunca como validação autônoma;
- brapi.dev e APIs semelhantes, úteis para prototipagem, mas não substitutas do dado oficial ou licenciado.

## 4.2 Requisitos mínimos por tipo de afirmação

- Cotação e volume: bolsa, administrador do índice ou provedor reconhecido.
- Decisão monetária: banco central e ata/comunicado.
- Custo fiscal: Tesouro, orçamento, tribunal de contas ou lei.
- Multa e sanção: regulador, tribunal ou acordo publicado.
- Fatalidades e danos: autoridade competente mais organismo técnico; registrar revisões.
- Crime ou fraude: documento processual, regulador ou órgão investigador.
- Impacto segurado: resseguradora ou estudo técnico com data-base.
- Evento militar: fontes oficiais de mais de uma parte mais verificação jornalística independente.

## 4.3 Registro de fonte

Cada fonte deve conter:

    {
      "source_id": "SRC-BCB-2026-06-COPOM-279",
      "title": "...",
      "publisher": "Banco Central do Brasil",
      "url": "https://...",
      "publication_date": "2026-06-...",
      "updated_at": null,
      "accessed_at": "2026-07-13T18:00:00-03:00",
      "source_level": "A",
      "language": "pt-BR",
      "document_type": "comunicado",
      "supports": ["claim_id_1", "claim_id_2"],
      "archive_url": null,
      "notes": null
    }

---

# 5. PADRÃO OBRIGATÓRIO DO VERBETE

## 5.1 Identificação

- Nome canônico.
- Aliases e nomes usados pela imprensa.
- ID estável.
- Episódio-pai e eventos relacionados.
- Prioridade: P0, P1 ou P2.
- Categorias e tags.

## 5.2 Data, horário e precisão

- Início e fim.
- Horário local e UTC.
- Momento em que a informação se tornou pública.
- Precisão temporal.
- Sessão de mercado afetada.

## 5.3 Atores, entidades e geografia

- Pessoas, governos, empresas, órgãos e grupos.
- Países, regiões, cidades, bacias, rotas e instalações.
- Coordenadas ou polígono somente quando apropriado.

## 5.4 Contexto anterior ao choque

- Regime macroeconômico.
- Condições de liquidez e posicionamento.
- Fragilidades acumuladas.
- Narrativa dominante antes do gatilho.
- Dados que o mercado já conhecia.

## 5.5 Gatilho verificável

- Ato, anúncio, acidente, divulgação, voto, ataque, quebra, desastre ou decisão.
- Fonte que confirma o gatilho.
- Se era esperado, surpresa parcial ou surpresa ampla.

## 5.6 Linha do tempo factual

- Marcos com data/hora.
- Separação entre fatos e alegações.
- Revisões de números.
- Respostas de autoridades.
- Encerramento ou transformação do evento.

## 5.7 Canais de transmissão

Para cada canal:

- mecanismo;
- direção esperada ex ante;
- evidência observada ex post;
- defasagem;
- grau de confiança;
- fatores concorrentes.

## 5.8 Impacto imediato nos mercados

### Brasil

- Ibovespa, volume e circuit breaker;
- USD/BRL;
- DI por vértice;
- títulos públicos e CDS;
- setores, ações, ADRs e ETFs;
- commodities relevantes;
- fluxo estrangeiro.

### Global

- S&P 500, Nasdaq, Dow, Stoxx 600, Nikkei, Hang Seng e MSCI EM, conforme aplicável;
- VIX;
- DXY e principais pares;
- Treasuries e curvas soberanas;
- ouro;
- petróleo, gás, carvão, metais e agrícolas;
- spreads de crédito, fretes e volatilidade.

## 5.9 Estudo de evento

- Janela usada.
- Preço de abertura, mínima, máxima e fechamento.
- Retorno simples e anormal.
- Benchmark.
- Moeda.
- Fonte.
- Observação sobre sobreposição de choques.
- Limitação metodológica.

## 5.10 Economia real e distribuição dos efeitos

- PIB e produção;
- emprego e renda;
- comércio;
- inflação;
- crédito;
- infraestrutura;
- efeitos regionais;
- grupos sociais afetados;
- horizonte temporal.

## 5.11 Setores, empresas e instrumentos

Para cada item, registrar:

- exposição;
- mecanismo;
- reação observada;
- horizonte;
- fonte;
- se o efeito foi temporário ou persistente.

## 5.12 Custos, seguros e impacto fiscal

- danos diretos;
- perdas indiretas;
- perdas seguradas;
- proteção insuficiente;
- resgates e garantias;
- créditos extraordinários;
- impacto em resultado primário, dívida ou passivos contingentes;
- custo privado versus público.

## 5.13 Respostas monetária, fiscal e cambial

- decisão;
- autoridade;
- instrumento;
- tamanho;
- prazo;
- objetivo declarado;
- execução;
- avaliação posterior documentada.

## 5.14 Regulação, investigação e compliance

- leis e normas;
- processos;
- sanções;
- acordos;
- mudanças de governança;
- efeitos sobre auditoria, disclosure, capital, liquidez, proteção ao consumidor e concorrência.

## 5.15 Desdobramentos até a âncora

- status em 13 de julho de 2026;
- efeitos encerrados e persistentes;
- reparações, recuperações ou reestruturações;
- controvérsias abertas;
- próximos marcos já agendados, sem previsão do resultado.

## 5.16 Lições e precedentes

- mecanismo educacional;
- paralelo histórico;
- diferenças que limitam o paralelo;
- indicadores que passaram a ser monitorados;
- nenhuma recomendação de investimento.

## 5.17 Curiosidades financeiras

Somente fatos verificáveis:

- posições short documentadas;
- operações de hedge;
- falhas de precificação;
- disfunções de mercado;
- falências ou aquisições;
- anedotas com fonte.

## 5.18 Fontes, confiança e revisão

- fontes por afirmação;
- grau de confiança;
- divergências;
- data de última revisão;
- revisor;
- lacunas conhecidas.

---

# 6. ESQUEMA JSON CANÔNICO

O objeto abaixo é um modelo. Campos não aplicáveis devem ser nulos ou arrays vazios, nunca preenchidos artificialmente.

    {
      "schema_version": "1.0.0",
      "event_id": "EVT-YYYY-REGION-SLUG",
      "episode_id": "EPI-SLUG",
      "parent_event_id": null,
      "canonical_name_pt": "",
      "canonical_name_en": "",
      "aliases": [],
      "priority": "P0",
      "record_status": "verified",
      "event_status_at_cutoff": "closed|ongoing|contested|under_investigation",
      "cutoff_at": "2026-07-13T23:59:59-03:00",
      "categories": [],
      "tags": [],
      "time": {
        "start_local": null,
        "start_utc": null,
        "end_local": null,
        "end_utc": null,
        "public_awareness_at": null,
        "precision": "second|minute|hour|day|month|range",
        "timezone": null,
        "market_session": null
      },
      "geography": {
        "countries": [],
        "admin_regions": [],
        "cities": [],
        "physical_features": [],
        "coordinates": [],
        "bounding_box": null,
        "geographic_scope_note": null
      },
      "entities": {
        "people": [],
        "governments": [],
        "institutions": [],
        "companies": [],
        "groups": [],
        "assets": []
      },
      "context_before": {
        "macro": "",
        "political": "",
        "financial": "",
        "sectoral": "",
        "positioning_and_expectations": ""
      },
      "trigger": {
        "description": "",
        "trigger_type": "",
        "expectedness": "expected|partly_expected|surprise|unknown",
        "claim_ids": []
      },
      "timeline": [
        {
          "at": "",
          "precision": "",
          "description": "",
          "fact_status": "confirmed",
          "claim_ids": []
        }
      ],
      "transmission_channels": [
        {
          "channel": "",
          "mechanism": "",
          "lag": "",
          "direction": "",
          "causality_level": "direta_documentada",
          "confounders": [],
          "claim_ids": []
        }
      ],
      "market_impact": {
        "brazil": [],
        "global": [],
        "market_closed_or_disrupted": false,
        "event_study_method": {
          "windows": ["T-1", "T0", "T+1", "T+5", "T+20"],
          "benchmark": null,
          "currency_basis": null,
          "limitations": []
        }
      },
      "real_economy_impact": [],
      "sector_and_company_impact": [],
      "costs": {
        "direct_damage": [],
        "economic_loss": [],
        "insured_loss": [],
        "market_cap_change": [],
        "fiscal_measures": [],
        "contingent_liabilities": [],
        "methodology_notes": []
      },
      "policy_responses": {
        "monetary": [],
        "fiscal": [],
        "fx": [],
        "prudential": [],
        "trade": [],
        "humanitarian": []
      },
      "legal_regulatory_compliance": [],
      "status_at_cutoff": {
        "summary": "",
        "persistent_effects": [],
        "resolved_effects": [],
        "open_questions": [],
        "scheduled_milestones": []
      },
      "lessons": [],
      "historical_precedents": [],
      "financial_curiosities": [],
      "related_event_ids": [],
      "claims": [
        {
          "claim_id": "",
          "text": "",
          "fact_status": "confirmed|estimated|alleged|contested",
          "confidence": 0.0,
          "source_ids": []
        }
      ],
      "source_ids": [],
      "rag": {
        "summary_80_words": "",
        "summary_250_words": "",
        "retrieval_questions": [],
        "keywords": [],
        "entities_normalized": [],
        "chunk_group": "",
        "do_not_answer_without_live_data": []
      },
      "quality": {
        "completeness_score": 0,
        "source_quality_score": 0,
        "causal_confidence_score": 0,
        "last_reviewed_at": "",
        "review_notes": []
      }
    }

## 6.1 Observação de mercado separada

    {
      "observation_id": "OBS-...",
      "event_id": "EVT-...",
      "instrument_id": "AST-USDBRL",
      "timestamp": "",
      "session": "",
      "field": "close|open|high|low|yield|spread|volume",
      "value": null,
      "unit": "",
      "currency": "",
      "return_window": "",
      "benchmark_adjusted_return": null,
      "source_id": "",
      "data_vintage": "",
      "notes": ""
    }

---

# 7. PRIORIDADE E CRITÉRIO DE INCLUSÃO

## 7.1 Prioridades

- **P0 — indispensável:** mudou preços, política ou instituições em escala nacional/global.
- **P1 — obrigatório:** efeito relevante em setores, regiões ou classes de ativos.
- **P2 — contextual:** ajuda a explicar padrões, contágio ou precedentes.

## 7.2 Teste de materialidade

Incluir um evento se cumprir pelo menos dois critérios, ou um critério de intensidade excepcional:

- movimento relevante de preços ou volatilidade;
- disfunção de mercado;
- mudança material de política;
- custo fiscal ou econômico relevante;
- interrupção logística ou produtiva;
- mudança regulatória duradoura;
- falência, fraude ou resgate sistêmico;
- alteração de termos de troca;
- repercussão mensurável no Brasil;
- precedente amplamente usado por analistas;
- grande perda humana e de infraestrutura com transmissão econômica.

## 7.3 Anti-duplicação

Cada evento possui um registro canônico. Outros capítulos usam referências cruzadas. Não criar um segundo verbete para o mesmo choque apenas porque ele cabe em mais de uma categoria.

---

# 8. CATÁLOGO MESTRE DE EVENTOS

Legenda:

- **[P0]** indispensável;
- **[P1]** obrigatório;
- **[P2]** contextual;
- o texto após o travessão indica o principal eixo econômico a investigar, não uma conclusão pronta.

## 8.1 Precedentes estruturais anteriores a 2000

Estes eventos não integram o núcleo exaustivo de 2000–2026, mas são necessários para explicar regimes monetários, crises bancárias, inflação, commodities e instituições.

### Guerras, regimes monetários e grandes depressões

- **[P1] Pânico Bancário de 1907** — corridas bancárias, papel de J. P. Morgan e origem institucional do Federal Reserve.
- **[P1] Primeira Guerra Mundial e suspensão do padrão-ouro (1914–1918)** — dívida de guerra, inflação, comércio e mudança do centro financeiro global.
- **[P1] Pandemia de Influenza de 1918–1920** — trabalho, mortalidade, oferta e comparação metodológica com pandemias modernas.
- **[P2] Recessão e deflação de 1920–1921** — ajuste pós-guerra e volatilidade de commodities.
- **[P1] Hiperinflação de Weimar (1921–1923)** — moeda, dívida, indexação e ruptura social.
- **[P0] Crash de 1929 e Grande Depressão** — alavancagem, falências bancárias, desemprego, protecionismo e transmissão ao café brasileiro.
- **[P1] Smoot–Hawley e retaliação comercial (1930)** — espiral protecionista e contração do comércio.
- **[P1] Abandono do padrão-ouro e desvalorizações competitivas (1931–1936)** — espaço monetário, controles e blocos cambiais.
- **[P1] Política de valorização e destruição de estoques de café no Brasil** — sustentação de preços, câmbio e financiamento público.
- **[P1] Dust Bowl nos Estados Unidos (1930–1936)** — seca, migração, produtividade agrícola e crédito rural.
- **[P1] New Deal e Glass–Steagall (1933)** — seguro de depósitos, separação bancária e expansão fiscal.
- **[P2] Recessão norte-americana de 1937–1938** — retirada prematura de estímulos como precedente histórico.
- **[P0] Segunda Guerra Mundial (1939–1945)** — mobilização industrial, racionamento, dívida, commodities e reorganização produtiva.
- **[P0] Bretton Woods, criação do FMI e do Banco Mundial (1944–1945)** — dólar, câmbios fixos e arquitetura financeira multilateral.
- **[P1] Plano Marshall (1948–1952)** — reconstrução, produtividade europeia e integração comercial.
- **[P1] GATT e liberalização comercial do pós-guerra (1947 em diante)** — regras multilaterais que antecederam a OMC.

### Guerra Fria, petróleo e inflação

- **[P1] Revolução Chinesa e fundação da República Popular (1949)** — mudança estrutural posteriormente central para commodities e manufatura.
- **[P1] Guerra da Coreia (1950–1953)** — choque de commodities, inflação e gastos militares.
- **[P1] Crise de Suez (1956)** — canal marítimo, petróleo e risco de gargalos.
- **[P1] Criação da OPEP (1960)** — coordenação de produtores e poder de mercado.
- **[P2] Crise dos Mísseis de Cuba (1962)** — risco nuclear, ativos de refúgio e proximidade geopolítica do Brasil.
- **[P1] Golpe de 1964, PAEG e reformas financeiras no Brasil** — inflação, sistema bancário, correção monetária e Banco Central.
- **[P1] Escalada da Guerra do Vietnã e pressões sobre o dólar** — déficits externos, ouro e inflação.
- **[P0] Nixon Shock e fim da conversibilidade do dólar em ouro (1971)** — ruptura de Bretton Woods.
- **[P1] Adoção generalizada de câmbios flutuantes (1973)** — formação do regime cambial contemporâneo.
- **[P0] Embargo árabe e Primeiro Choque do Petróleo (1973–1974)** — estagflação, petrodólares e vulnerabilidade energética brasileira.
- **[P1] Milagre Econômico, Primeiro Choque e II PND no Brasil** — dívida externa, substituição de importações e infraestrutura.
- **[P0] Grande Geada do Café no Paraná (1975)** — choque global de oferta e migração geográfica da cafeicultura.
- **[P0] Revolução Iraniana e Segundo Choque do Petróleo (1978–1980)** — inflação, recessão e energia.
- **[P0] Choque Volcker (1979–1982)** — juros reais, dólar, recessão e crise da dívida emergente.
- **[P0] Moratória mexicana e crise da dívida latino-americana (1982)** — bancos internacionais, FMI e década perdida.
- **[P1] Crise da dívida e hiperinflação brasileira dos anos 1980** — indexação, dívida, planos heterodoxos e desorganização de preços.
- **[P1] Plano Cruzado e congelamento de preços (1986)** — inflação reprimida, desabastecimento e reversão.
- **[P1] Desastre nuclear de Chernobyl (1986)** — energia nuclear, custos públicos, agricultura e risco transfronteiriço.
- **[P1] Moratória brasileira de 1987** — crédito soberano, negociação externa e reputação.
- **[P0] Black Monday (19 de outubro de 1987)** — negociação programada, liquidez e mecanismos de circuit breaker.
- **[P1] Basileia I (1988)** — capital bancário e arbitragem regulatória.
- **[P1] Crise das Savings and Loans nos EUA** — risco de juros, seguro de depósitos e custo fiscal.

### Globalização, estabilização e crises emergentes

- **[P1] Queda do Muro de Berlim e dissolução da URSS (1989–1991)** — integração de mercados, privatização e nova geopolítica.
- **[P1] Estouro da bolha imobiliária e acionária japonesa (1989–1992)** — desalavancagem, deflação e “décadas perdidas”.
- **[P1] Plano Collor e bloqueio de ativos financeiros (1990)** — liquidez, confiança e direitos de propriedade.
- **[P1] Guerra do Golfo (1990–1991)** — petróleo, coalizões militares e prêmio geopolítico.
- **[P1] Crise do Mecanismo Europeu de Câmbio e “Black Wednesday” (1992)** — ataques especulativos e limites de bandas cambiais.
- **[P0] Plano Real (1993–1994)** — URV, estabilização, câmbio, juros e reorganização empresarial.
- **[P1] Crise do México e “Efeito Tequila” (1994–1995)** — capitais voláteis, reservas e pacote internacional.
- **[P1] Criação da OMC (1995)** — institucionalização do comércio global.
- **[P0] Crise Financeira Asiática (1997–1998)** — câmbios administrados, dívida em moeda estrangeira e contágio.
- **[P0] Default russo e colapso do LTCM (1998)** — arbitragem alavancada, liquidez e intervenção coordenada.
- **[P0] Crise cambial brasileira e adoção do câmbio flutuante (1999)** — desvalorização, metas de inflação e tripé macroeconômico.
- **[P1] Lançamento do euro (1999)** — moeda comum sem união fiscal plena.
- **[P2] Revogação de partes da Glass–Steagall pelo Gramm–Leach–Bliley Act (1999)** — consolidação financeira e debate regulatório.

## 8.2 Geografia física, clima e desastres ambientais

### Terremotos, tsunamis e falhas tectônicas

- **[P1] Terremoto de Gujarat, Índia (2001)** — reconstrução, seguros e infraestrutura industrial.
- **[P1] Terremoto de Bam, Irã (2003)** — patrimônio, ajuda internacional e economia regional.
- **[P0] Terremoto e tsunami do Oceano Índico (2004)** — turismo, pesca, portos, ajuda e reconstrução asiática.
- **[P1] Terremoto da Caxemira (2005)** — infraestrutura, fronteiras e capacidade fiscal.
- **[P1] Terremoto de Sichuan, China (2008)** — produção industrial, energia, reconstrução e aço.
- **[P0] Terremoto do Haiti (2010)** — colapso institucional, remessas, ajuda e custos humanos.
- **[P1] Terremoto de Maule, Chile (2010)** — cobre, celulose, portos, seguros e regras de construção.
- **[P1] Terremoto de Christchurch, Nova Zelândia (2011)** — resseguros, migração urbana e custo fiscal.
- **[P0] Terremoto, tsunami e acidente nuclear de Fukushima (2011)** — automóveis, eletrônicos, urânio, gás natural e política energética.
- **[P1] Terremotos do Nepal (2015)** — turismo, remessas e reconstrução.
- **[P1] Terremotos do México (2017)** — seguros catastróficos, infraestrutura e cadeias regionais.
- **[P1] Terremoto e tsunami de Sulawesi, Indonésia (2018)** — logística insular, óleo de palma e resposta pública.
- **[P0] Terremotos da Turquia e Síria (fevereiro de 2023)** — construção, lira, orçamento, aço, têxteis e risco soberano.
- **[P1] Terremoto de Al Haouz, Marrocos (2023)** — turismo, moradia rural e reconstrução.
- **[P1] Terremoto da Península de Noto, Japão (janeiro de 2024)** — componentes, automóveis e infraestrutura.
- **[P0] Terremoto de Hualien, Taiwan (abril de 2024)** — semicondutores, TSMC, concentração geográfica e seguros.
- **[P1] Terremoto do Tibete (janeiro de 2025)** — infraestrutura de altitude, transparência de dados e resposta estatal.
- **[P0] Terremoto de Myanmar e efeitos na Tailândia (março de 2025)** — fábricas, construção, guerra civil e perdas econômicas.
- **[P0] Terremotos de La Guaira e Caracas, Venezuela (24 de junho de 2026)** — moradia, saúde, dívida, sanções, reconstrução e ajuda internacional.

### Vulcões, cinzas e riscos atmosféricos

- **[P1] Erupção do Eyjafjallajökull, Islândia (2010)** — fechamento do espaço aéreo europeu, turismo e carga de alto valor.
- **[P2] Erupção do Grímsvötn, Islândia (2011)** — comparação com protocolos aéreos pós-2010.
- **[P1] Erupção do Cumbre Vieja em La Palma (2021)** — agricultura, moradia, turismo e seguros.
- **[P1] Erupção do Hunga Tonga–Hunga Haʻapai (2022)** — telecomunicações submarinas, tsunami e choque local.

### Ciclones, furacões, tempestades e incêndios

- **[P0] Furacão Katrina (2005)** — refino, petróleo e gás do Golfo, seguros, portos e reconstrução.
- **[P1] Ciclone Nargis em Myanmar (2008)** — arroz, ajuda humanitária e restrições políticas.
- **[P1] Incêndios “Black Saturday” na Austrália (2009)** — energia, seguros e adaptação.
- **[P1] Furacão Sandy (2012)** — Nova York, infraestrutura financeira, energia e seguros.
- **[P1] Tufão Haiyan nas Filipinas (2013)** — portos, agricultura, remessas e ajuda.
- **[P0] Furacões Harvey, Irma e Maria (2017)** — refino, petroquímica, Porto Rico, seguros e dívida municipal.
- **[P1] Ciclone Idai em Moçambique e Zimbábue (2019)** — portos, agricultura, dívida e ajuda.
- **[P1] Incêndios australianos de 2019–2020** — turismo, carvão, saúde e resseguros.
- **[P1] Incêndios da Califórnia e crises de utilities (2017–2020)** — PG&E, responsabilidade, falência e seguro residencial.
- **[P1] Tempestade de inverno Uri no Texas (2021)** — gás, eletricidade, preços extremos e desenho do ERCOT.
- **[P1] Inundações no vale do Ahr, Alemanha e Bélgica (2021)** — seguros, infraestrutura e adaptação europeia.
- **[P1] Inundações de Henan, China (2021)** — transporte urbano, fábricas e alimentos.
- **[P1] Furacão Ian (2022)** — seguros da Flórida, resseguros e habitação.
- **[P1] Tempestade Daniel e colapso de barragens em Derna, Líbia (2023)** — falha institucional e infraestrutura.
- **[P1] Incêndios florestais do Canadá (2023)** — madeira, petróleo, qualidade do ar e interrupções.
- **[P1] Furacão Beryl (2024)** — Caribe, Texas, energia, agricultura e seguros.
- **[P0] Furacões Helene e Milton (2024)** — seguros, infraestrutura, agricultura e perdas bilionárias nos EUA.
- **[P1] Inundações de Valência, Espanha (2024)** — automóveis, logística, seguros e alerta meteorológico.
- **[P0] Incêndios de Los Angeles (janeiro–fevereiro de 2025)** — perda segurada recorde, imóveis e disponibilidade de cobertura.
- **[P1] Incêndios florestais da Coreia do Sul (2025)** — patrimônio, evacuação e custo público.
- **[P1] Furacão Melissa no Caribe (outubro de 2025)** — Jamaica, Cuba, portos, turismo e seguros.
- **[P1] Inundações de Moçambique (2025–2026)** — ferrovias, agricultura, moradia e ajuda.
- **[P2] Tempestade Harry e deslizamento de Niscemi, Sicília (2026)** — evacuação, infraestrutura e risco geológico.

### Secas, calor, água, safras e corredores logísticos

- **[P1] Onda de calor europeia de 2003** — mortalidade, energia, agricultura e seguros.
- **[P1] Seca amazônica de 2005** — navegação, pesca, florestas e emissões.
- **[P1] Seca e incêndios na Rússia com restrição à exportação de trigo (2010)** — alimentos e tensões sociais.
- **[P1] Seca do Chifre da África (2011–2012)** — alimentos, migração e ajuda.
- **[P1] Seca dos Estados Unidos (2012)** — milho, soja, ração e preços globais.
- **[P1] Super El Niño de 2015–2016** — safras, pesca, energia e inflação de alimentos.
- **[P1] Seca prolongada na África Oriental (2020–2023)** — segurança alimentar, pecuária e migração.
- **[P1] Onda de calor europeia e baixo nível do Reno (2022)** — carvão, químicos, siderurgia e fretes.
- **[P0] Seca do Canal do Panamá (2023–2024)** — calado, filas, rotas alternativas e custos logísticos.
- **[P1] El Niño de 2023–2024** — energia, alimentos, pesca, secas e enchentes em múltiplas regiões.
- **[P1] Crise do cacau na África Ocidental (2023–2025)** — clima, doença, oferta, futuros e margens da indústria.
- **[P1] Citrus greening, clima e choque nos futuros de suco de laranja (2023–2025)** — Brasil, Flórida e concentração produtiva.

### Brasil: água, barragens, chuvas, queimadas e agro

- **[P0] Seca, racionamento e crise do “apagão” (2001–2002)** — hidrologia, falhas de planejamento, consumo e PIB.
- **[P1] Enchentes e deslizamentos em Santa Catarina (2008)** — portos, indústria, rodovias e reconstrução.
- **[P0] Desastre da Região Serrana do Rio de Janeiro (2011)** — ocupação urbana, defesa civil e infraestrutura.
- **[P1] Enchentes no Espírito Santo e em Minas Gerais (2013)** — logística e custo regional.
- **[P1] Crise hídrica de São Paulo (2014–2015)** — Cantareira, indústria, saneamento e governança da água.
- **[P0] Rompimento da Barragem de Fundão, Mariana (2015)** — mineração, Samarco, Vale/BHP, reparação e regulação.
- **[P0] Rompimento da Barragem de Córrego do Feijão, Brumadinho (2019)** — Vale, mortes, multas, produção e segurança de barragens.
- **[P1] Queimadas e pressão internacional sobre a Amazônia (2019–2020)** — ESG, acordos comerciais, agro e fiscalização.
- **[P1] Incêndios no Pantanal (2020)** — pecuária, biodiversidade, turismo e seguros.
- **[P0] Crise hídrica e bandeira “Escassez Hídrica” (2021)** — térmicas, inflação, tarifas e risco de racionamento.
- **[P1] Geadas no cinturão de café e cana (2021)** — arábica, açúcar, etanol e seguro rural.
- **[P1] Chuvas e enchentes na Bahia e em Minas Gerais (2021–2022)** — mineração, rodovias e moradia.
- **[P1] Tragédia de Petrópolis (2022)** — risco urbano, turismo e reconstrução.
- **[P1] Seca no Sul e quebras de safra (2021–2023)** — soja, milho, PIB agropecuário e crédito rural.
- **[P1] Chuvas no Litoral Norte de São Paulo (2023)** — rodovias, turismo, moradia e seguros.
- **[P0] Seca dos rios amazônicos e isolamento logístico de Manaus (2023–2024)** — Zona Franca, cabotagem e preços.
- **[P0] Enchentes no Rio Grande do Sul (abril–maio de 2024)** — indústria, arroz, logística, seguros, crédito e orçamento extraordinário.
- **[P1] Seca, queimadas e fumaça no Brasil central e na Amazônia (2024)** — hidroeletricidade, saúde, agro e navegação.

## 8.3 Macroeconomia global, bancos centrais e regimes de política

### Anos 2000: globalização, crédito e resposta à crise

- **[P1] Introdução física de notas e moedas de euro (2002)** — integração monetária, preços e infraestrutura financeira.
- **[P1] Período de juros baixos do Federal Reserve após 2001** — crédito, habitação e busca por rendimento.
- **[P1] Ciclo de alta do Fed de 2004–2006** — hipotecas de taxa ajustável, curva de juros e vulnerabilidade financeira.
- **[P1] “Global saving glut” e desequilíbrios externos dos anos 2000** — Treasuries, dólar, crédito e déficits.
- **[P1] Reação monetária e fiscal coordenada à crise de 2008–2009** — cortes de juros, garantias e expansão de balanços.
- **[P0] Primeiro Quantitative Easing do Federal Reserve (2008–2010)** — títulos, dólar, liquidez e ativos de risco.
- **[P1] Estímulo fiscal e creditício da China de 2008–2009** — infraestrutura, minério, aço e dívida local.
- **[P1] Elevação do G20 ao principal fórum econômico global (2008–2009)** — coordenação de crise e reforma financeira.

### Euro, políticas não convencionais e emergentes

- **[P0] Crise da dívida soberana da Zona do Euro (2010–2012)** — spreads, bancos, austeridade e risco de ruptura.
- **[P0] Primeiro resgate e reestruturações da dívida grega (2010–2012)** — troika, PSI e contágio.
- **[P1] Resgates de Irlanda, Portugal, Espanha e Chipre** — bancos, depósitos, austeridade e desenho da união monetária.
- **[P0] Discurso “whatever it takes” e OMT do BCE (2012)** — prêmio de redenominação e credibilidade.
- **[P1] LTROs e expansão de liquidez do BCE (2011–2012)** — funding bancário e carry soberano.
- **[P0] Taper Tantrum (2013)** — Treasuries, câmbio, juros e saída de capitais de emergentes.
- **[P1] “Fragile Five” e reprecificação de Brasil, Índia, Indonésia, África do Sul e Turquia (2013)** — déficits externos e vulnerabilidade.
- **[P1] Abenomics e expansão monetária japonesa (2013 em diante)** — iene, ações e inflação.
- **[P1] Adoção de juros negativos por bancos centrais europeus e pelo Japão (2014–2016)** — bancos, curvas e busca por rendimento.
- **[P1] Abandono do piso EUR/CHF pelo Banco Nacional Suíço (2015)** — perdas de corretoras, liquidez e gaps cambiais.
- **[P0] Desvalorização do renminbi e turbulência chinesa (agosto de 2015)** — commodities, emergentes e política cambial.
- **[P1] Circuit breakers e suspensão do mecanismo na bolsa chinesa (janeiro de 2016)** — desenho de mercado e efeito pró-cíclico.
- **[P1] Brexit: choque macro e resposta do Bank of England (2016)** — libra, gilts, investimento e incerteza.
- **[P1] Reforma tributária dos Estados Unidos de 2017** — lucros, repatriação, déficit e buybacks.
- **[P1] Aperto monetário do Fed e redução do balanço (2017–2019)** — dólar, funding e emergentes.
- **[P1] Pivot do Fed após o estresse do quarto trimestre de 2018** — condições financeiras e comunicação.
- **[P1] Crise de liquidez no mercado de repo dos EUA (setembro de 2019)** — reservas bancárias e operações do Fed.
- **[P1] Sincronização da desaceleração industrial global (2018–2019)** — manufatura, comércio e commodities.

### Pandemia, inflação e novo ciclo de juros

- **[P0] Corte emergencial do Fed, juros próximos de zero e QE de 2020** — liquidez global e Treasuries.
- **[P0] CARES Act e pacotes fiscais norte-americanos de 2020–2021** — renda, déficit, poupança e demanda.
- **[P1] Programas de compra emergencial do BCE e estímulos de outros bancos centrais (2020)** — spreads e crédito.
- **[P1] Suspensão de regras fiscais europeias e mutualização parcial via NextGenerationEU** — dívida comum e recuperação.
- **[P0] Surto inflacionário global de 2021–2023** — oferta, demanda, energia, salários e erro de classificação “transitória”.
- **[P0] Ciclo de alta do Federal Reserve de 2022–2023** — dólar, duration, crédito, bancos e emergentes.
- **[P1] Aperto sincronizado de bancos centrais em 2022** — crescimento, câmbio e dívida.
- **[P0] Crise dos gilts e fundos LDI no Reino Unido durante o governo Liz Truss (2022)** — alavancagem e intervenção do BoE.
- **[P1] Fim dos juros negativos e normalização do BCE (2022–2024)** — spreads soberanos e bancos.
- **[P1] Controle da curva de juros e ajustes do BoJ (2016–2024)** — iene, carry trade e JGBs.
- **[P0] Alta de juros do BoJ e reversão do carry trade global (julho–agosto de 2024)** — iene, Nikkei, volatilidade e desalavancagem.
- **[P1] Início do ciclo de cortes do Fed em 2024** — dólar, curvas e reprecificação de emergentes.
- **[P1] Divergência monetária entre Fed, BCE, BoJ e emergentes (2024–2026)** — câmbio e fluxos globais.
- **[P1] Revisão das regras fiscais da União Europeia (2024)** — trajetórias de dívida e investimento.
- **[P1] Expansão fiscal e de defesa na Europa após mudanças geopolíticas (2025–2026)** — dívida, indústria e infraestrutura.
- **[P1] Rebaixamento da nota soberana dos EUA pela Moody’s (2025)** — déficit, Treasuries e governança fiscal.
- **[P1] Mudanças na política tarifária dos EUA e instabilidade das expectativas de inflação (2025–2026)** — pass-through e reação monetária.
- **[P0] Choque de energia e inflação decorrente da guerra com o Irã e da crise de Hormuz (2026)** — petróleo, gás, fretes e bancos centrais.

## 8.4 Brasil: política econômica, fiscal, monetária e institucional

### 2000–2010: transição, credibilidade e boom de commodities

- **[P1] Consolidação inicial do tripé macroeconômico (1999–2002)** — metas de inflação, câmbio flutuante e superávit primário.
- **[P0] Eleição de 2002, Carta ao Povo Brasileiro e pico do risco-país** — câmbio, dívida, juros e transição FHC–Lula.
- **[P1] Continuidade macroeconômica e ajuste de 2003** — superávit, Selic, inflação e confiança.
- **[P1] Reforma da Previdência do setor público de 2003** — regras, passivos e sinalização fiscal.
- **[P1] Criação e expansão do Bolsa Família (2003–2006)** — renda, consumo e avaliação fiscal/social.
- **[P0] Escândalo do Mensalão (2005 e julgamento posterior)** — governabilidade, risco político e reação dos ativos.
- **[P1] Liquidação do Banco Santos (2004–2005)** — supervisão, fundos e recuperação de ativos.
- **[P0] Descobertas do pré-sal (2006–2007)** — reservas, Petrobras, conteúdo local e regime regulatório.
- **[P1] Programa de Aceleração do Crescimento, PAC (2007)** — infraestrutura, execução e investimento público.
- **[P0] Concessão do grau de investimento ao Brasil (2008)** — spreads, fluxos e composição do investidor.
- **[P0] Resposta brasileira à crise global de 2008–2009** — compulsórios, reservas, crédito público, IPI e BNDES.
- **[P1] Expansão dos aportes do Tesouro ao BNDES (2009–2014)** — subsídio implícito, dívida bruta e investimento.
- **[P1] IOF sobre fluxos e debate da “guerra cambial” (2009–2011)** — apreciação do real e controles de capital.
- **[P0] Capitalização da Petrobras e cessão onerosa (2010)** — diluição, reservas, governo e mercado de capitais.

### 2011–2018: intervenção, recessão e reformas

- **[P0] Nova Matriz Econômica (2011–2014)** — juros, crédito direcionado, câmbio, subsídios e deterioração fiscal.
- **[P0] MP 579 e renovação das concessões elétricas (2012–2013)** — tarifas, Eletrobras, geradoras e segurança regulatória.
- **[P1] Desonerações tributárias e da folha em larga escala (2011–2014)** — custo fiscal e emprego.
- **[P1] Controle de preços de combustíveis e defasagem da Petrobras (2011–2014)** — inflação, caixa e endividamento.
- **[P0] Protestos de junho de 2013** — confiança, mobilidade urbana, gasto público e risco político.
- **[P1] Rebaixamento da perspectiva e deterioração fiscal de 2013–2014** — curva de juros e dívida.
- **[P0] Eleição presidencial de 2014 e volatilidade dos ativos estatais** — pesquisas, probabilidades e risco de modelo.
- **[P0] Recessão brasileira de 2014–2016** — investimento, emprego, crédito e queda de arrecadação.
- **[P0] “Pedaladas fiscais”, revisão de contas públicas e crise de credibilidade estatística/fiscal** — resultado primário e governança orçamentária.
- **[P0] Perda do grau de investimento do Brasil (2015–2016)** — mandato de fundos, spreads e custo de capital.
- **[P0] Processo de impeachment de Dilma Rousseff (2015–2016)** — probabilidade política, câmbio, bolsa e risco-país.
- **[P1] Mudança de equipe econômica e agenda de reformas no governo Temer (2016)** — expectativas e ativos domésticos.
- **[P0] Emenda Constitucional do Teto de Gastos (2016)** — regra fiscal, expectativas e rigidez orçamentária.
- **[P0] Joesley Day (18 de maio de 2017)** — gravação, circuit breaker, câmbio, DI e investigação de operações.
- **[P1] Reforma trabalhista de 2017** — contratos, emprego, litígios e produtividade.
- **[P1] TLP e mudança no crédito do BNDES (2017–2018)** — subsídios e mercado de capitais.
- **[P0] Greve dos caminhoneiros (maio de 2018)** — desabastecimento, PIB, diesel, subsídios e Petrobras.
- **[P1] Crise cambial de emergentes e intervenções do BCB em 2018** — swaps, reservas e eleição.
- **[P1] Eleição de Jair Bolsonaro (2018)** — agenda de reformas, estatais e prêmio de risco.

### 2019–2022: reformas, pandemia e exceções fiscais

- **[P0] Reforma da Previdência de 2019** — economia fiscal estimada, transição e curva longa.
- **[P1] Lei da Liberdade Econômica (2019)** — ambiente regulatório e formalização.
- **[P1] Marco Legal do Saneamento (2020)** — concessões, estatais e investimento.
- **[P0] Saída de Sergio Moro do Ministério da Justiça (abril de 2020)** — crise política e reação de câmbio, bolsa e juros.
- **[P0] Estado de calamidade, Orçamento de Guerra e auxílio emergencial (2020)** — renda, déficit, dívida e atividade.
- **[P1] Transferências, Pronampe e programas de crédito da pandemia** — garantias e risco fiscal.
- **[P1] Autonomia formal do Banco Central (2021)** — mandatos, governança e credibilidade.
- **[P0] Troca no comando da Petrobras em fevereiro de 2021** — interferência percebida, valor de mercado e política de preços.
- **[P1] Privatização da Eletrobras (processo 2021–2022)** — governança, diluição e desenho de capital.
- **[P0] PEC dos Precatórios (2021)** — teto, parcelamento, Auxílio Brasil e curva de juros.
- **[P1] Ciclo de alta da Selic de 2021–2022** — inflação, crédito, atividade e dívida.
- **[P0] Redução de tributos sobre combustíveis, teto de ICMS e benefícios eleitorais de 2022** — inflação, estados e regra fiscal.
- **[P1] Novas trocas na presidência da Petrobras em 2022** — governança e política de combustíveis.
- **[P0] Eleição presidencial de 2022** — pesquisas, estatais, câmbio e transição.
- **[P0] PEC da Transição de 2022** — Bolsa Família, teto de gastos e expectativas fiscais.

### 2023–13 de julho de 2026: novo regime fiscal e tensões institucionais

- **[P0] Ataques às sedes dos Três Poderes em 8 de janeiro de 2023** — risco institucional e abertura dos mercados.
- **[P0] Confronto retórico entre governo Lula e Banco Central (2023–2024)** — expectativas, autonomia e curva de juros.
- **[P0] Novo Arcabouço Fiscal, Lei Complementar 200/2023** — bandas, limite de despesa, contingenciamento e credibilidade.
- **[P1] Mudança da política de preços da Petrobras (2023)** — paridade de importação, margens, inflação e governança.
- **[P0] Reforma tributária do consumo, EC 132/2023, e regulamentação posterior** — CBS, IBS, transição, setores e federalismo.
- **[P1] Remessa Conforme e tributação de compras internacionais (2023–2024)** — varejo, plataformas, arrecadação e consumidor.
- **[P1] Apagões prolongados na Região Metropolitana de São Paulo e crise da concessão Enel (2023–2024)** — qualidade, indenizações e regulação.
- **[P1] Disputa sobre desoneração da folha entre Executivo, Congresso e STF (2023–2024)** — compensação e segurança jurídica.
- **[P0] Retenção de dividendos extraordinários da Petrobras (março de 2024)** — governança, capex e reação de mercado.
- **[P1] Pressões políticas e sucessão na Vale (2024)** — governança de empresa privatizada e percepção de interferência.
- **[P1] Decisões do STF sobre a “Revisão da Vida Toda” (2024–2025)** — passivo previdenciário e estimativas divergentes.
- **[P0] Exceções fiscais e pacote de reconstrução do Rio Grande do Sul (2024)** — crédito extraordinário, dívida estadual e garantias.
- **[P1] Paralisação e retomada gradual de Porto Alegre, indústria e logística gaúcha (2024)** — atividade regional e arrecadação.
- **[P1] Emendas de relator RP9, emendas Pix e decisões do STF sobre transparência (2020–2026)** — governança orçamentária e execução.
- **[P0] Pacote de revisão de gastos e mudança no abono, BPC e salário mínimo anunciado no fim de 2024** — economia projetada e reação do câmbio/juros.
- **[P0] Depreciação do real e intervenções cambiais do BCB no fim de 2024** — leilões à vista, linha e swaps; separar cada instrumento.
- **[P0] Transição de Roberto Campos Neto para Gabriel Galípolo na presidência do BCB (2024–2025)** — autonomia, comunicação e teste de credibilidade.
- **[P0] Ciclo de alta da Selic de 2024–2025 e manutenção em 15% no início de 2026** — expectativas, câmbio e atividade.
- **[P1] Regulamentação da reforma tributária e cronograma de implementação (2024–2026)** — sistemas, créditos e transição federativa.
- **[P0] Disputa do IOF entre Executivo, Congresso e STF (2025)** — compensação fiscal, legalidade e precificação da dívida.
- **[P1] MP 1.303/2025 e debate sobre tributação de aplicações e compensações fiscais** — arrecadação, instrumentos isentos e mercado.
- **[P0] Tarifa extraordinária dos EUA sobre produtos brasileiros e Plano Brasil Soberano (2025)** — exportações, crédito e resposta fiscal.
- **[P1] COP30 em Belém (2025)** — financiamento climático, infraestrutura amazônica e compromissos.
- **[P0] Liquidação extrajudicial do Banco Master e regimes no conglomerado (novembro de 2025)** — estabilidade financeira, FGC e crédito; verbete canônico no capítulo bancário.
- **[P0] Operação Sem Desconto e ressarcimento de beneficiários do INSS (2025–2026)** — governança, custo público e investigação; verbete canônico no capítulo de fraudes.
- **[P0] Início dos cortes de Selic em abril e junho de 2026, chegando a 14,25%** — atividade, expectativas e choque de petróleo.
- **[P1] Revisão de gastos obrigatórios e pente-fino de benefícios (2025–2026)** — economia efetiva versus projetada e efeitos distributivos.
- **[P1] Preparação orçamentária e volatilidade pré-eleitoral de 2026 até 13 de julho** — separar medidas aprovadas de propostas e rumores.

## 8.5 Geopolítica, guerras, terrorismo, sanções e segurança econômica

### Terrorismo e guerras do início do século

- **[P0] Atentados de 11 de setembro de 2001** — fechamento de Wall Street, aviação, seguros, defesa, petróleo e liquidez.
- **[P1] Invocação do Artigo 5º da OTAN e invasão do Afeganistão (2001)** — gastos militares, reconstrução e risco regional.
- **[P0] Invasão do Iraque (2003)** — petróleo, dólar, defesa, custo fiscal e reconstrução.
- **[P2] Atentados de Madri (2004) e Londres (2005)** — transporte, turismo, seguros e resposta de mercado.
- **[P1] Guerra do Líbano entre Israel e Hezbollah (2006)** — risco regional e petróleo.
- **[P1] Primeiro teste nuclear norte-coreano (2006) e ciclos posteriores de tensão** — defesa, Coreia do Sul, Japão e ativos de refúgio.
- **[P1] Guerra Rússia–Geórgia (2008)** — energia, OTAN e precedente pós-soviético.

### Primavera Árabe, Síria e reconfiguração do Oriente Médio

- **[P0] Primavera Árabe (2010–2012)** — petróleo, alimentos, turismo, dívida e mudança de regimes.
- **[P1] Revolução tunisiana e queda de Ben Ali (2011)** — gatilho regional e economia do turismo.
- **[P1] Revolução egípcia e queda de Mubarak (2011)** — Canal de Suez, gás e turismo.
- **[P1] Guerra civil e intervenção internacional na Líbia (2011)** — oferta de petróleo e fragmentação estatal.
- **[P0] Guerra civil síria (2011 em diante)** — refugiados, sanções, energia e intervenção externa.
- **[P1] Ascensão territorial do Estado Islâmico (2014–2017)** — segurança, petróleo ilícito e gasto militar.
- **[P1] Intervenção militar russa na Síria (2015)** — poder regional e relações energéticas.
- **[P1] Acordo nuclear com o Irã, JCPOA (2015)** — sanções, exportações de petróleo e ativos iranianos.
- **[P1] Retirada dos EUA do JCPOA e retomada de sanções (2018)** — petróleo, moedas regionais e empresas europeias.
- **[P1] Bloqueio diplomático e econômico do Catar (2017–2021)** — LNG, aviação e rotas.
- **[P1] Assassinato de Jamal Khashoggi (2018)** — reputação soberana, investimentos e empresas sauditas.
- **[P1] Ataque às instalações de Abqaiq e Khurais na Arábia Saudita (2019)** — capacidade de petróleo e reação intradia.
- **[P0] Morte de Qasem Soleimani em ataque dos EUA (2020)** — prêmio do petróleo e risco de escalada.
- **[P1] Explosão no Porto de Beirute (2020)** — grãos, seguros, porto e crise libanesa.
- **[P1] Retirada dos EUA e tomada de Cabul pelo Talibã (2021)** — ajuda, reservas, bancos e sanções.

### Rússia, Ucrânia e arquitetura de segurança europeia

- **[P0] Euromaidan, queda de Yanukovych e anexação da Crimeia (2013–2014)** — sanções, gás, grãos e risco europeu.
- **[P1] Guerra no Donbas e sanções ocidentais de 2014** — bancos, energia e indústria russa.
- **[P0] Invasão em larga escala da Ucrânia pela Rússia (24 de fevereiro de 2022)** — energia, grãos, fertilizantes, defesa e inflação.
- **[P0] Congelamento de reservas russas e exclusão parcial do SWIFT (2022)** — sanções financeiras e reservas soberanas.
- **[P1] Controles de capital russos, pagamento de gás em rublos e default externo técnico (2022)** — moeda e contratos.
- **[P1] Sabotagem dos gasodutos Nord Stream (2022)** — gás europeu, infraestrutura submarina e seguros.
- **[P1] Adesão da Finlândia e da Suécia à OTAN (2023–2024)** — defesa, fronteiras e gasto público.
- **[P1] Ataques a refinarias, portos e infraestrutura energética no Mar Negro (2022–2026)** — petróleo, fretes e seguro de guerra.
- **[P1] Mudança da postura dos EUA sobre financiamento e negociação da guerra (2025–2026)** — defesa europeia, dívida e prêmio geopolítico.
- **[P1] Continuidade da guerra, sanções secundárias e reorientação do petróleo russo até 13 de julho de 2026** — shadow fleet, descontos e compradores asiáticos.

### Israel, Gaza, Irã e rotas marítimas

- **[P1] Segunda Intifada e ciclos de conflito Israel–Palestina no início dos anos 2000** — turismo, segurança e risco regional.
- **[P1] Conflitos Israel–Gaza de 2008–2009, 2014 e 2021** — precedentes de escalada e reação de ativos.
- **[P0] Ataques do Hamas de 7 de outubro de 2023 e guerra em Gaza** — energia, defesa, turismo e risco humanitário.
- **[P0] Ataques houthis e crise de navegação no Mar Vermelho (2023–2025)** — Suez, fretes, seguros e prazos.
- **[P1] Operação naval internacional de proteção à navegação no Mar Vermelho** — custo de segurança e rerroteamento pelo Cabo.
- **[P0] Troca direta de ataques entre Irã e Israel (abril e outubro de 2024)** — mudança do padrão de confronto e petróleo.
- **[P1] Ampliação do conflito para Líbano e Hezbollah (2024)** — risco regional, aviação e infraestrutura.
- **[P1] Queda do governo Assad na Síria (dezembro de 2024)** — sanções, refugiados, Rússia, Turquia e reconstrução.
- **[P0] Guerra Israel–Irã e participação militar dos EUA em 2025** — instalações nucleares, petróleo e prêmio de risco.
- **[P0] Nova guerra envolvendo EUA, Israel e Irã iniciada em 28 de fevereiro de 2026** — liderança iraniana, infraestrutura e energia.
- **[P0] Bloqueio e disfunção no Estreito de Hormuz em 2026** — petróleo, LNG, navios, seguros, inflação e rotas alternativas.
- **[P0] Retomada de ataques a navios e escalada em Hormuz em julho de 2026** — registrar apenas fatos conhecidos até 13 de julho.
- **[P1] Anúncio norte-americano de novo bloqueio/controle marítimo em 13 de julho de 2026** — não incorporar ações ocorridas em 14 de julho.

### Ásia, Taiwan e competição estratégica

- **[P1] Crises nucleares e de mísseis da Coreia do Norte (2006–2026)** — separar testes de maior impacto em subeventos.
- **[P1] Disputas no Mar do Sul da China e militarização de ilhas (2012–2026)** — comércio, navegação e defesa.
- **[P1] Protestos de Hong Kong (2014 e 2019–2020)** — mercado financeiro, capital e integração com a China.
- **[P1] Lei de Segurança Nacional de Hong Kong (2020)** — listagens, governança e fluxos.
- **[P0] Visita de Nancy Pelosi a Taiwan e exercícios chineses (2022)** — semicondutores, fretes e risco de bloqueio.
- **[P1] Eleições de Taiwan de 2024 e exercícios militares subsequentes** — prêmio geopolítico de chips.
- **[P1] Cercos, exercícios e incursões no Estreito de Taiwan (2025–2026)** — distinguir exercícios documentados de cenários hipotéticos.
- **[P1] Conflitos fronteiriços China–Índia no Himalaia (2020 em diante)** — comércio, defesa e cadeias.
- **[P1] Escalada Índia–Paquistão de 2025** — aviação, mercados locais e risco nuclear.
- **[P1] Golpes militares e guerra civil em Myanmar (2021–2026)** — sanções, gás, mineração e cadeias asiáticas.

### África, América Latina e outras zonas de instabilidade

- **[P1] Guerra civil no Sudão (2023–2026)** — ouro, agricultura, Mar Vermelho e crise humanitária.
- **[P1] Golpes no Sahel, especialmente Níger (2020–2023)** — urânio, ajuda, França e Rússia.
- **[P1] Guerra no leste da República Democrática do Congo e escaladas do M23 (2022–2026)** — cobalto, cobre e risco regional.
- **[P1] Guerra de Nagorno-Karabakh de 2020 e êxodo armênio de 2023** — energia, corredores e Rússia/Turquia.
- **[P1] Crise do Essequibo entre Venezuela e Guiana (2023–2024)** — petróleo offshore, fronteiras e ExxonMobil.
- **[P0] Eleição de Donald Trump em novembro de 2024 e posse em 2025** — dólar, Treasuries, tarifas, defesa e imigração.
- **[P0] Operação dos EUA que capturou Nicolás Maduro em 3 de janeiro de 2026** — soberania, petróleo, sanções e dívida.
- **[P1] Governo interino de Delcy Rodríguez e retomada de relações do FMI com a Venezuela (2026)** — dívida, reservas e reestruturação.
- **[P1] Reabertura parcial e renegociação do setor petrolífero venezuelano em 2026** — PDVSA, credores e sanções.

## 8.6 Comércio, cadeias de suprimento, energia e commodities

### Globalização, China e superciclo

- **[P0] Entrada da China na OMC (2001)** — manufatura, desindustrialização, comércio e commodities.
- **[P0] Superciclo de commodities de 2003–2008** — urbanização chinesa, minério, petróleo, soja e moedas exportadoras.
- **[P1] Ampliação da União Europeia para o Leste (2004 e 2007)** — trabalho, investimento e cadeias.
- **[P1] Crises de gás Rússia–Ucrânia de 2006 e 2009** — segurança energética europeia.
- **[P1] Crise global de alimentos de 2007–2008** — grãos, biocombustíveis, estoques e instabilidade social.
- **[P1] Fracasso da Rodada Doha e avanço de acordos regionais** — fragmentação das regras comerciais.
- **[P1] Restrições chinesas de terras raras e disputa com o Japão (2010)** — dependência mineral e política industrial.
- **[P1] Nova crise de alimentos de 2010–2011** — trigo, milho, clima e Primavera Árabe.
- **[P0] Revolução do shale nos Estados Unidos (2008–2018)** — petróleo, gás, petroquímica e balança externa.
- **[P0] Queda do petróleo de 2014–2016** — shale, OPEP, Petrobras, países exportadores e crédito high yield.
- **[P1] Formação e atuação da OPEP+ a partir de 2016** — coordenação com a Rússia e disciplina de oferta.
- **[P1] Expansão do Canal do Panamá (2016)** — LNG, grãos e tamanho de navios.

### Guerra comercial e política industrial

- **[P0] Guerra comercial EUA–China de 2018–2019** — tarifas, soja, manufatura, câmbio e substituição de fornecedores.
- **[P1] Tarifas dos EUA sobre aço e alumínio, Seção 232 (2018)** — siderurgia brasileira e desvios de comércio.
- **[P1] Sanções e controles sobre Huawei e ZTE (2018–2020)** — 5G, chips e fornecedores.
- **[P1] Acordo “Phase One” EUA–China (2020)** — compras agrícolas, tarifas remanescentes e cumprimento.
- **[P1] Coerção comercial China–Austrália (2020–2023)** — carvão, cevada, vinho e diversificação.
- **[P1] Restrições chinesas a importações e inspeções sanitárias de carnes brasileiras** — frigoríficos, preços e concentração de destino.
- **[P1] Política chinesa de “dual circulation” e autossuficiência tecnológica** — importações e cadeias.
- **[P1] CHIPS and Science Act dos EUA (2022)** — subsídios, fábricas e condições geopolíticas.
- **[P1] Inflation Reduction Act dos EUA (2022)** — veículos elétricos, energia limpa e conteúdo local.
- **[P1] Política industrial europeia, Net-Zero Industry Act e resposta a subsídios externos** — capex e competição.
- **[P1] Mecanismo de Ajuste de Carbono na Fronteira da UE, CBAM** — aço, alumínio, fertilizantes e reporte de carbono.
- **[P1] Regulamento europeu contra desmatamento, EUDR, e adiamentos** — café, soja, carne, rastreabilidade e Brasil.
- **[P1] Proibição indonésia de exportação de minério de níquel e industrialização doméstica** — baterias, aço inox e investimento chinês.
- **[P1] Controles chineses sobre gálio, germânio, grafite e terras raras (2023–2026)** — chips, baterias e defesa.
- **[P1] Tarifas da União Europeia sobre veículos elétricos chineses (2024)** — automóveis, baterias e retaliação.
- **[P1] Conclusão política das negociações UE–Mercosul e processo de ratificação (2024–2026)** — agro, indústria e barreiras ambientais.

### Pandemia e gargalos físicos

- **[P0] Fechamento de fábricas chinesas e ruptura inicial das cadeias na COVID-19 (2020)** — insumos, frete e estoques.
- **[P0] Petróleo WTI futuro em preço negativo em 20 de abril de 2020** — armazenamento, vencimento e microestrutura.
- **[P1] Corte histórico da OPEP+ e disputa Arábia Saudita–Rússia (março–abril de 2020)** — guerra de preços e demanda.
- **[P0] Crise global de contêineres e fretes (2020–2022)** — portos, congestionamento e inflação de bens.
- **[P0] Escassez global de semicondutores (2020–2022)** — automóveis, eletrônicos e concentração asiática.
- **[P0] Encalhe do Ever Given e bloqueio do Canal de Suez (março de 2021)** — fila de navios, seguros e estoque em trânsito.
- **[P1] Fechamentos de portos chineses sob a política zero-COVID (2021–2022)** — Ningbo, Xangai e confiabilidade logística.
- **[P1] Lockdown de Xangai em 2022** — fábricas, porto e demanda chinesa.

### Energia, alimentos e minerais após 2022

- **[P0] Corte de gás russo e crise energética europeia (2022–2023)** — TTF, eletricidade, fertilizantes e indústria.
- **[P1] Corrida europeia por LNG e novos terminais (2022–2025)** — contratos, navios e redirecionamento global.
- **[P0] Choque em trigo, milho, óleo de girassol e fertilizantes após a invasão da Ucrânia** — alimentos e agro brasileiro.
- **[P1] Iniciativa de Grãos do Mar Negro e seu encerramento (2022–2023)** — exportações, seguros e preços.
- **[P1] Restrições de exportação de arroz pela Índia (2023–2024)** — inflação de alimentos e países importadores.
- **[P1] Cortes voluntários da OPEP+ de 2022–2025** — Brent, receitas fiscais e market share.
- **[P1] Explosão de capacidade solar, eólica e de baterias chinesas (2020–2026)** — preços, excesso de capacidade e tarifas.
- **[P1] Crise europeia de energia intensiva e redução de produção de químicos/metais** — BASF, alumínio, vidro e fertilizantes.
- **[P1] Boom e correção dos preços de lítio, níquel e cobalto (2021–2025)** — mineração, baterias e projetos.
- **[P1] Crescimento da demanda elétrica de data centers e IA (2023–2026)** — utilities, gás, nuclear, rede e cobre.
- **[P1] Expansão de capacidade de LNG dos EUA e Catar (2024–2026)** — contratos e segurança energética.

### Tarifas de 2025–2026 e fragmentação do comércio

- **[P0] Tarifas de 25% dos EUA sobre aço e alumínio em 2025** — Brasil, Canadá, México, custos e retaliação.
- **[P0] Tarifas automotivas dos EUA em 2025** — montadoras, autopeças e cadeias norte-americanas.
- **[P0] “Liberation Day” e tarifas recíprocas anunciadas em 2 de abril de 2025** — queda global de bolsas, dólar e Treasuries.
- **[P0] Escalada tarifária EUA–China para níveis superiores a 100% e posterior trégua em 2025** — estoques, portos e volatilidade.
- **[P1] Restrições chinesas de minerais críticos em resposta às tarifas de 2025** — defesa, automóveis e eletrônicos.
- **[P1] Acordos tarifários dos EUA com União Europeia, Japão e outros parceiros em 2025** — taxas efetivas e compromissos.
- **[P0] Tarifa adicional anunciada pelos EUA contra o Brasil em julho de 2025** — café, carne, aço, aviação e diplomacia.
- **[P1] Redirecionamento de exportações brasileiras após as tarifas de 2025** — Índia, América Latina e preços líquidos.
- **[P1] Modificações e exceções às tarifas sobre produtos brasileiros em novembro de 2025** — medir produto a produto.
- **[P1] Acordo econômico e comercial EUA–China de novembro de 2025** — tarifas, compras, minerais e prazo.
- **[P1] Encerramento ou alteração de ações tarifárias norte-americanas em fevereiro de 2026** — base legal e taxa efetiva.
- **[P1] Expansão do BRICS+ (2024–2026)** — comércio, financiamento e coordenação política.
- **[P1] Iniciativas de pagamentos em moedas locais e infraestrutura financeira do BRICS+** — distinguir sistemas reais de propostas de “moeda comum”.

## 8.7 Sistema financeiro, crédito, liquidez e microestrutura de mercado

### Formação e ruptura da crise financeira global

- **[P1] Congelamento de fundos do BNP Paribas em 9 de agosto de 2007** — marco da crise de liquidez hipotecária.
- **[P1] Corrida e nacionalização do Northern Rock (2007–2008)** — depósitos, securitização e garantia estatal.
- **[P0] Colapso e venda do Bear Stearns ao JPMorgan (março de 2008)** — repo, derivativos e apoio do Fed.
- **[P1] Conservatorship de Fannie Mae e Freddie Mac (setembro de 2008)** — hipotecas e passivos públicos.
- **[P0] Falência do Lehman Brothers (15 de setembro de 2008)** — contraparte, funding, ativos globais e recessão.
- **[P0] Resgate da AIG (setembro de 2008)** — CDS, colateral e risco sistêmico.
- **[P0] “Breaking the buck” do Reserve Primary Fund** — corrida em money market funds e papel comercial.
- **[P1] Rejeição inicial do TARP e queda histórica de Wall Street (29 de setembro de 2008)** — política e confiança.
- **[P1] Aprovação e execução do TARP (outubro de 2008)** — capital bancário, custo e recuperação.
- **[P1] Falência do Washington Mutual e venda do Wachovia (2008)** — depósitos e consolidação.
- **[P1] Resgates e nacionalizações bancárias no Reino Unido e Europa (2008–2009)** — RBS, Lloyds, Fortis e Dexia.
- **[P1] Colapso do sistema bancário islandês (2008)** — dívida externa, controles de capital e depositantes estrangeiros.
- **[P0] Perdas com derivativos cambiais de Sadia, Aracruz e outras empresas brasileiras (2008)** — hedge, alavancagem e disclosure.
- **[P1] Fusão Sadia–Perdigão e criação da BRF (2009)** — consequência corporativa da crise cambial.
- **[P1] Testes de estresse bancário dos EUA (2009)** — recapitalização e transparência.

### Falhas de mercado, algoritmos e infraestrutura

- **[P0] Flash Crash de 6 de maio de 2010** — algoritmos, liquidez e cancelamento de negócios.
- **[P1] Falência da MF Global (2011)** — dívida soberana europeia e segregação de recursos de clientes.
- **[P1] Downgrade dos Estados Unidos pela S&P e crise do teto da dívida (2011)** — Treasuries, ações e governança fiscal.
- **[P1] Falha operacional da Knight Capital (2012)** — software, ordens erradas e recapitalização.
- **[P1] Congelamento bancário e bail-in de depósitos no Chipre (2013)** — resolução e fuga de capitais.
- **[P1] Crise grega de 2015, controles de capital e referendo** — bancos, depósitos e risco de saída do euro.
- **[P1] Resolução do Banco Espírito Santo (2014)** — banco bom/banco ruim e credores.
- **[P1] Problemas do Monte dei Paschi e recapitalização italiana** — NPLs e regras europeias.
- **[P1] Flash crash da libra esterlina (outubro de 2016)** — liquidez eletrônica e horário asiático.
- **[P1] Surto de volatilidade “Volmageddon” (fevereiro de 2018)** — produtos short VIX e rebalanceamento.
- **[P1] Estresse do mercado de Treasuries e “dash for cash” (março de 2020)** — margem, dealers e compras do Fed.
- **[P0] Seis acionamentos do circuit breaker da B3 em março de 2020** — contar acionamentos e sessões separadamente.
- **[P1] Disfunção global em fundos imobiliários, crédito e resgates na pandemia** — liquidez e marcação.
- **[P0] Short squeeze da GameStop e ações “meme” (2021)** — varejo, opções, margem e pagamento por fluxo.
- **[P0] Colapso da Archegos Capital Management (2021)** — total return swaps, concentração e perdas bancárias.
- **[P1] Colapso da Greensill Capital (2021)** — supply-chain finance, fundos e seguradoras.
- **[P0] Short squeeze do níquel e suspensão da LME (março de 2022)** — margem, cancelamento de trades e governança da bolsa.
- **[P1] Congelamentos de fundos imobiliários britânicos e outros episódios de iliquidez pós-2022** — descasamento de liquidez.

### Bancos, imóveis e crédito no pós-pandemia

- **[P0] Crise imobiliária da China e default da Evergrande (2021–2024)** — pré-vendas, fornecedores, confiança e governos locais.
- **[P1] Defaults de incorporadoras chinesas e crise da Country Garden (2022–2024)** — offshore bonds e demanda.
- **[P1] Veículos de financiamento de governos locais chineses, LGFVs** — dívida implícita e infraestrutura.
- **[P0] Colapso do Silicon Valley Bank (março de 2023)** — duration, depósitos não segurados e corrida digital.
- **[P0] Fechamento do Signature Bank (março de 2023)** — depósitos, cripto e exceção de risco sistêmico.
- **[P1] Falência e venda do First Republic Bank (2023)** — depósitos de alta renda e consolidação.
- **[P0] Aquisição emergencial do Credit Suisse pelo UBS (março de 2023)** — AT1, garantias e resolução.
- **[P1] Zeragem dos AT1 do Credit Suisse e contágio em títulos bancários** — hierarquia de capital e litígios.
- **[P1] Estresse em bancos regionais dos EUA e imóveis comerciais (2023–2025)** — escritórios, depósitos e provisões.
- **[P1] Crise de imóveis comerciais e bancos na Alemanha, Áustria, Suíça e EUA** — refinanciamento e valuation.
- **[P1] Problemas do New York Community Bancorp (2024)** — CRE, controles internos e capital.
- **[P1] Desalavancagem do carry trade em iene (agosto de 2024)** — margem e correlação entre ativos.
- **[P1] Venda de Treasuries e estresse de base trades durante o choque tarifário de 2025** — hedge funds, margem e liquidez.
- **[P1] Mudanças regulatórias em money market funds, fundos abertos e Treasuries (2014–2026)** — swing pricing, clearing e liquidez.

### Brasil: bancos, crédito privado e regimes especiais

- **[P1] Fraude contábil e socorro ao Banco Panamericano (2010)** — FGC, Caixa e supervisão.
- **[P1] Liquidação do Banco Cruzeiro do Sul (2012)** — consignado, FGC e crédito.
- **[P1] Colapso do Grupo EBX e recuperação da OGX (2013)** — debêntures, garantias e mercado de capitais.
- **[P1] Recessão, inadimplência e desalavancagem bancária no Brasil (2014–2017)** — provisões e crédito.
- **[P1] Crescimento de fintechs, bancos digitais e competição no crédito (2016–2026)** — funding, Pix e regulação.
- **[P1] Estresse de crédito privado durante a pandemia de 2020** — resgates, spreads e atuação do BCB.
- **[P1] Caso IRB Brasil RE e recapitalizações (2020–2024)** — reservas, resseguro e confiança.
- **[P0] Efeito Americanas sobre fundos, debêntures, bancos e fornecedores (2023)** — spreads, provisões e covenants.
- **[P1] Recuperação judicial da Light (2023) e disputa regulatória** — concessão, debêntures e continuidade do serviço.
- **[P1] Recuperação judicial da 123milhas (2023)** — consumidores, cartões, turismo e crédito.
- **[P1] Expansão de CDBs de bancos médios e concentração de risco via FGC (2020–2025)** — incentivos e distribuição.
- **[P0] Tentativa de venda do Banco Master ao BRB e escrutínio regulatório (2025)** — partes relacionadas, governança e risco público.
- **[P0] Liquidação extrajudicial do Banco Master, Banco Master de Investimento, Letsbank e corretora; RAET no Banco Master Múltiplo (18 de novembro de 2025)** — motivo oficial, ativos e captações.
- **[P0] Acionamento do FGC e repercussões da resolução do Conglomerado Master (2025–2026)** — cobertura, prazo, custo e risco moral.
- **[P1] Indisponibilidade de bens e inquéritos administrativos relacionados ao Banco Master (2025–2026)** — estágio e responsabilidades.
- **[P1] Deterioração de inadimplência e cautela do Comef em 2026** — famílias, empresas e concessão de crédito.

## 8.8 Fraudes, corrupção, falhas de governança e auditoria

### Escândalos corporativos globais

- **[P0] Fraude da Enron e colapso da Arthur Andersen (2001–2002)** — SPEs, auditoria e Sarbanes–Oxley.
- **[P0] Fraude da WorldCom (2002)** — capitalização indevida de despesas e controles internos.
- **[P1] Escândalo da Tyco (2002)** — remuneração, apropriação e conselho.
- **[P1] Fraude da Parmalat (2003)** — caixa inexistente, bancos e auditoria.
- **[P1] Escândalo da Ahold (2003)** — consolidação, rebates e governança.
- **[P1] Escândalo de subornos da Siemens (2006–2008)** — FCPA, multas e compliance global.
- **[P0] Esquema Ponzi de Bernard Madoff (revelado em 2008)** — custódia, due diligence e restituições.
- **[P1] Fraude da Satyam na Índia (2009)** — caixa, auditoria e outsourcing.
- **[P1] Escândalo contábil da Olympus (2011)** — perdas ocultadas e governança japonesa.
- **[P0] Manipulação da Libor (investigações e acordos 2012 em diante)** — benchmarks, multas e transição para taxas livres de risco.
- **[P1] Manipulação de benchmarks cambiais, caso “Forex Fixing”** — conduta de traders e multas.
- **[P1] Fraude contábil da Toshiba (2015)** — pressão por metas e supervisão.
- **[P0] Dieselgate da Volkswagen (2015)** — emissões, multas, reputação e transição automotiva.
- **[P1] Contas falsas do Wells Fargo (2016)** — incentivos comerciais e proteção do consumidor.
- **[P1] Escândalo 1MDB (2015–2020)** — títulos, bancos, lavagem e recuperação de ativos.
- **[P1] Panama Papers (2016)** — offshore, beneficiário final e cooperação fiscal.
- **[P1] Paradise Papers (2017) e Pandora Papers (2021)** — planejamento tributário, opacidade e exposição reputacional.
- **[P1] Colapso da Steinhoff (2017)** — contabilidade, varejo e investidores sul-africanos/europeus.
- **[P1] Falência da Carillion (2018)** — contratos públicos, pensões e papel das auditorias.
- **[P1] Escândalo de lavagem de dinheiro do Danske Bank (2018)** — controles AML e multas.
- **[P1] Prisão e fuga de Carlos Ghosn; crise de governança Nissan–Renault (2018–2020)** — aliança e jurisdição.
- **[P0] Acidentes do Boeing 737 MAX e falhas de supervisão (2018–2024)** — segurança, certificação, caixa e fornecedores.
- **[P1] Theranos e condenações (2018–2022)** — venture capital, diligência e governança de empresas fechadas.
- **[P0] Fraude da Wirecard (2020)** — caixa inexistente, BaFin, auditoria e reputação alemã.
- **[P1] Fraude contábil da Luckin Coffee (2020)** — listagens chinesas nos EUA e auditoria.
- **[P1] Caso Nikola e alegações de tecnologia (2020–2022)** — SPACs, disclosure e vendas a descoberto.
- **[P1] Escândalo Cum-Ex e arbitragem tributária europeia** — bancos, impostos e processos.
- **[P1] Purdue Pharma e litígios da crise de opioides** — responsabilidade, falência e acordos.
- **[P1] Títulos “tuna bonds” de Moçambique e Credit Suisse** — dívida oculta, suborno e resolução.
- **[P1] Relatórios da Hindenburg sobre Adani e reação do grupo (2023–2024)** — short selling, free float e regulação indiana.
- **[P1] Falhas de segurança e governança da Boeing após o incidente da Alaska Airlines (2024)** — produção, FAA e fornecedores.

### Brasil: corrupção, contabilidade e falhas de controles

- **[P1] Caso Banco Marka e FonteCindam, com desdobramentos no início dos anos 2000** — câmbio, socorro e responsabilização.
- **[P1] Escândalos de governança do Banco Santos (2004–2005)** — partes relacionadas, arte e liquidação.
- **[P0] Mensalão: investigação, julgamento e efeitos institucionais (2005–2014)** — separar fatos políticos de impacto de mercado.
- **[P1] Máfia das Sanguessugas e outros casos de compras públicas (2006)** — emendas e controle.
- **[P1] Operação Satiagraha e controvérsias judiciais (2008–2011)** — bancos, devido processo e nulidades.
- **[P1] Fraude do Banco Panamericano (2010)** — cessões de carteira duplicadas e falhas de auditoria.
- **[P0] Operação Lava Jato (2014–2021)** — corrupção, construção, óleo e gás, emprego, leniência e decisões posteriores.
- **[P0] Esquema de corrupção na Petrobras e maiores baixas contábeis relacionadas** — fornecedores, dívida e governança.
- **[P0] Odebrecht/Novonor, acordo de leniência e repercussão internacional** — financiamento de obras e compliance.
- **[P1] Operação Zelotes (2015)** — CARF, empresas e contencioso tributário.
- **[P1] Fundos de pensão e Operação Greenfield (2016 em diante)** — investimentos, déficits e responsabilização.
- **[P0] Operações da J&F em torno do Joesley Day e processos por insider trading/manipulação** — cronologia da informação e sanções.
- **[P1] Colapso do Grupo EBX e condenações de Eike Batista** — disclosure, partes relacionadas e confiança.
- **[P1] Trincas e afundamento do solo ligados à mineração da Braskem em Maceió (2018–2026)** — provisões, acordos, moradia e municípios.
- **[P0] Caso IRB Brasil RE: informações incorretas, reservas e processos (2020–2024)** — CVM, recapitalização e auditoria.
- **[P1] Inconsistências contábeis da CVC e republicação de balanços (2020 em diante)** — controles, auditoria e dívida.
- **[P1] Fraudes e pirâmides de criptoativos no Brasil, incluindo GAS Consultoria, Atlas Quantum e Braiscompany** — custódia, promessas e recuperação.
- **[P0] Inconsistências contábeis da Americanas reveladas em janeiro de 2023** — risco sacado, governança e recuperação judicial.
- **[P0] Investigações, acordos e plano de recuperação da Americanas (2023–2026)** — separar alegações, confissões, decisões e valores.
- **[P1] Crise da 123milhas e venda de passagens flexíveis (2023)** — consumidor, crédito e recuperação.
- **[P1] Crises de Hurb e empresas de turismo digital (2023–2025)** — pré-pagamento, reputação e fiscalização.
- **[P0] Operação Sem Desconto sobre descontos associativos indevidos no INSS (deflagrada em abril de 2025)** — investigação, entidades e controles.
- **[P0] Suspensão dos descontos e acordos de ressarcimento do INSS (2025–2026)** — beneficiários, execução e custo.
- **[P1] Desdobramentos criminais e administrativos da Operação Sem Desconto até 13 de julho de 2026** — não antecipar culpa.

### Epstein e compliance financeiro

- **[P1] Relações financeiras de Jeffrey Epstein e falhas de compliance bancário** — contas, alertas, relacionamento e governança.
- **[P1] Acordos civis do JPMorgan e Deutsche Bank relacionados a vítimas de Epstein (2023)** — valores, alegações e ausência de admissão quando aplicável.
- **[P1] Caso Jes Staley, Barclays e reguladores britânicos** — declarações, processo e estágio recursal.
- **[P1] Consequências de governança para Leon Black e Apollo Global Management** — investigação independente, pagamentos e saída executiva.
- **[P2] Repercussões reputacionais sobre universidades, fundações e gestores** — apenas efeitos documentados; não presumir “saídas massivas ESG”.

### Auditores, gatekeepers e lições transversais

- **[P0] Sarbanes–Oxley e criação do PCAOB (2002)** — certificação, controles e independência.
- **[P1] Rotação, independência e serviços não auditáveis após grandes fraudes** — EUA, UE e Brasil.
- **[P1] Falhas e sanções de PwC, KPMG, EY e Deloitte em casos específicos** — criar subeventos, sem generalização indevida.
- **[P1] Papel de bancos, agências de rating, escritórios e custodiantes como gatekeepers** — conflitos e deveres.
- **[P1] Whistleblowers, canais de denúncia e recompensas regulatórias** — SEC, CFTC e legislação brasileira.
- **[P1] Beneficiário final, AML/KYC e expansão de sanções financeiras (2001–2026)** — custo de compliance e exclusão financeira.

## 8.9 Tecnologia, telecomunicações, cibersegurança e inteligência artificial

### Internet, plataformas e telecomunicações

- **[P1] Preparação global para o bug do milênio, Y2K (1998–2000)** — gasto de TI, risco operacional e legado de sistemas.
- **[P0] Estouro da bolha das pontocom (2000–2002)** — Nasdaq, venture capital, telecom e empresas sem lucro.
- **[P1] Leilão de licenças 3G europeias e endividamento das telecoms (2000–2002)** — capex e consolidação.
- **[P1] Crise das “teles” brasileiras após privatização e bolha global** — dívida em dólar, competição e reestruturação.
- **[P1] Expansão da banda larga e do comércio eletrônico (2000–2010)** — produtividade, varejo e publicidade.
- **[P1] IPO do Google (2004) e ascensão da publicidade digital** — plataformas e concentração.
- **[P1] Lançamento do iPhone e economia de aplicativos (2007–2012)** — semicondutores, telecom e modelos de negócio.
- **[P1] Computação em nuvem e ascensão de AWS, Azure e Google Cloud** — capex, software e concentração de infraestrutura.
- **[P1] IPO do Facebook/Meta (2012)** — plataformas, dados e publicidade.
- **[P1] Economia de plataformas, Uber/Airbnb e conflitos regulatórios (2010–2020)** — trabalho, mobilidade e ativos urbanos.
- **[P1] Consolidação das Big Techs e investigações antitruste (2017–2026)** — multas, aquisições e regras de plataforma.
- **[P1] GDPR europeu (2018)** — privacidade, compliance e publicidade.
- **[P1] Lei Geral de Proteção de Dados brasileira e entrada em vigor (2018–2021)** — controles, sanções e dados.
- **[P1] Digital Markets Act e Digital Services Act da União Europeia (2022–2024)** — gatekeepers e obrigações.
- **[P1] Suspensão da plataforma X no Brasil e posterior restabelecimento (2024)** — decisões judiciais, multas e plataformas globais.

### Vazamentos, ataques e interrupções operacionais

- **[P1] Ataques cibernéticos à Estônia (2007)** — infraestrutura digital e defesa cibernética.
- **[P1] Stuxnet e sabotagem de infraestrutura nuclear iraniana (2010)** — ciberarma e sistemas industriais.
- **[P1] Revelações de Edward Snowden (2013)** — soberania de dados, nuvem e vigilância.
- **[P0] Ataques WannaCry e NotPetya (2017)** — hospitais, logística, indústria e perdas corporativas.
- **[P1] Vazamento da Equifax (2017)** — dados de crédito, multas e identidade.
- **[P1] Cambridge Analytica e Facebook (2018)** — dados, eleições e regulação.
- **[P1] Ataque à SolarWinds (2020)** — supply chain de software e governo.
- **[P1] Ataque ao Superior Tribunal de Justiça do Brasil (2020)** — continuidade pública e ransomware.
- **[P1] Ataque ao Colonial Pipeline (2021)** — combustíveis, ransomware e infraestrutura crítica.
- **[P1] Ataque cibernético à JBS (2021)** — frigoríficos, produção e resgate.
- **[P1] Vulnerabilidade Log4Shell (2021)** — risco sistêmico de software aberto.
- **[P1] Ataque ao sistema de saúde Change Healthcare (2024)** — pagamentos, farmácias e concentração.
- **[P0] Atualização defeituosa da CrowdStrike e interrupção global de TI (19 de julho de 2024)** — aviação, bancos, hospitais e risco de terceiros.
- **[P1] Ataques a cabos submarinos e infraestrutura de telecomunicações (2022–2026)** — atribuição, redundância e seguro.
- **[P1] Crescimento de fraudes por engenharia social, deepfakes e IA generativa (2023–2026)** — bancos, identidade e compliance.

### Infraestrutura digital e pagamentos no Brasil

- **[P0] Lançamento do Pix (novembro de 2020)** — pagamentos, bancos, adquirência e inclusão.
- **[P1] Open Banking/Open Finance no Brasil (2021–2026)** — portabilidade de dados e competição.
- **[P1] Leilão do 5G no Brasil (2021)** — espectro, capex e obrigações regionais.
- **[P1] Vazamentos de chaves Pix e incidentes reportados pelo BCB** — governança, notificação e ausência/presença de perda financeira.
- **[P1] Limites, mecanismos antifraude e devolução no Pix** — resposta regulatória a sequestros e golpes.
- **[P1] Projeto Drex e pilotos de moeda/tokenização do BCB (2023–2026)** — privacidade, contratos e infraestrutura.

### Inteligência artificial e semicondutores

- **[P1] Avanços de deep learning e aceleração por GPUs (2012–2020)** — Nvidia, data centers e pesquisa.
- **[P0] Lançamento público do ChatGPT (novembro de 2022)** — adoção, software e reprecificação de IA.
- **[P0] Rali de semicondutores e megacaps ligado à IA (2023–2026)** — Nvidia, TSMC, memória e concentração de índices.
- **[P1] Controles dos EUA sobre exportação de chips avançados para a China (2022–2026)** — Nvidia, ASML, foundries e evasão.
- **[P1] Resposta chinesa com investimento doméstico em semicondutores** — SMIC, equipamentos e subsídios.
- **[P1] Disputa por máquinas de litografia e restrições neerlandesas/japonesas** — ASML e gargalos.
- **[P1] EU AI Act (2024 e implementação)** — risco, modelos de propósito geral e compliance.
- **[P1] Aumento de capex de data centers e gargalos de energia (2023–2026)** — utilities, turbinas, cobre e rede.
- **[P0] Choque DeepSeek em janeiro de 2025** — custo de treinamento, Nvidia e revisão de premissas.
- **[P1] Disputa global por capacidade de chips e acordos de fornecimento de IA em 2025–2026** — soberania computacional.
- **[P1] Concentração do S&P 500 e de índices globais em empresas de IA** — contribuição para retorno e risco de fator.
- **[P1] Debates sobre “bolha de IA”** — tratar como hipótese: valuations, lucros, capex e produtividade, sem afirmar colapso.

## 8.10 Saúde pública, demografia, trabalho e choques sociais

### Epidemias e pandemias

- **[P1] Surto de SARS (2002–2004)** — aviação, turismo, Hong Kong e precedente asiático.
- **[P1] Influenza H1N1 (2009)** — farmacêuticas, escolas, saúde e comparação com 2020.
- **[P1] Epidemia de Ebola na África Ocidental (2014–2016)** — mineração, fronteiras, saúde e ajuda.
- **[P1] Epidemia de Zika e microcefalia no Brasil (2015–2016)** — saúde, turismo e Olimpíadas.
- **[P1] Epidemias recorrentes de dengue e recordes brasileiros de 2024–2025** — produtividade, orçamento e vacinas.
- **[P1] Peste suína africana na China (2018–2020)** — carne suína, ração e exportações brasileiras.
- **[P1] Nuvens de gafanhotos no Leste da África e Sul da Ásia (2019–2020)** — alimentos e resposta multilateral.
- **[P1] Influenza aviária H5N1 em aves e mamíferos (2021–2026)** — abates, ovos, leite e vigilância; não declarar pandemia humana sem fonte.

### Episódio COVID-19 e eventos-filhos

- **[P0] Identificação do surto em Wuhan e primeiros alertas internacionais (dezembro de 2019–janeiro de 2020)** — informação e reação inicial.
- **[P0] Lockdown de Wuhan e interrupção industrial chinesa (janeiro de 2020)** — cadeias e transporte.
- **[P0] Declaração de Emergência de Saúde Pública pela OMS (30 de janeiro de 2020)** — marco sanitário.
- **[P0] Disseminação na Itália, Irã e Coreia do Sul (fevereiro de 2020)** — percepção de pandemia.
- **[P0] Declaração de pandemia pela OMS (11 de março de 2020)** — gatilho institucional global.
- **[P0] Crash global de março de 2020** — ações, crédito, dólar, ouro e liquidez.
- **[P0] Circuit breakers da B3 em março de 2020** — evento canônico no capítulo de mercado.
- **[P0] Fechamento de fronteiras e colapso da aviação (2020)** — companhias, aeroportos e turismo.
- **[P0] Medidas de distanciamento e restrições no Brasil (2020–2021)** — federalismo, serviços e emprego.
- **[P0] Colapso sanitário de Manaus e crise de oxigênio (2021)** — logística, saúde e governança.
- **[P0] Desenvolvimento, autorização e início das vacinas (2020–2021)** — farmacêuticas, logística fria e reabertura.
- **[P1] Variantes Alpha, Delta e Ômicron (2020–2022)** — ondas, mobilidade e ativos.
- **[P1] Passaportes sanitários, mandatos e disputas trabalhistas** — regulação e mobilidade.
- **[P1] Reabertura econômica e rotação de ativos (2020–2021)** — valor/crescimento, commodities e serviços.
- **[P1] Excesso de poupança, estímulos e boom de bens duráveis** — demanda e gargalos.
- **[P1] Long COVID, afastamentos e produtividade** — evidência gradual e custo persistente.
- **[P1] Encerramento da emergência global de COVID-19 pela OMS (2023)** — mudança institucional, não “fim” de toda circulação.

### Trabalho, população e consumo

- **[P1] Expansão do trabalho remoto e híbrido (2020–2026)** — escritórios, tecnologia, cidades e produtividade.
- **[P1] “Great Resignation” e escassez de mão de obra em economias avançadas (2021–2022)** — salários e participação.
- **[P1] Envelhecimento populacional e queda da população chinesa (2022 em diante)** — imóveis, poupança e trabalho.
- **[P1] Migração venezuelana e impactos regionais (2015–2026)** — trabalho, remessas e serviços públicos.
- **[P1] Crise de refugiados sírios e europeia (2015–2016)** — orçamento, trabalho e política.
- **[P1] Migração ucraniana após 2022** — trabalho e gasto social europeu.
- **[P1] Ascensão dos medicamentos GLP-1 para obesidade (2023–2026)** — farmacêuticas, alimentos, saúde e seguros.
- **[P1] Crise de custo de vida global de 2022–2024** — energia, alimentos, salários e política.

## 8.11 Criptoativos, stablecoins e finanças digitais

- **[P1] White paper do Bitcoin (2008) e bloco gênese (2009)** — resposta intelectual à crise e escassez digital.
- **[P1] Fechamento do Silk Road (2013)** — uso ilícito, apreensões e percepção regulatória.
- **[P0] Colapso da Mt. Gox (2014)** — custódia, hacks, recuperação e risco de exchange.
- **[P1] Lançamento do Ethereum (2015)** — contratos inteligentes e tokenização.
- **[P0] Boom de ICOs e alta do Bitcoin em 2017** — captação, fraude e euforia.
- **[P1] Fork Bitcoin/Bitcoin Cash e debates de escalabilidade (2017)** — governança descentralizada.
- **[P1] Lançamento de futuros de Bitcoin na CME/Cboe (2017)** — institucionalização e descoberta de preço.
- **[P1] Criptoinverno de 2018** — desalavancagem e fechamento de projetos.
- **[P1] Anúncio e recuo do projeto Libra/Diem da Meta (2019–2022)** — soberania monetária e stablecoins.
- **[P1] Boom de DeFi, NFTs e stablecoins (2020–2021)** — colateral, oráculos e liquidez.
- **[P1] Listagem da Coinbase (2021)** — euforia e exposição acionária.
- **[P1] Proibição/restrição chinesa à mineração e negociação de cripto (2021)** — hash rate e migração.
- **[P1] Bitcoin como moeda de curso legal em El Salvador (2021)** — reservas, dívida e inclusão.
- **[P1] Hacks da Poly Network, Ronin e bridges (2021–2022)** — segurança e risco de contratos.
- **[P1] “The Merge” do Ethereum (2022)** — energia e consenso.
- **[P0] Colapso de Terra/Luna e UST (maio de 2022)** — stablecoin algorítmica e contágio.
- **[P0] Quebras da Three Arrows Capital, Celsius e Voyager (2022)** — empréstimos e alavancagem.
- **[P0] Falência da FTX e Alameda Research (novembro de 2022)** — custódia, partes relacionadas e governança.
- **[P1] Julgamento, condenação e sentença de Sam Bankman-Fried (2023–2024)** — estágio processual e recuperação.
- **[P1] Depeg temporário do USDC durante a crise do SVB (2023)** — reservas e horário bancário.
- **[P1] Acordo da Binance com autoridades dos EUA e saída de Changpeng Zhao (2023)** — AML e sanções.
- **[P1] Regulação MiCA na União Europeia (2023–2026)** — emissores, reservas e prestadores.
- **[P1] Lei brasileira 14.478/2022 e regulamentação de prestadores de ativos virtuais** — competências e transição.
- **[P0] Aprovação de ETFs spot de Bitcoin nos EUA (janeiro de 2024)** — fluxos, custódia e estrutura.
- **[P1] Halving do Bitcoin de abril de 2024** — emissão e economia dos mineradores.
- **[P1] ETFs spot de Ether e expansão de produtos regulados (2024–2025)** — staking, custódia e fluxos.
- **[P1] Mudança da postura regulatória norte-americana sobre cripto em 2025** — ações efetivamente aprovadas, não promessas.
- **[P1] Criação de reserva/estoque estratégico de Bitcoin pelos EUA em 2025** — origem dos ativos e limites legais.
- **[P1] Legislação de stablecoins nos EUA em 2025–2026** — reservas, emissores e bancos.
- **[P1] Crescimento de stablecoins em pagamentos e mercados emergentes (2023–2026)** — dólar digital e controles.
- **[P1] Tokenização de títulos, depósitos e ativos reais (2022–2026)** — pilotos versus escala comercial.

## 8.12 América Latina e outros mercados emergentes

### Argentina

- **[P0] Crise argentina, corralito e default soberano (2001–2002)** — depósitos, câmbio, pobreza e contágio.
- **[P1] Pesificação assimétrica e fim da conversibilidade** — balanços e contratos.
- **[P1] Reestruturações da dívida argentina de 2005 e 2010** — haircuts e holdouts.
- **[P1] Litígio com credores holdouts e default seletivo de 2014** — pari passu e jurisdição.
- **[P1] Fim parcial dos controles e retorno aos mercados sob Mauricio Macri (2015–2017)** — carry trade e dívida.
- **[P0] Crise cambial e acordo recorde com o FMI em 2018** — juros, reservas e recessão.
- **[P1] Eleição de 2019, retorno de controles e reestruturação de 2020** — pesos, títulos e inflação.
- **[P0] Eleição de Javier Milei e choque de estabilização (2023–2024)** — desvalorização, fiscal, inflação e atividade.
- **[P1] Superávit fiscal, desinflação e custos sociais do ajuste argentino (2024–2026)** — dados mensais e metodologia.
- **[P1] Mudanças cambiais, controles, reservas e relação com FMI sob Milei (2024–2026)** — medidas efetivas.
- **[P1] Relação Argentina–Mercosul e abertura comercial (2024–2026)** — propostas versus decisões vigentes.

### Venezuela

- **[P1] Greve e paralisação da PDVSA (2002–2003)** — petróleo, produção e controle estatal.
- **[P1] Nacionalizações e controles de preços/câmbio sob Hugo Chávez (2003–2012)** — investimento e produção.
- **[P0] Colapso do petróleo, monetização e hiperinflação venezuelana (2013–2021)** — moeda, escassez e migração.
- **[P1] Default de títulos soberanos e da PDVSA (2017 em diante)** — credores e ativos externos.
- **[P1] Sanções financeiras e petrolíferas dos EUA (2017–2024)** — produção, descontos e triangulação.
- **[P1] Reconhecimento internacional concorrente de Nicolás Maduro e Juan Guaidó (2019–2022)** — ativos e ouro no exterior.
- **[P0] Eleição contestada de julho de 2024 e repressão subsequente** — sanções, migração e legitimidade.
- **[P0] Captura de Maduro e governo interino em 2026** — verbete canônico no capítulo geopolítico.
- **[P1] Reestruturação potencial de dívida soberana e da PDVSA em 2026** — universo de créditos e sanções.
- **[P1] Terremotos de junho de 2026 e necessidade de reconstrução** — verbete canônico no capítulo geográfico.

### México, Chile, Colômbia, Peru e Equador

- **[P1] Guerra às drogas no México e efeitos econômicos regionais (2006–2026)** — turismo, investimento e segurança.
- **[P1] Reforma energética mexicana de 2013 e reversões sob AMLO** — Pemex e investimento privado.
- **[P1] Cancelamento do aeroporto de Texcoco (2018)** — títulos, confiança e política pública.
- **[P1] Dívida e fragilidade financeira da Pemex (2015–2026)** — apoio soberano e rating.
- **[P1] Nearshoring no México após 2018** — investimento, energia, água e integração USMCA.
- **[P1] Reforma judicial mexicana de 2024 e reação de ativos** — instituições e USMCA.
- **[P1] Protestos no Chile (2019) e processos constitucionais (2020–2023)** — peso, bolsa, pensões e mineração.
- **[P1] Reforma/retirada de pensões chilenas durante a pandemia** — mercado de capitais local.
- **[P1] Protestos na Colômbia e retirada da reforma tributária (2021)** — fiscal, peso e rating.
- **[P1] Eleição de Gustavo Petro e reformas colombianas (2022–2026)** — petróleo, saúde, pensões e fiscal.
- **[P1] Instabilidade presidencial no Peru (2016–2026)** — cobre, sol e investimento.
- **[P1] Default do Equador em 2008 e reestruturações posteriores** — dívida, petróleo e acesso ao mercado.
- **[P1] Crise de segurança e energia no Equador (2023–2025)** — produção, orçamento e atividade.

### Turquia, África, Sul da Ásia e Oriente Médio emergente

- **[P1] Crise bancária e cambial turca de 2001** — FMI, reformas e inflação.
- **[P1] Tentativa de golpe na Turquia (2016)** — lira, turismo e instituições.
- **[P0] Crise da lira turca de 2018** — dívida externa corporativa e sanções.
- **[P1] Política monetária não convencional turca e inflação de 2021–2023** — reservas, depósitos protegidos e câmbio.
- **[P1] Retorno parcial à ortodoxia monetária turca (2023–2026)** — juros, reservas e credibilidade.
- **[P1] Crise energética da Eskom e load shedding na África do Sul (2008–2025)** — mineração, PIB e dívida.
- **[P1] “State capture” sob Jacob Zuma e reformas posteriores** — estatais e governança.
- **[P1] Greylisting da África do Sul pelo FATF e saída posterior** — bancos e compliance.
- **[P1] Demonetização da Índia (2016)** — dinheiro vivo, informalidade e pagamentos digitais.
- **[P1] Implementação do GST na Índia (2017)** — formalização e logística.
- **[P0] Default soberano e crise do Sri Lanka (2022)** — combustível, protestos e reestruturação.
- **[P1] Default do Líbano e colapso bancário (2020 em diante)** — depósitos, câmbio múltiplo e pobreza.
- **[P1] Defaults e reestruturações de Zâmbia e Gana (2020–2025)** — Common Framework e credores chineses.
- **[P1] Crises recorrentes de balanço de pagamentos do Paquistão (2018–2026)** — FMI, energia e moeda.
- **[P1] Desvalorizações e programa do FMI no Egito (2016–2026)** — inflação, Canal de Suez e capital do Golfo.

## 8.13 Eleições, crises constitucionais e choques institucionais globais

- **[P1] Eleição presidencial contestada Bush–Gore nos EUA (2000)** — Suprema Corte, incerteza e transição.
- **[P1] Rejeição do tratado constitucional europeu em França e Países Baixos (2005)** — integração e euro.
- **[P1] Eleição de Barack Obama durante a crise financeira (2008)** — estímulo, bancos e saúde.
- **[P1] Impasses do teto da dívida e shutdowns dos EUA (2011, 2013, 2018–2019, 2023)** — rating, Treasuries e serviços.
- **[P1] Referendo de independência da Escócia (2014)** — libra, bancos e sedes corporativas.
- **[P1] Eleição do Syriza e confronto Grécia–credores (2015)** — depósitos e risco de Grexit.
- **[P0] Eleição de Donald Trump em 2016** — dólar, Treasuries, impostos, regulação e comércio.
- **[P1] Referendo constitucional italiano e crise bancária/política (2016)** — spreads e euro.
- **[P1] Referendo de independência da Catalunha (2017)** — sedes corporativas, turismo e títulos espanhóis.
- **[P1] Protestos dos “coletes amarelos” na França (2018–2019)** — combustíveis, fiscal e consumo.
- **[P1] Crise orçamentária italiana e abertura dos spreads em 2018** — regras europeias e bancos.
- **[P1] Impeachments de Donald Trump (2019 e 2021)** — instituições e reação limitada/condicional dos mercados.
- **[P0] Eleição norte-americana de 2020 e ataque ao Capitólio em 6 de janeiro de 2021** — transição e risco institucional.
- **[P1] Posse de Joe Biden e mudança de política fiscal, climática e regulatória (2021)** — estímulos e setores.
- **[P1] Centralização política e remoção de limites de mandato na China (2018–2022)** — risco de governança e política econômica.
- **[P1] Congresso do Partido Comunista Chinês de 2022 e composição da liderança** — prioridades econômicas e reação de Hong Kong.
- **[P1] Terceiro mandato de Narendra Modi e eleições indianas de 2024** — coalizão, infraestrutura e ativos.
- **[P1] Eleições europeias e eleição antecipada na França em 2024** — spreads franceses e risco fiscal.
- **[P1] Decisão do Tribunal Constitucional alemão sobre fundos extrabudgetários (2023)** — orçamento e investimento.
- **[P1] Queda da coalizão alemã e mudança de política fiscal/defesa (2024–2025)** — dívida e indústria.
- **[P1] ANC perde maioria na África do Sul e forma governo de unidade (2024)** — reformas, Eskom e rand.
- **[P1] Eleição de Claudia Sheinbaum no México (2024)** — continuidade, reforma judicial e peso.
- **[P0] Eleição e retorno de Trump à Casa Branca (2024–2025)** — verbete canônico no capítulo geopolítico.
- **[P1] Uso de poderes emergenciais e disputas judiciais sobre tarifas dos EUA (2025–2026)** — IEEPA, Congresso e Suprema Corte.
- **[P1] Expansão de gastos de defesa da OTAN em 2025–2026** — orçamento, indústria e dívida.
- **[P1] Crises de coalizão e ascensão de partidos antissistema na Europa (2015–2026)** — registrar eventos nacionais, não generalizações.

## 8.14 Acidentes industriais, falhas de infraestrutura e desastres tecnológicos

- **[P1] Acidente nuclear de Three Mile Island (1979, precedente)** — regulação e custo da energia nuclear.
- **[P1] Desastre químico de Bhopal (1984, precedente)** — responsabilidade transnacional e segurança industrial.
- **[P1] Desastre da plataforma Piper Alpha (1988, precedente)** — segurança offshore e seguros.
- **[P1] Derramamento do Exxon Valdez (1989, precedente)** — multas, limpeza e regulação ambiental.
- **[P1] Acidente do ônibus espacial Columbia (2003)** — indústria aeroespacial, contratos e cultura de segurança.
- **[P0] Explosão da plataforma Deepwater Horizon e derramamento no Golfo (2010)** — BP, perfuração, pesca, multas e seguros.
- **[P1] Desabamento do Rana Plaza em Bangladesh (2013)** — moda global, auditoria social e responsabilidade da cadeia.
- **[P1] Descarrilamento e explosão de Lac-Mégantic, Canadá (2013)** — transporte ferroviário de petróleo e seguro.
- **[P1] Explosões no Porto de Tianjin, China (2015)** — automóveis, químicos, logística e fiscalização.
- **[P1] Crise de água contaminada em Flint, Michigan (2014–2019)** — infraestrutura, títulos municipais e saúde.
- **[P1] Colapso da Ponte Morandi em Gênova (2018)** — concessões, Atlantia e manutenção.
- **[P1] Rompimentos de Mariana e Brumadinho** — verbetes canônicos no capítulo geográfico, com tag de falha industrial.
- **[P1] Afundamento do solo em Maceió ligado à mineração de sal-gema** — verbete canônico no capítulo de governança.
- **[P1] Obstrução do Suez pelo Ever Given** — verbete canônico no capítulo logístico.
- **[P1] Descarrilamento químico de East Palestine, Ohio (2023)** — ferrovias, seguros e regulação.
- **[P1] Colapso da Ponte Francis Scott Key em Baltimore (março de 2024)** — porto, automóveis, carvão e responsabilidade marítima.
- **[P1] Falhas de controle de tráfego aéreo e interrupções nacionais relevantes (2006–2026)** — separar eventos com impacto mensurável.
- **[P1] Apagões nacionais ou regionais de grande escala** — Nordeste brasileiro 2011, Índia 2012, Argentina/Uruguai 2019, Texas 2021 e Península Ibérica 2025, cada um como evento independente.
- **[P1] Acidentes e paralisações em minas estratégicas** — cobre, minério, carvão e metais críticos, quando houver impacto de oferta.

---

# 9. FOTOGRAFIA MACRO EM 13 DE JULHO DE 2026

Este capítulo é um snapshot datado, não um evento. Deve ser reconstruído a partir dos últimos dados disponíveis até a âncora, informando a defasagem de cada série. Não se pode misturar fechamento de 13 de julho com indicador mensal divulgado semanas antes sem explicitar a data-base.

## 9.1 Painel brasileiro obrigatório

- Meta Selic, decisão do Copom e orientação do comunicado.
- Curva DI: vértices curtos, intermediários e longos.
- IPCA acumulado, núcleos, serviços, administrados e expectativas Focus.
- USD/BRL: abertura, mínima, máxima, fechamento e PTAX.
- Reservas internacionais, swaps e intervenções recentes; não somar instrumentos diferentes.
- Ibovespa, índice de small caps, IFNC, IMAT, ICON, IEE e UTIL.
- Fluxo estrangeiro acumulado na B3.
- NTN-B, prefixados, inclinação e leilões do Tesouro.
- CDS Brasil de cinco anos e comparação emergente.
- Resultado primário, nominal, dívida bruta, despesas obrigatórias e contingenciamento.
- Cumprimento formal e econômico do Arcabouço Fiscal.
- Balança comercial, conta corrente e investimento direto.
- PIB, IBC-Br, produção industrial, varejo, serviços e desemprego.
- Crédito, inadimplência, spreads e observações do Comef.
- Situação do Banco Master, FGC e regimes especiais.
- Execução do ressarcimento do INSS e provisões/ações de recuperação.
- Estado da reforma tributária e calendário de implementação.
- Risco hidrológico, armazenamento, bandeiras tarifárias e clima.
- Safra, fertilizantes e preços agrícolas relevantes.
- Calendário e regras eleitorais de 2026 já vigentes, sem prever o resultado.

## 9.2 Painel global obrigatório

- Fed funds, curva de Treasuries e Treasury de dez anos.
- DXY, EUR/USD, USD/JPY e principais moedas emergentes.
- S&P 500, Nasdaq, Stoxx 600, Nikkei, Hang Seng e MSCI EM.
- VIX e índices de volatilidade de juros.
- Brent, WTI, gás europeu TTF e LNG.
- Ouro, cobre, minério de ferro, grãos e fertilizantes.
- Situação operacional do Estreito de Hormuz exatamente até a âncora.
- Guerra EUA/Israel–Irã e efeitos documentados em energia e transporte.
- Guerra Rússia–Ucrânia, sanções e fluxos de energia.
- Gaza, Líbano, Síria e Mar Vermelho.
- Tarifas efetivamente vigentes dos EUA, China, UE e Brasil.
- Estado das relações comerciais EUA–China.
- Condições financeiras e projeções mais recentes do FMI, Banco Mundial e OCDE.
- Política monetária de BCE, BoJ, PBoC e principais emergentes.
- Imóveis e crescimento da China.
- Capex de IA, semicondutores e concentração dos índices.
- Bitcoin, Ether, stablecoins e regulação vigente.
- Perdas de catástrofes naturais de 2025 e eventos acumulados de 2026.

## 9.3 Formato do snapshot

Cada linha do painel deve conter:

    indicador | valor | unidade | data-base | horário |
    fonte | variação diária | variação no ano |
    comparação histórica | nota metodológica

## 9.4 Regra de atualização

O snapshot perde validade assim que novos dados são publicados. O RAG deve responder perguntas como “qual é a Selic atual?” consultando fonte viva; a base histórica só deve responder “qual era a Selic na âncora de 13/07/2026?”.

# 10. CORREÇÕES CONCEITUAIS APLICADAS AO GUIA ORIGINAL

| Formulação anterior | Problema | Formulação robusta |
|---|---|---|
| “2000–2026”, mas com eventos de 1975 e 1986 | Escopo inconsistente | Núcleo exaustivo 2000–13/07/2026 e precedentes selecionados 1900–1999 |
| “Um documento JSON de 300–800 páginas” | JSON não tem paginação e um arquivo único é frágil | JSONL particionado, mais documentação Markdown e renderização opcional |
| Coordenadas exatas para todo evento | Impraticável para guerras, secas e políticas | Coordenadas somente para pontos; regiões, bacias ou polígonos para eventos difusos |
| “Impacto instantâneo” sempre disponível | Muitos choques ocorrem com mercado fechado ou evoluem lentamente | Registrar sessão, data de conhecimento e janelas T0/T+1/T+5 |
| “Os seis circuit breakers” como seis dias | Pode confundir acionamentos com sessões | Contar acionamentos, sessões e níveis separadamente |
| “Queima de reservas com swaps” | Swap não reduz reservas brutas como venda à vista | Separar venda spot, linha, recompra e swap cambial |
| “Tarifas beneficiaram o agro brasileiro” | Efeito depende de produto, destino, preço e retaliação | Tratar substituição de comércio como hipótese mensurável |
| “Queda de Maduro reduziu o risco da América Latina” | Conclusão causal ampla e não necessariamente observada | Medir petróleo, dívida, sanções, spreads e risco político antes de concluir |
| “Bolha de IA” como fato | “Bolha” é interpretação | Registrar valuations, lucros, concentração e capex; classificar a tese como contestada |
| “Impacto trilionário” da Revisão da Vida Toda | Pode misturar estimativas, horizontes e cenários | Registrar cada estimativa com autor, data, hipótese e decisão judicial |
| “Fraudes no INSS e créditos consignados” | O episódio central de 2025 trata de descontos associativos indevidos | Separar descontos associativos, consignado, ressarcimento e outras fraudes |
| “Crise de confiança do Banco Master 2023–2025” | Status ficou desatualizado | Incluir tentativa de venda, liquidação extrajudicial, RAET, FGC e investigações até a âncora |
| “Saídas massivas de fundos ESG” ligadas a Epstein | Afirmação exige evidência específica | Limitar a acordos, processos, renúncias e fluxos comprovados |
| “Tempestade de areia bloqueou Suez” | Simplifica causalidade do encalhe | Descrever vento, visibilidade, navegação, encalhe e investigação separadamente |
| “R$ 100 bilhões” para terremoto estrangeiro | Conversão arbitrária e sem data-base | Preservar moeda/estimativa original e informar conversão |
| “Ações do agro subiram; seguradoras derreteram” | Generalização sem janela nem ticker | Listar instrumentos, retorno, benchmark, data e fatores concorrentes |
| “Rombo” e “calote” como nomes canônicos | Linguagem editorial | Usar título jurídico/técnico e manter apelido apenas como alias |

---

# 11. APÊNDICES OBRIGATÓRIOS

## 11.1 Cronologia dos circuit breakers da B3

Criar um registro por acionamento com:

- data e horário;
- nível acionado;
- queda que motivou a interrupção;
- duração;
- horário de reabertura;
- fechamento do pregão;
- evento associado;
- regra vigente naquele momento;
- fonte oficial da B3;
- distinção entre circuit breaker, leilão e interrupção técnica.

Cobrir, no mínimo, episódios ligados à crise asiática, crise russa, desvalorização de 1999, crise de 2008, Joesley Day e março de 2020.

## 11.2 Intervenções cambiais do BCB

Tabela por operação:

    data | instrumento | anunciado | colocado |
    vencimento | taxa | objetivo declarado |
    reservas afetadas? | estoque de swaps |
    USD/BRL antes/depois | fonte

Não somar valor nocional de swap a venda à vista como se fossem a mesma intervenção.

## 11.3 Linha do tempo da Selic e dos ciclos monetários

- decisão por reunião;
- votação;
- comunicado e ata;
- inflação e expectativas disponíveis;
- hiato e atividade;
- USD/BRL;
- surpresa versus consenso;
- início/fim de ciclo;
- taxa real ex ante.

## 11.4 Defaults soberanos e reestruturações

Cobrir Argentina, Rússia, Grécia, Venezuela/PDVSA, Líbano, Zâmbia, Sri Lanka, Gana, Ucrânia e outros casos materiais. Incluir:

- lei aplicável;
- moeda;
- CACs;
- principal e juros;
- haircut de valor presente;
- holdouts;
- FMI e credores oficiais;
- tempo de retorno ao mercado.

## 11.5 Resoluções e resgates bancários

Comparar:

- Northern Rock;
- Bear Stearns;
- Lehman;
- AIG;
- Islândia;
- Chipre;
- Banco Espírito Santo;
- SVB;
- Signature;
- First Republic;
- Credit Suisse;
- Banco Santos;
- Panamericano;
- Cruzeiro do Sul;
- Banco Master.

## 11.6 Legislação criada ou reformada após crises

### Global

- Glass–Steagall e FDIC como precedentes;
- Sarbanes–Oxley e PCAOB;
- Dodd–Frank e Volcker Rule;
- Basel I, II, 2.5, III e finalização de Basel III;
- EMIR, MiFID II, BRRD e regras de bail-in;
- reformas de money market funds;
- GDPR, DMA, DSA e AI Act;
- MiCA e regras de stablecoins;
- CHIPS Act, IRA, CBAM e EUDR.

### Brasil

- Lei de Responsabilidade Fiscal;
- Novo Mercado e reformas de governança;
- Lei Anticorrupção;
- Lei das Estatais;
- reformas da Lei de Recuperação e Falências;
- TLP;
- autonomia do Banco Central;
- LGPD;
- Marco do Saneamento;
- Open Finance e regulação do Pix;
- Teto de Gastos;
- Novo Arcabouço Fiscal;
- reforma tributária do consumo;
- marco legal de criptoativos;
- normas de barragens, mineração e segurança após Mariana/Brumadinho.

Para cada norma: evento motivador, data, alcance, transição, órgão supervisor, efeitos e críticas documentadas.

## 11.7 Gargalos geoeconômicos

Mapa e fichas para:

- Estreito de Hormuz;
- Bab el-Mandeb;
- Canal de Suez;
- Canal do Panamá;
- Estreito de Malaca;
- Bósforo e Dardanelos;
- Mar Negro;
- Estreito de Taiwan;
- portos brasileiros de Santos, Paranaguá, Rio Grande, Itaguaí e Itaqui;
- ferrovias e hidrovias brasileiras;
- cabos submarinos;
- fábricas críticas de semicondutores;
- gasodutos e terminais de LNG.

## 11.8 Sanções e “weaponization of finance”

- congelamento de ativos;
- bloqueio de bancos;
- SDN lists;
- SWIFT;
- controles de exportação;
- sanções secundárias;
- teto de preço do petróleo;
- shadow fleet;
- moedas locais;
- ouro e cripto como vias de contorno;
- custos de compliance e overcompliance.

## 11.9 Catástrofes, seguros e proteção insuficiente

Para cada desastre:

- perda econômica;
- perda segurada;
- taxa de cobertura;
- resseguradoras;
- seguro público;
- títulos catastróficos;
- revisão de prêmio;
- retirada de seguradoras;
- custo de reconstrução;
- adaptação e códigos de construção.

## 11.10 Matriz de exposição das empresas brasileiras

Campos mínimos:

    empresa | ticker | ADR | receita por região |
    moeda de receita | moeda de custo |
    dívida por moeda | commodity |
    dependência logística | risco regulatório |
    seguro | hedge | fonte e data

Essa matriz deve ser datada; exposição corporativa muda a cada balanço.

## 11.11 Glossário expandido

Incluir, no mínimo:

- risco de cauda e cisne negro;
- drawdown, volatilidade realizada e implícita;
- beta, retorno anormal e estudo de evento;
- flight to quality, flight to liquidity e safe haven;
- contágio e sudden stop;
- risco sacado, forfait, factoring e supply-chain finance;
- covenant, waiver, cross-default e acceleration;
- marcação na curva e a mercado;
- duration, convexidade e basis trade;
- repo, haircut e margin call;
- CDS, spread soberano e recovery rate;
- bail-out, bail-in, resolution e good bank/bad bank;
- quantitative easing, tightening e forward guidance;
- fiscal dominance;
- sterilized intervention, swap e linha;
- nearshoring, reshoring e friendshoring;
- terms of trade e pass-through cambial;
- weaponization of the dollar;
- shadow fleet;
- stranded assets;
- protection gap;
- cat bond;
- Emendas Pix, RP9, restos a pagar e crédito extraordinário;
- risco hidrológico, GSF e bandeira tarifária;
- PPI, preço de paridade e crack spread;
- stablecoin, depeg, proof of reserves e bridge;
- data lineage, data vintage e point-in-time data.

---

# 12. PREPARAÇÃO PARA RAG

## 12.1 Estratégia de chunks

Não dividir cegamente por número fixo de caracteres. Usar chunks semânticos:

1. identificação, gatilho e contexto;
2. linha do tempo;
3. impacto de mercado no Brasil;
4. impacto global e commodities;
5. economia real, fiscal e seguros;
6. regulação, investigação e status;
7. lições, precedentes e curiosidades.

Cada chunk deve repetir:

- event_id;
- nome canônico;
- intervalo temporal;
- países;
- categorias;
- entidades centrais;
- cutoff_at.

## 12.2 Metadados de recuperação

- ano, década e duração;
- país e região;
- Brasil afetado: sim/não;
- classes de ativo;
- setores;
- empresas/tickers;
- tipo de choque;
- canais de transmissão;
- severidade;
- prioridade;
- status jurídico;
- confiança;
- necessidade de dados vivos.

## 12.3 Perguntas sintéticas por evento

Gerar 8 a 20 perguntas que o verbete pode responder, por exemplo:

- O que desencadeou o Joesley Day?
- Quantos acionamentos de circuit breaker ocorreram?
- Como o USD/BRL reagiu?
- Quais fatores concorrentes existiam?
- Qual foi o impacto sobre a curva DI?
- Quais processos e sanções se seguiram?
- Que precedente é comparável e por quê?

Não gerar pergunta cuja resposta não esteja sustentada no verbete.

## 12.4 Recuperação híbrida

Combinar:

- busca lexical para nomes, datas e tickers;
- embeddings para mecanismos e paralelos;
- filtros estruturados;
- grafo de relações;
- reranking por prioridade, data e confiança.

## 12.5 Política de frescor

Campos como “atual”, “hoje”, “vigente” ou “presidente” devem acionar consulta viva. O RAG histórico só pode responder com a data explícita: “em 13 de julho de 2026”.

## 12.6 Resposta segura

Se fontes divergirem, o agente deve:

1. informar a divergência;
2. citar as duas estimativas;
3. explicar a data-base;
4. evitar escolher uma sem justificativa.

Se faltarem dados, responder “não há evidência suficiente na base”, em vez de completar por plausibilidade.

---

# 13. FLUXO DE PRODUÇÃO

## Fase 1 — inventário e IDs

- congelar o catálogo;
- atribuir event_id e episode_id;
- deduplicar aliases;
- marcar P0/P1/P2;
- definir relações.

## Fase 2 — pesquisa primária

- coletar documentos oficiais;
- registrar fontes;
- extrair afirmações;
- capturar tabelas e séries;
- preservar data de acesso.

## Fase 3 — mercado

- obter observações T-20 a T+252;
- validar calendário;
- ajustar moeda e benchmark;
- registrar eventos concorrentes;
- calcular retornos de forma reprodutível.

## Fase 4 — economia real e custos

- coletar PIB, produção, emprego, comércio, inflação;
- distinguir projeção contemporânea de realização posterior;
- coletar dano direto, perda econômica, seguro e fiscal.

## Fase 5 — jurídico e regulatório

- atualizar estágio de investigações;
- conferir anulações, recursos, acordos e reversões;
- vincular normas e decisões.

## Fase 6 — redação

- produzir verbete estruturado;
- usar linguagem neutra;
- gerar resumos e perguntas;
- não inserir dados sem claim_id.

## Fase 7 — revisão

- revisão factual;
- revisão quantitativa;
- revisão jurídica;
- revisão de viés;
- validação JSON Schema;
- teste de recuperação.

## Fase 8 — congelamento

- aplicar cutoff;
- remover fatos posteriores;
- gerar checksum;
- publicar changelog;
- registrar versão.

---

# 14. CONTROLES DE QUALIDADE

## 14.1 Checklist factual

- [ ] Gatilho apoiado por fonte primária ou múltiplas fontes confiáveis.
- [ ] Data do evento separada da data da notícia.
- [ ] Horário e fuso corretos.
- [ ] Números têm unidade e data-base.
- [ ] Estimativas revisadas não foram misturadas.
- [ ] Nenhum fato posterior a 13/07/2026.

## 14.2 Checklist de mercado

- [ ] Pregão, feriado e horário conferidos.
- [ ] Abertura, fechamento e intradia não foram confundidos.
- [ ] Retorno em pontos não foi confundido com percentual.
- [ ] Moeda local e dólar estão identificados.
- [ ] Benchmark e fatores concorrentes constam.
- [ ] “Valor de mercado perdido” não foi tratado como custo fiscal.

## 14.3 Checklist jurídico

- [ ] Investigado, denunciado, réu e condenado estão diferenciados.
- [ ] Instância e recursos constam.
- [ ] Acordo não é descrito como condenação.
- [ ] Anulações e arquivamentos foram atualizados.
- [ ] Pessoas não foram associadas por mera proximidade.

## 14.4 Checklist de causalidade

- [ ] Canal de transmissão explícito.
- [ ] Grau causal informado.
- [ ] Choques concorrentes listados.
- [ ] Efeito temporário separado de persistente.
- [ ] Paralelo histórico inclui diferenças.

## 14.5 Checklist de neutralidade

- [ ] Adjetivos editoriais removidos dos campos canônicos.
- [ ] Mesma régua aplicada a governos e partidos diferentes.
- [ ] Custos e benefícios distributivos apresentados.
- [ ] Alegações de todas as partes identificadas como tal.

## 14.6 Checklist técnico

- [ ] JSONL válido linha a linha.
- [ ] IDs únicos.
- [ ] Relações não apontam para registros inexistentes.
- [ ] URLs válidas.
- [ ] Claims têm fontes.
- [ ] Chunks preservam event_id.
- [ ] Datas seguem ISO 8601.
- [ ] Valores numéricos não usam texto no campo numérico.

---

# 15. PROMPT OPERACIONAL PARA PREENCHIMENTO EM LOTES

Usar o texto abaixo como instrução-base para a IA pesquisadora:

> Você está construindo uma base histórica auditável para investidores brasileiros. Trabalhe somente nos event_ids fornecidos neste lote. Obedeça ao cutoff de 13 de julho de 2026, 23h59 BRT. Pesquise fontes primárias primeiro. Não invente horários, cotações, custos, coordenadas ou causalidade. Registre cada afirmação material em claims com source_ids. Separe fato, estimativa, alegação e interpretação. Para dados de mercado, informe sessão, janela, moeda, benchmark e choques concorrentes. Para processos, informe estágio, instância e recursos. Para eventos externos, inclua a camada brasileira. Não faça previsão nem recomendação. Se não houver evidência, use nulo e registre a lacuna. Entregue JSONL válido e um relatório de pendências.

## 15.1 Tamanho de lote recomendado

- 3 a 5 eventos P0;
- 5 a 10 eventos P1;
- 10 a 20 eventos P2;
- nunca misturar eventos com grande sobreposição sem definir primeiro o episódio-pai.

## 15.2 Saída de cada lote

- arquivo JSONL;
- arquivo de fontes;
- observações de mercado;
- relatório de claims sem fonte;
- relatório de divergências;
- log de validação;
- lista de eventos relacionados descobertos.

---

# 16. TESTES DE ACEITAÇÃO

A base só está pronta quando:

1. todos os eventos P0 possuem fontes de nível A ou justificativa explícita;
2. todos os números materiais possuem data-base;
3. todos os processos sensíveis estão atualizados até o cutoff;
4. nenhum evento posterior ao cutoff aparece;
5. consultas por data, país, ativo, setor e empresa retornam os registros corretos;
6. perguntas sobre “impacto no Brasil” recuperam dados brasileiros, não apenas narrativa global;
7. eventos lentos, como seca e inflação, não recebem horário inventado;
8. circuit breakers e intervenções cambiais são contabilizados corretamente;
9. efeitos de mercado não são descritos como causalidade exclusiva sem controle;
10. a base consegue dizer “não há evidência”;
11. uma amostra aleatória de eventos é reproduzível a partir das fontes;
12. o snapshot de 13/07/2026 está inteiramente datado.

---

# 17. NOTAS DE VERIFICAÇÃO PARA 2025–13 DE JULHO DE 2026

Estas referências servem para corrigir o status dos itens recentes do guia. Elas não substituem a pesquisa completa de cada verbete.

- O Banco Central registrou a liquidação extrajudicial de instituições do Conglomerado Master em 18 de novembro de 2025 e informou os motivos prudenciais: [nota do Banco Central](https://www.bcb.gov.br/detalhenoticia/20936/nota).
- O BCB mantém consulta de instituições sob regime de resolução e publicou atos posteriores em 2026: [consulta de regimes especiais](https://www.bcb.gov.br/estabilidadefinanceira/consulta_regesp).
- A Operação Sem Desconto foi deflagrada para apurar descontos associativos não autorizados em benefícios do INSS, com suspensão e ressarcimento posteriores: [CGU](https://www.gov.br/cgu/pt-br/assuntos/noticias/2025/11/cgu-e-policia-federal-deflagram-nova-fase-da-operacao-sem-desconto) e [INSS](https://www.gov.br/inss/pt-br/noticias/noticias/inss-devolve-descontos-indevidos-de-abril-a-partir-desta-segunda-feira-26).
- O Copom reduziu a Selic para 14,25% ao ano em junho de 2026: [comunicados do Copom](https://www.bcb.gov.br/controleinflacao/comunicadoscopom).
- A avaliação macro e os riscos de inflação de junho de 2026 estão no [Relatório de Política Monetária do BCB](https://www.bcb.gov.br/publicacoes/rpm/202606).
- O impacto observado das tarifas norte-americanas sobre as exportações brasileiras e o redirecionamento de mercados foram analisados pelo [BNDES](https://blogdodesenvolvimento.bndes.gov.br/serie/estudos-especiais/Impactos-do-tarifaco-na-balanca-comercial-brasileira/).
- As ordens executivas dos EUA permitem reconstruir a cronologia e as modificações tarifárias: [arquivo de ações presidenciais da Casa Branca](https://www.whitehouse.gov/presidential-actions/executive-orders/?s=tariffs).
- Em julho de 2026, a CIA listava Delcy Rodríguez como presidente interina da Venezuela: [CIA World Leaders](https://www.cia.gov/resources/world-leaders/foreign-governments/venezuela).
- O FMI anunciou a retomada de relações com o governo venezuelano sob a administração interina em abril de 2026: [comunicado do FMI](https://www.imf.org/en/news/articles/2026/04/16/pr26123-venezuela-imf-announces-resumption-of-dealings).
- A crise do Estreito de Hormuz permanecia central em 13 de julho de 2026; qualquer fato de 14 de julho deve ser excluído desta versão: [checagem da AP publicada em 13 de julho](https://apnews.com/article/8df557699c900b29fb33172e6da7f3e9).
- As perdas globais por catástrofes naturais em 2025 foram consolidadas pela [Swiss Re](https://www.swissre.com/institute/research/sigma-research/sigma-2026-01-natcat-2025-wildfire-storm-risk/global-natcat-losses-2025.html).
- O Banco Mundial estimou danos diretos do terremoto de Myanmar em 2025 e seus efeitos macroeconômicos: [Banco Mundial](https://www.worldbank.org/en/news/press-release/2025/06/12/earthquake-compounds-myanmar-s-economic-challenges).

---

# 18. REGRA FINAL

Extensão não substitui rigor. O objetivo não é produzir a maior narrativa possível, mas a maior base **verificável, comparável, atualizável e recuperável** possível. Um campo nulo com uma lacuna documentada é superior a uma estatística plausível sem fonte.
