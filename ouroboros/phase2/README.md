# Ouroboros Fase II · O Limiar da Serpente

Laboratório offline para a rede de Feistel sintética do EXP-008. Uso exclusivo de pesquisa. Para dados reais, use uma biblioteca mantida com AEAD estabelecido. A implementação e o oráculo congelados conservam seus nomes e semântica históricos.

- [Demonstração prática em 16 bits](DEMO.md)
- [Inventário das fontes](INVENTARIO.md)
- [Decisões, critérios de refutação e agenda 2027](ARQUITETURA.md)
- [Resultados locais](RESULTADOS.md)
- [Campanha diferencial com novas chaves](DIFERENCIAL.md)
- [Análise diferencial por rodada](RODADAS.md)
- [Comparação diferencial com o sufixo Feistel](SUFIXO.md)
- [Comparação da referência com a variante de até 12 rodadas](VARIANTE.md)
- [Confirmação diferencial das nove rodadas](CONFIRMACAO.md)
- [Comparação linear das configurações de 8, 9 e 12 rodadas](LINEAR.md)
- [Ensaio linear com máscaras de até dois bits](LINEAR_PESO2.md)
- [Ensaio diferencial com diferenças de dois bits](DIFERENCIAL_PESO2.md)

## Resultados e conclusões

Os ensaios abaixo comparam as mesmas oito chaves sintéticas e oito controles simulados. Cada célula foi calculada sobre os 65.536 blocos. A tabela mostra o maior valor observado por configuração. Os limiares foram ajustados separadamente para as comparações de cada ensaio.

| Ensaio | 8 rodadas | 9 rodadas | 12 rodadas | Controles | Limiar ajustado |
| --- | ---: | ---: | ---: | ---: | ---: |
| [Diferencial · 1 bit de entrada](CONFIRMACAO.md) | 54 | 16 | 14 | 16 | 20 pares ordenados |
| [Diferencial · 2 bits de entrada](DIFERENCIAL_PESO2.md) | 28 | 16 | 16 | 18 | 22 pares ordenados |
| [Linear · máscaras de 1 bit](LINEAR.md) | 900 | 856 | 916 | 924 | 1.232 em valor absoluto de Walsh |
| [Linear · máscaras de 1 ou 2 bits](LINEAR_PESO2.md) | 1.188 | 1.220 | 1.188 | 1.200 | 1.436 em valor absoluto de Walsh |

- **Diferencial.** Com oito rodadas, as oito chaves atingiram ou ultrapassaram o limiar de um bit. No ensaio de dois bits, cinco linhas atingiram ou ultrapassaram o limiar, todas com os bits alterados no mesmo byte. Nove e doze ficaram abaixo dos dois limiares em todas as chaves. Nove foi a menor configuração avaliada com esse resultado.
- **Linear.** Nenhuma configuração atingiu os limiares. O ensaio com até dois bits não encontrou vantagem consistente de doze sobre nove. Os dados dos dois ensaios lineares se sobrepõem, pois o recorte ampliado inclui as máscaras anteriores.
- **Estrutura.** Para diferenças no byte alto, a primeira rodada transfere a diferença para o byte baixo sem alterá-la. O histograma resultante coincide com o das rodadas restantes iniciadas com essa diferença no byte baixo. A igualdade foi verificada em 256 histogramas. [Demonstração e dados](SUFIXO.md)
- **Correção e custo.** O EXP-014 reproduziu 327.680 comparações da referência com o oráculo em cinco chaves. Com as tabelas de rodada preparadas, o benchmark local mediu 611 ns por bloco com oito rodadas e 847 ns com doze. O benchmark não mediu nove rodadas. [Conformidade](RESULTADOS.md) · [Benchmark](VARIANTE.md)

O resultado sustenta a queda do excesso diferencial de oito para nove nos recortes medidos. As campanhas não estabelecem equivalência entre nove e doze nem validam segurança. O estudo usa um bloco de 16 bits, chave de 32 bits e um conjunto limitado de chaves e máscaras. A reprodução em outra implementação e máquina está pendente. O Ouroboros permanece restrito ao laboratório com dados sintéticos.

Na raiz do projeto, com Python 3.11+ e biblioteca padrão:

```sh
python3 -m unittest ouroboros.phase2.test_lab -v
python3 -m ouroboros.phase2.lab trace
python3 -m ouroboros.phase2.lab panel
python3 -m ouroboros.phase2.lab schedule
python3 -m ouroboros.phase2.lab benchmark
```

`trace` mostra os dois bytes do estado a cada rodada; `panel` compara Feistel, identidade e permutação aleatória usando a mesma amostra sintética. Use `panel --exact` para percorrer 65.536 entradas por diferença/máscara do recorte. O denominador converte contagens SAC e diferencial em probabilidades empíricas, e converte numeradores assinados de Walsh em correlações. A diferença de entrada e ambas as máscaras lineares têm peso um. A diferença de saída diferencial pode ter qualquer peso. O painel amostral é exploratório.

Para repetir a conformidade histórica, faça checkout de `34f98b19429070ab817c79bfc205d087cb62d3dd` do Workshop em uma cópia descartável e execute da raiz dela:

```sh
python3 research/cryptography/ouroboros-low-level/experiments/014-research-consolidation/conformance.py
```

O comando salva o relatório dentro dessa cópia.
