# Órbita

Organiza dependências em ondas de tarefas executáveis em paralelo, com ordenação alfabética em cada onda. Reporta as tarefas bloqueadas se houver um ciclo.

## Executar

Requisitos no Debian. Go 1.22+. Execute os comandos a partir deste diretório.

```sh
go run -buildvcs=false . < example.json
```

A entrada é um objeto JSON que mapeia cada tarefa à lista de seus pré-requisitos. São aceitas até 10 mil tarefas, 100 mil dependências e 4 MiB de entrada.

## Testar

```sh
go test ./...
```

Licença [MIT](../LICENSE).
