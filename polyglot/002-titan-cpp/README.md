# Titan

Simulação 2D de discos com impulso elástico, correção ponderada pela massa e reflexão em paredes. Use passos pequenos para reduzir colisões perdidas por atravessamento. O benchmark mede 100 discos por 1.000 passos com busca quadrática.

## Executar

Requisitos de execução e compilação. C++17 e G++.

Execute os comandos a partir deste diretório.

```sh
mkdir -p .build
c++ -std=c++17 -O2 -Wall -Wextra -Werror simulation.cpp main.cpp -o .build/titan
.build/titan
.build/titan --bench
```

## Testar

```sh
mkdir -p .build
c++ -std=c++17 -O2 -Wall -Wextra -Werror simulation.cpp test.cpp -o .build/test
.build/test
```

Licença [MIT](../LICENSE).
