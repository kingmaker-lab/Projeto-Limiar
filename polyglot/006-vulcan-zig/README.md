# Vulcan

Armazenamento de chave e valor em snapshot TSV de até 1 MiB. A atualização sincroniza o arquivo e usa substituição atômica. Execute mutações em série para o mesmo arquivo. Chave ausente gera erro e saída diferente de zero.

## Executar

Requisitos de execução e compilação. Zig 0.14.1.

Execute os comandos a partir deste diretório.

```sh
mkdir -p .build
zig build-exe main.zig -O ReleaseSafe -femit-bin=.build/vulcan
.build/vulcan put .build/data mode local
.build/vulcan get .build/data mode
.build/vulcan del .build/data mode
```

## Testar

```sh
mkdir -p .build
zig test store.zig
```

Licença [MIT](../LICENSE).
