# Uma rodada a menos de mistura diferencial

A campanha anterior comparou máximos por rodada. Aqui acompanhamos cada uma das oito diferenças de peso um no byte alto da entrada e comparamos seu histograma completo ao do sufixo correspondente, iniciado com a mesma diferença no byte baixo e sem a primeira subchave. O domínio foi enumerado para quatro chaves sintéticas e oito prefixos.

## Por que a igualdade é exata

Escreva uma rodada Feistel como T(L,R) = (R, L XOR F(R,K)). Se a entrada muda de (L,R) para (L XOR d,R), as duas saídas da primeira rodada diferem por (0,d). Como T é bijetiva, seus estados de saída percorrem o domínio todo uma vez. Assim, para qualquer sufixo G composto pelas rodadas seguintes, o histograma de G(T(x)) para diferença de entrada (d,0) coincide com o histograma de G(y) para diferença (0,d). A primeira rodada transporta a diferença do byte alto sem misturá-la. A identidade decorre da estrutura Feistel e vale para qualquer função de rodada. O tamanho do excesso que resta depende da permutação do sufixo.

## Resultados

Os 256 histogramas completos coincidiram. Os 256 máximos de linha e as diferenças de saída correspondentes também repetiram o relatório histórico por rodada. A tabela acompanha, para cada chave, uma diferença de entrada fixa escolhida retrospectivamente por atingir o maior valor na oitava rodada. Cada célula é o máximo de sua linha em pares ordenados. A diferença de saída que atinge esse máximo pode mudar.

| Chave sintética | Diferença de entrada | Rodadas 1–8 |
| --- | --- | --- |
| `13579bdf` | `1000` | 65.536 → 16.384 → 4.096 → 1.024 → 256 → 256 → 96 → 28 |
| `2468ace0` | `0100` | 65.536 → 16.384 → 4.096 → 2.048 → 512 → 160 → 30 → 26 |
| `31415926` | `0100` | 65.536 → 16.384 → 4.096 → 2.048 → 512 → 172 → 28 → 28 |
| `27182818` | `0100` | 65.536 → 16.384 → 4.096 → 2.048 → 512 → 144 → 96 → 32 |

A execução serial levou 14,43 s, com pico de 22.028 KiB de RSS. Passaram dez testes. Os histogramas foram comparados em memória. O [relatório JSON](results/suffix-2026-11-27.json) guarda os máximos, as diferenças de saída associadas e a quantidade de saídas distintas por linha.

```sh
python3 -m unittest ouroboros.phase2.test_lab ouroboros.phase2.test_differential ouroboros.phase2.test_rounds ouroboros.phase2.test_suffix -v
python3 -m ouroboros.phase2.suffix > sufixo.json
```
