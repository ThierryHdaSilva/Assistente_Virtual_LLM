# Dicionário de dados

Os registros em `database/events` seguem exatamente o esquema da seção 6 do guia. `record_status` distingue `partially_verified` de `cataloged_pending_research`. Campos vazios indicam ausência de evidência registrada, não ausência do fenômeno histórico.

`database/episodes` usa `episode_id`, nomes canônicos, `event_ids`, `source_ids` e `notes`, pois o guia define episódios conceitualmente, mas não fornece um esquema JSON específico para eles. `database/relations` registra o identificador determinístico, tipos de registros, relação, fontes e notes.
