# Hermes

Fila de leitura HTTP em loopback com até mil mensagens e consulta por cursor. Publicações são serializadas e substituem um snapshot por rename atômico após sincronizar o arquivo. Use um processo por arquivo em disco local. A sincronização do diretório pai fica fora da garantia de recuperação em falha de energia.

## Executar

Requisitos de execução e compilação. Go 1.22+; curl para o exemplo.

Execute os comandos a partir deste diretório.

```sh
mkdir -p .build
go run . -file .build/messages.json
# Em outro terminal
curl -sS -X POST -H 'Content-Type: application/json' -d '{"text":"olá"}' http://127.0.0.1:8080/messages
curl -sS 'http://127.0.0.1:8080/messages?after=0'
```

## Testar

```sh
mkdir -p .build
go test -race ./...
```

Licença [MIT](../LICENSE).
