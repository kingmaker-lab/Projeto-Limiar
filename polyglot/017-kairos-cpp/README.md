# Kairos

Encontra o conjunto de trabalhos sem sobreposição que maximiza o valor total. Os intervalos são semiabertos. A ordenação e a busca binária dão complexidade O(n log n) e memória O(n).

## Executar

Requisitos no Debian. G++ com C++17. Execute os comandos a partir deste diretório.

```sh
mkdir -p .build
c++ -std=c++17 -O2 schedule.cpp main.cpp -o .build/kairos
.build/kairos < example.txt
```

Cada linha tem ID, início, fim e valor inteiro. O exemplo seleciona first e second e totaliza 12. A entrada aceita até 200 mil trabalhos.

## Testar

```sh
mkdir -p .build
c++ -std=c++17 -O2 -Wall -Wextra -Werror schedule.cpp test.cpp -o .build/test
.build/test
```

Licença [MIT](../LICENSE).

## Benchmark

Compile com `-O2` pelo comando acima. A medição inclui leitura, otimização e impressão da seleção.

```bash
awk 'BEGIN {for (i=0; i<100000; i++) print "job" i, i, i+3, (i%37)+1}' > .build/bench.txt
time .build/kairos < .build/bench.txt > /dev/null
```
