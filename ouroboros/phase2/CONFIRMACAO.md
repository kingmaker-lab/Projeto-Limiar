# Ensaio de confirmação das nove rodadas

A campanha anterior observou queda abaixo do limiar na nona rodada. Esta campanha fixa oito chaves novas, derivadas dos primeiros quatro bytes de SHA-256 dos rótulos ASCII `limiar-ouroboros-confirmacao-v1:0` a `limiar-ouroboros-confirmacao-v1:7`, em ordem big-endian. A derivação é uma regra pública de seleção. A campanha usa oito controles simulados, com sementes inteiras de 20261201 a 20261208.

O desfecho primário exige que a referência de oito rodadas ultrapasse ou alcance o limiar em pelo menos quatro chaves e que todos os máximos de nove rodadas fiquem abaixo dele. Doze rodadas servem de referência comparativa. O limiar a 1% inclui a busca nas três configurações, oito chaves, 16 diferenças de entrada de peso um e 65.535 diferenças de saída. Os controles são uma verificação de sanidade. Todos os máximos são obtidos por enumeração do domínio de 65.536 entradas.

O ensaio confirma a observação em outra seleção de chaves na mesma implementação. A reprodução externa e o exame de outras famílias de diferenças e máscaras seguem questões separadas.

```sh
python3 -m ouroboros.phase2.confirm > confirmacao.json
```

## Resultado de 27 de novembro de 2026

O ensaio cumpriu o critério. O limiar ajustado foi de 20 pares ordenados, para uma família de 25.165.440 células.

| Configuração | Intervalo dos máximos | Chaves no limiar ou acima |
| --- | ---: | ---: |
| 8 rodadas | 24–54 | 8/8 |
| 9 rodadas | 12–16 | 0/8 |
| 12 rodadas | 12–14 | 0/8 |
| Controles aleatórios | 12–16 | 0/8 |

Nas oito chaves e diferenças de peso um, nove foi o menor número de rodadas **entre os três avaliados nesta campanha** que ficou abaixo do limiar em todas as chaves. A comparação entre os máximos medidos em nove e doze rodadas não estabelece equivalência entre as duas configurações. A próxima comparação pode examinar máscaras lineares e diferenças de maior peso com critérios próprios.

A campanha rodou em um processo, em 43,16 s, com pico de 23.592 KiB de RSS. Os 12 testes do laboratório passaram. A rotina compartilhada também reproduziu os resultados por linha dos cinco prefixos para a primeira chave da campanha anterior. [Dados e máximos por linha](results/confirm-2026-11-27.json)
