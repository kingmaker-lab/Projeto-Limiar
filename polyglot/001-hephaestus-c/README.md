# Hephaestus

Arena linear alinhada a max_align_t, com reset coletivo, pico de uso e contadores cumulativos. Use uma arena por thread. Os ponteiros deixam de ser válidos para uso após reset ou destruição.

## Executar

Requisitos de execução e compilação. C11 e GCC.

Execute os comandos a partir deste diretório.

```sh
mkdir -p .build
cc -std=c11 -O2 -Wall -Wextra -Werror arena.c main.c -o .build/hephaestus
.build/hephaestus
.build/hephaestus --bench
```

## Testar

```sh
mkdir -p .build
cc -std=c11 -O2 -Wall -Wextra -Werror arena.c test.c -o .build/test
.build/test
```

Licença [MIT](../LICENSE).
