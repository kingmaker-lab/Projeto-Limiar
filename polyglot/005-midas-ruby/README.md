# Midas

Fatura CSV sem cabeçalho em centavos inteiros. A categoria partner recebe desconto de 10%. O tributo demonstrativo de 8% incide sobre o valor líquido. Cada etapa arredonda para o centavo mais próximo com metade para cima.

## Executar

Requisitos de execução e compilação. Ruby 3.1+ com CSV e JSON da distribuição.

Execute os comandos a partir deste diretório.

```sh
mkdir -p .build
ruby main.rb partner example.csv
```

## Testar

```sh
mkdir -p .build
ruby test.rb
```

Licença [MIT](../LICENSE).
