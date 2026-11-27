# Daedalus

Rotinas System V AMD64 de MDC sem sinal, soma modular de vetor e contagem de bits. O cabeçalho descreve a interface C. Passe um vetor válido para contagens positivas. O benchmark executa um milhão de MDCs.

## Executar

Requisitos de execução e compilação. GCC, GNU assembler e x86-64 Linux.

Execute os comandos a partir deste diretório.

```sh
mkdir -p .build
cc -c math.S -o .build/math.o
ar rcs .build/libdaedalus.a .build/math.o
cc -O2 test.c .build/libdaedalus.a -o .build/daedalus
.build/daedalus
.build/daedalus --bench
```

## Testar

```sh
mkdir -p .build
cc -O2 -Wall -Wextra -Werror math.S test.c -o .build/test
.build/test
```

Licença [MIT](../LICENSE).
