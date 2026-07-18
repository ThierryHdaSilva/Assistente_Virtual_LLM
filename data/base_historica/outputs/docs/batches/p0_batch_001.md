# Lote P0-001

Overlay incremental de três eventos P0 pendentes, aplicado sobre o manifesto existente sem alterar os arquivos-base. A ordem foi: Crash de 1929, Segunda Guerra Mundial e Bretton Woods.

Cada objeto de evento preserva o ID existente e contém somente evidências adicionadas neste lote. Consumidores devem aplicar `overlay_upsert` por `event_id`; não devem concatenar o lote às partições-base sem deduplicação.

Os campos de impacto, custos, causalidade, relações adicionais e camada brasileira continuam pendentes quando não há evidência registrada.
