# Comparação linear das configurações de 8, 9 e 12 rodadas

A campanha usa as mesmas oito chaves e oito permutações de controle do [ensaio diferencial](CONFIRMACAO.md). Mede um desfecho distinto: as correlações de Walsh para cada um dos 256 pares de máscaras de entrada e saída de peso um. Cada célula é calculada sobre os 65.536 blocos. O relatório registra toda a matriz assinada e os máximos absolutos. A correlação é o valor de Walsh dividido por 65.536.

Sob uma permutação uniforme, o número H de entradas com bit de entrada e bit de saída ambos iguais a um segue a hipergeométrica com população N, N/2 sucessos e N/2 retiradas. O Walsh é 4H−N. Para H ≥ h > N/4, o primeiro termo é C(N/2,h)² / C(N,N/2). A razão entre termos sucessivos é ((N/2−h)/(h+1))² e decresce. Uma série geométrica limita a cauda, multiplicada por dois pela simetria.

Fixamos o nível de 1% para as 6.144 células nas três configurações e oito chaves. O programa determina o primeiro limiar de Walsh absoluto que satisfaz esse limite por união. Uma configuração cruza o limiar se houver pelo menos uma célula que o atinja. Os controles simulados servem para verificar a ordem de grandeza. Valores abaixo do limiar deixam a hipótese sem refutação neste recorte. Eles não estabelecem equivalência entre configurações.

```sh
python3 -m ouroboros.phase2.linear > linear.json
```

## Resultado de 27 de novembro de 2026

O limiar ajustado foi `|Walsh| ≥ 1.232`, equivalente a correlação absoluta de aproximadamente 1,88%. Nenhuma chave ou controle cruzou o limiar.

| Configuração | Intervalo do máximo absoluto por chave ou controle |
| --- | ---: |
| 8 rodadas | 700–900 |
| 9 rodadas | 608–856 |
| 12 rodadas | 632–916 |
| Controles aleatórios | 700–924 |

As oito rodadas, que cruzaram o limite diferencial para todas essas chaves, ficaram abaixo do limite linear. Os dois ensaios medem propriedades distintas. Neste recorte linear, os dados não sustentam uma vantagem consistente de doze sobre nove rodadas.

Há ainda uma dependência estrutural entre configurações adjacentes. O byte alto da rodada 9 é o byte baixo da rodada 8. As colunas de Walsh correspondentes coincidiram para todas as máscaras de entrada nas oito chaves. O ajuste por união continua válido com essa dependência.

A execução serial levou 34,91 s, com pico de 19.896 KiB de RSS. Os 15 testes passaram, inclusive a comparação com Walsh escalar num domínio pequeno e a verificação da cauda e do limiar. [Matrizes assinadas e máximos](results/linear-2026-11-27.json)
