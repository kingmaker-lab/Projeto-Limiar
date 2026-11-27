# Campanha diferencial da Fase II

O piloto mostrou um máximo de 44 pares ordenados no Feistel e 14 no controle aleatório. Esta campanha testa a hipótese de que as permutações obtidas com chaves sintéticas novas apresentam máximos compatíveis com uma permutação uniforme de 16 bits, dentro do recorte de entrada de peso um.

O protocolo fixa quatro chaves (`13579bdf`, `2468ace0`, `31415926`, `27182818`), quatro controles simulados (sementes 20261127 a 20261130) e um nível de 1% para a família de testes. Percorre as 16 diferenças de entrada e considera todas as 65.535 diferenças de saída possíveis. A chave do piloto fica fora da campanha. O script mantém uma tabela e um histograma por vez, usa um único processo e produz JSON sem depender de dados externos.

Para uma diferença de entrada fixa, a permutação transforma os pares disjuntos de entrada em um emparelhamento uniforme dos 65.536 valores de saída. Uma diferença de saída fixa define outro emparelhamento. Em domínio de tamanho N, a chance de pelo menos k pares em comum é limitada por C(N/2,k) dividido por (N−1)(N−3)…(N−2k+1). O numerador conta os subconjuntos de k pares possíveis, e o denominador vem da probabilidade de aparecerem juntos. O script multiplica esse limite por 4 × 16 × 65.535 para controlar as comparações da campanha. Essa correção vale mesmo com dependência entre linhas e chaves. Cada par disjunto equivale a dois pares ordenados na convenção do piloto.

A hipótese é rejeitada se alguma chave cruzar o limiar. Duas ou mais chaves acima do limiar registram repetição na própria campanha. Os controles simulados servem como verificação de sanidade. A reprodução independente exige outra implementação e outra máquina. O teste avalia este recorte diferencial e preserva o Feistel histórico como referência para futuras variantes.

```sh
python3 -m unittest ouroboros.phase2.test_lab ouroboros.phase2.test_differential -v
python3 -m ouroboros.phase2.differential > diferencial.json
```

## Resultado de 27 de novembro de 2026

O limite de 1% para a família de 4.194.240 comparações foi cruzado a partir de 20 pares ordenados. Os máximos das quatro chaves foram 28, 26, 28 e 32. Os quatro controles ficaram em 14, 14, 12 e 14. Entre as chaves do Feistel, o maior limite superior ajustado foi 8,23 × 10⁻⁸. O resultado rejeita a hipótese de permutação uniforme neste recorte e se repete nas quatro chaves da campanha. A abrangência sobre o espaço de chaves e a reprodução independente permanecem em aberto.

A execução local usou 46,13 segundos em um processo, com pico de RSS de 17.848 KiB. Os máximos, as diferenças correspondentes e os resultados por linha e as decisões por chave estão no [relatório JSON](results/differential-2026-11-27.json).
