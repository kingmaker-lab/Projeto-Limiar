# Estudo de rodadas adicionais

## Protocolo

A hipótese é que mais rodadas reduzem o excesso diferencial observado no Ouroboros de oito rodadas. Comparamos prefixos de 8 a 12 rodadas, com quatro chaves sintéticas novas (`6a09e667`, `bb67ae85`, `3c6ef372`, `a54ff53a`) e quatro permutações de controle (sementes 20261131–20261134). As chaves antigas motivaram a pergunta. As novas são constantes públicas fixadas para este ensaio e não representam uma amostra aleatória do espaço de chaves.

A variante **W16-K32-Feistel12-S4-P8-KS1E** estende a recorrência de KS1 aos índices 8–11, com a mesma fórmula para as constantes e o mesmo empacotamento. O prefixo de oito rodadas conserva o comportamento do EXP-008. A variante tem identificador separado, pois acrescentar rodadas também exige subchaves adicionais. A comparação avalia a extensão como um todo.

Para cada chave e prefixo, enumeramos 65.536 entradas para cada uma das 16 diferenças de peso um. Usamos o limite por emparelhamentos descrito na [campanha diferencial](DIFERENCIAL.md), com correção para cinco prefixos, quatro chaves, 16 diferenças de entrada e 65.535 diferenças de saída. A hipótese operacional exige que o prefixo de oito rodadas cruze o limite em pelo menos uma das novas chaves e que o de doze fique abaixo em todas. Os prefixos intermediários ajudam a caracterizar a queda. Os controles comparam a ordem de grandeza dos máximos.

O custo é medido no mesmo processo para 8 e 12 rodadas, com agenda e tabelas de rodada preparadas. A mediana usa cinco repetições, alternando a ordem. A velocidade mede esta implementação e esta máquina. O resultado diferencial se limita ao recorte e às chaves do ensaio.

```sh
python3 -m unittest ouroboros.phase2.test_lab ouroboros.phase2.test_differential ouroboros.phase2.test_rounds ouroboros.phase2.test_suffix ouroboros.phase2.test_variant -v
python3 -m ouroboros.phase2.variant > variante.json
```

## Resultado de 27 de novembro de 2026

O limiar ajustado foi de 20 pares ordenados. A hipótese operacional foi satisfeita nas quatro chaves.

| Chave sintética | 8 rodadas | 9 | 10 | 11 | 12 |
| --- | ---: | ---: | ---: | ---: | ---: |
| `6a09e667` | 60 | 14 | 14 | 14 | 12 |
| `bb67ae85` | 30 | 14 | 14 | 14 | 14 |
| `3c6ef372` | 28 | 16 | 14 | 14 | 14 |
| `a54ff53a` | 54 | 14 | 12 | 14 | 14 |

Os quatro controles tiveram máximos de 14, 12, 14 e 12. A primeira queda abaixo do limiar nas quatro chaves apareceu na nona rodada. A nona é candidata para um ensaio confirmatório em chaves reservadas. O critério desta campanha comparava oito e doze.

No benchmark com tabelas preparadas, a mediana local passou de 611 para 847 ns por bloco, um aumento de cerca de 39%. O ensaio serial levou 15,14 s, com pico de RSS de 18.940 KiB. Os 12 testes passaram. A campanha verificou que as 65.536 saídas da variante de 12 rodadas são distintas em cada uma das quatro chaves.

A variante continua experimental. O espaço de chaves é de 32 bits, o bloco é de 16 bits e ainda faltam uma campanha linear da variante e reprodução independente. Para reproduzir os resultados determinísticos, compare as seções de Feistel e controle do [relatório JSON](results/variant-2026-11-27.json). As medições do benchmark variam por execução.
