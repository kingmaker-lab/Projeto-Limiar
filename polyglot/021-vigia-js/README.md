# Vigia

Agrega registros NDJSON em fluxo, com contagem de requisições, respostas HTTP 5xx e limite superior do p95 por serviço. A estimativa usa faixas fixas de latência e mantém somente as contagens.

## Executar

Requisitos no Debian. Node.js 18+. Execute os comandos a partir deste diretório.

```sh
node main.mjs < example.ndjson
```

A entrada contém service, status e ms por linha. O exemplo tem dois registros e uma resposta 5xx. Aceita até 256 serviços e latências de até 60 segundos.

## Testar

```sh
node test.mjs
```

Licença [MIT](../LICENSE).
