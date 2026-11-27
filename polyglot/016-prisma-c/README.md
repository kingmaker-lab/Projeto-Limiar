# Prisma

Calcula histograma e percentis exatos de imagens PGM ASCII (P2), em fluxo. Aceita até 10 milhões de pixels e valores de até 255. A contagem usa 256 posições de memória.

## Executar

Requisitos no Debian. GCC com C11. Execute os comandos a partir deste diretório.

```sh
mkdir -p .build
cc -std=c11 -O2 histogram.c main.c -o .build/prisma
.build/prisma < example.pgm
```

O exemplo tem quatro pixels, com p50 igual a 20 e p95 igual a 255.

## Testar

```sh
mkdir -p .build
cc -std=c11 -O2 -Wall -Wextra -Werror histogram.c test.c -o .build/test
.build/test
```

Licença [MIT](../LICENSE).

## Benchmark

Compile o binário com `-O2` pelo comando acima. A medição inclui leitura, análise e impressão dos resultados.

```bash
awk 'BEGIN {print "P2\n1000 1000\n255"; for (i=0; i<1000000; i++) print i%256}' > .build/bench.pgm
time .build/prisma < .build/bench.pgm > /dev/null
```
