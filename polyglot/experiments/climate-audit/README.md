# Auditoria de relatórios climáticos

Gaia gera um relatório mensal determinístico com o ano-base de 2024. Aegis calcula o SHA-256 dos bytes do arquivo. Hermes guarda um evento de referência em um snapshot local. Após reiniciar o Hermes, o roteiro recupera o digest, confirma o relatório original e verifica que uma troca de um byte produz `status=changed` e código de saída 1, embora o JSON continue equivalente.

## Executar no Debian 13

Requer Go 1.22+, Cargo e Rust 1.85+, Python 3.10+, Bash, coreutils, curl, jq e GNU time. O Hermes usa uma porta de loopback escolhida pelo sistema operacional. Após instalar as ferramentas, toda a execução é local.

Execute na raiz do repositório.

```bash
bash polyglot/experiments/climate-audit/run.sh
```

O roteiro usa dados sintéticos de [sample.csv](sample.csv), valida o resultado contra [expected-report.json](expected-report.json) e compara duas execuções byte a byte. O relatório, o snapshot e os binários temporários são removidos ao sair. O mesmo roteiro roda no CI.

## Contrato

O [esquema v1](climate-report-event.v1.schema.json) define o objeto de evento. O Hermes recebe o objeto serializado como string no campo `text` e atribui um ID à mensagem. O período vai do primeiro ao último mês observado, inclusive, com lacunas permitidas. O `report_id` é o identificador lógico do relatório. O digest identifica os bytes daquela versão.

A verificação assume que o digest recuperado do Hermes permanece confiável. O experimento verifica persistência após reiniciar o processo e trabalha com um único publicador em loopback. A integridade do próprio snapshot e a recuperação após perda de energia ficam fora do teste.

## Medição

A saída inclui os tamanhos do relatório e do snapshot em bytes, o tempo e pico de memória dos comandos Gaia e Aegis, e o pico de memória do Hermes após a leitura do snapshot. O tempo do GNU time tem resolução de centésimos de segundo. A compilação fica fora das medições.
