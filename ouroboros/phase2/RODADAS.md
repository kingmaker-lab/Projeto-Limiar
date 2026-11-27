# Análise diferencial por rodada

Estudo diagnóstico da referência Feistel de 16 bits. Para cada uma das quatro chaves da campanha diferencial, percorremos os oito prefixos sem trocar a agenda. Em cada prefixo, enumeramos o domínio inteiro para as 16 diferenças de entrada de peso um e registramos o máximo de cada linha, com a diferença de saída correspondente. As duas metades do bloco são examinadas separadamente no resumo.

O controle usa as quatro permutações simuladas da campanha anterior. Uma permutação uniforme de 16 bits é a mesma referência marginal para cada prefixo. O ajuste do limiar considera a busca nos oito prefixos, quatro chaves, 16 diferenças de entrada e 65.535 diferenças de saída. Usamos o limite de emparelhamentos da [campanha diferencial](DIFERENCIAL.md). A comparação entre prefixos é diagnóstica, pois a oitava rodada e as chaves já foram observadas.

A implementação avança uma tabela de estados de 128 KiB por vez. Pré-calcula 256 saídas da função de rodada para cada subchave. A oitava rodada deve reproduzir todos os máximos por linha do relatório anterior. Um máximo agregado pode mudar de diferença entre rodadas. Uma queda na série de máximos descreve a distribuição, sem identificar a trajetória de uma diferença específica ou uma causa única.

```sh
python3 -m unittest ouroboros.phase2.test_lab ouroboros.phase2.test_differential ouroboros.phase2.test_rounds -v
python3 -m ouroboros.phase2.rounds > rodadas.json
```

## Resultado de 27 de novembro de 2026

Os valores são contagens máximas de pares ordenados no recorte. O intervalo resume as quatro chaves.

| Rodadas | Diferença no byte baixo | Diferença no byte alto |
| --- | ---: | ---: |
| 1 | 16.384 | 65.536 |
| 2 | 4.096 | 16.384 |
| 3 | 2.048 | 4.096 |
| 4 | 512 | 2.048 |
| 5 | 256 | 512 |
| 6 | 76–168 | 256 |
| 7 | 24–50 | 72–102 |
| 8 | 12–18 | 26–32 |

Na primeira rodada, alterar apenas o byte alto deixa a entrada da função de rodada igual nos dois blocos. A diferença passa inteira para o byte baixo da saída, o que explica os 65.536 pares nessa linha. O excesso diminui ao longo das rodadas. Na oitava, os máximos do byte alto continuam acima do limiar ajustado de 20 nas quatro chaves. Os do byte baixo ficam abaixo do limiar, assim como os controles (12–14). O ajuste cobre 33.553.920 células. O resultado localiza o desvio neste recorte e nestas chaves. Para estudar sua causa, é preciso acompanhar as mesmas diferenças através dos prefixos.

Os nove testes passaram. Os 64 máximos por linha da oitava rodada e os 64 dos controles coincidiram exatamente com o relatório anterior. A execução levou 13,68 s em um processo, com pico de RSS de 18.272 KiB. [Relatório com os máximos de cada linha](results/rounds-2026-11-27.json)
