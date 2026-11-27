# Telemetria

A amostra JSON Lines registra uma alteração de política aceita e outra rejeitada. Cada linha contém um `id` único, a ação `policy_change` e um `outcome` igual a `accepted` ou `rejected`. O resumo contém a contagem de eventos e os identificadores alertados em ordem de leitura. Uma linha inválida ou um identificador duplicado encerra a execução com erro antes de emitir o resumo.

Os eventos representam decisões inventadas. Em relatórios de pesquisa, registre a revisão da amostra, a regra aplicada e o resultado observado.
