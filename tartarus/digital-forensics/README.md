# TAR-006 · Hecate

Hecate confere a integridade dos bytes da [amostra sintética](events.jsonl) usando o [SHA-256 de referência](events.sha256). Depois valida os campos e reconstrói a linha do tempo em memória, preservando o arquivo original. Eventos são ordenados por data UTC e, em caso de empate, por identificador.

```sh
make -s -C tartarus run TAR=TAR-006
make -C tartarus validate
```

O resultado esperado tem `integrity_ok: true` e a sequência `hc-001`, `hc-002`, `hc-003`. A suíte também verifica que uma alteração na amostra resulta em `integrity_ok: false`, sem linha do tempo, e código de saída 1 ao chamar a CLI Python diretamente.

Cada registro tem `id` único, `timestamp` no formato `AAAA-MM-DDTHH:MM:SSZ` e `action`. Use o hash da revisão confiável do Git como referência. A comparação verifica integridade em relação a esse valor. A procedência dos eventos depende da confiança na revisão e em quem produziu a amostra.
