# Hydra

Pub/sub local entre processos da mesma VM. O Supervisor reinicia o despachante e o Registry preserva assinaturas durante essa recuperação. Mensagens são transitórias. A CLI escript demonstra publicação e recebimento em uma sala dentro do mesmo processo.

## Executar

Requisitos de execução e compilação. Elixir 1.14+ e Erlang/OTP.

Execute os comandos a partir deste diretório.

```sh
mkdir -p .build
mix escript.build
printf 'olá\n' | .build/hydra operacoes
```

## Testar

```sh
mkdir -p .build
mix test
```

Licença [MIT](../LICENSE).
