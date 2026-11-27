# Ensaio linear com máscaras de até dois bits

Ampliamos o [ensaio de peso um](LINEAR.md) para as 136 máscaras não nulas de peso um ou dois em cada lado. Usamos as mesmas oito chaves, oito controles, três configurações e os 65.536 blocos por célula. Isso isola a mudança no conjunto de máscaras. O resultado continua sendo uma ampliação na mesma seleção de chaves.

O limiar familiar de 1% inclui todas as 443.904 células do Ouroboros, inclusive peso um × peso um. O relatório separa os quatro pares de pesos. Cada grupo registra o máximo absoluto, o Walsh assinado e suas máscaras, além da contagem de células que atingem o limiar. Empates escolhem a primeira célula na ordem de enumeração. Os oito controles ficam fora da família de testes e usam o mesmo limiar para comparação descritiva.

A paridade de dois bits é obtida com XOR dos planos individuais. Todas as células são enumeradas. O relatório preserva os resumos por grupo, e o código permite reproduzir a enumeração.

```sh
python3 -m ouroboros.phase2.linear_weight2 > linear-peso2.json
```

## Resultados de 27 de novembro de 2026

O limiar ajustado foi de 1.436 em valor absoluto de Walsh, cerca de 2,19% de correlação. Nenhuma célula do ensaio o atingiu.

| Configuração | 1 × 1 | 1 × 2 | 2 × 1 | 2 × 2 |
| --- | ---: | ---: | ---: | ---: |
| 8 rodadas | 900 | 1.188 | 1.064 | 1.184 |
| 9 rodadas | 856 | 1.044 | 1.076 | 1.220 |
| 12 rodadas | 916 | 1.096 | 1.108 | 1.188 |
| Controles | 924 | 1.044 | 996 | 1.200 |

A tabela mostra o maior valor absoluto observado em cada grupo, entre as oito chaves ou controles correspondentes. O maior pico da campanha com nove rodadas apareceu no grupo 2 × 2. Doze rodadas tiveram um pico menor nesse grupo e picos maiores nos outros três. O ensaio ampliado não demonstra uma vantagem linear consistente de uma configuração sobre a outra.

Os 32 máximos de peso um × peso um coincidiram com o relatório anterior. Os 16 testes passaram, inclusive a verificação das máscaras compostas contra a paridade escalar. A execução serial levou 28,03 s, com pico de 22.640 KiB de RSS. [Resumo por chave, rodada e grupo de máscaras](results/linear-weight2-2026-11-27.json)
