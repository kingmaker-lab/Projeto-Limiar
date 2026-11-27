# Ensaio diferencial com diferenças de dois bits

Este ensaio amplia a [confirmação diferencial](CONFIRMACAO.md) para todas as 120 diferenças de entrada com dois bits. Preserva as oito chaves, os oito controles simulados e as configurações de 8, 9 e 12 rodadas. Enumera os 65.536 blocos para cada diferença. Separa os casos com 28 diferenças no byte baixo, 28 no byte alto e 64 distribuídas pelos dois bytes.

O limite familiar de 1% cobre três configurações, oito chaves, 120 diferenças de entrada e 65.535 diferenças de saída não nulas. Os controles usam o mesmo limiar para comparação descritiva. Registramos a diferença de saída com maior contagem de pares ordenados de cada linha. Um empate escolhe a menor diferença de saída. A análise é uma ampliação na mesma seleção de chaves.

Para contar cada par disjunto uma vez, a implementação escolhe o membro cujo bit menos significativo da diferença está zerado. A contagem é dobrada para recuperar a convenção de pares ordenados.

```sh
python3 -m ouroboros.phase2.differential_weight2 > diferencial-peso2.json
```

## Resultados de 27 de novembro de 2026

O corte ajustado foi de 22 pares ordenados em 188.740.800 células. A tabela mostra o maior máximo observado entre as oito chaves ou controles de cada grupo.

| Configuração | Byte baixo | Byte alto | Bits em bytes diferentes | Linhas no limiar ou acima |
| --- | ---: | ---: | ---: | ---: |
| 8 rodadas | 28 | 26 | 18 | 5 |
| 9 rodadas | 16 | 16 | 14 | 0 |
| 12 rodadas | 16 | 14 | 16 | 0 |
| Controles | 16 | 16 | 18 | 0 |

Com oito rodadas, quatro linhas no byte alto e uma no byte baixo atingiram ou ultrapassaram o corte. Nove e doze rodadas ficaram abaixo do corte nas 960 linhas de cada configuração. A ampliação para peso dois preserva a queda observada de oito para nove no conjunto de chaves avaliado. Ela também mostra que as ocorrências acima do limiar em oito rodadas podem surgir no byte baixo quando a entrada tem dois bits ativos.

Os 17 testes passaram. A execução serial levou 194,50 s, com pico de 23.244 KiB de RSS. [Máximos de todas as linhas](results/differential-weight2-2026-11-27.json)
