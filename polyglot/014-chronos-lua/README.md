# Chronos

Motor de missões com donos NPC, progresso e cancelamento. Eventos do mesmo instante seguem ordem de inserção. Transições inválidas são registradas com applied=false.

## Executar

Requisitos de execução e compilação. Lua 5.4.

Execute os comandos a partir deste diretório.

```sh
mkdir -p .build
lua5.4 main.lua
```

## Testar

```sh
mkdir -p .build
lua5.4 test.lua
```

Licença [MIT](../LICENSE).
