# Balança

Concilia partidas dobradas por transação, com aritmética inteira em centavos. Valida um único lado positivo por linha e exige que débitos e créditos fechem em cada transação.

## Executar

Requisitos no Debian. Ruby com CSV e JSON. Execute os comandos a partir deste diretório.

```sh
ruby main.rb < example.csv
```

O cabeçalho CSV define transação, conta, débito e crédito. O saldo é débito menos crédito. O exemplo produz cash = 125 e sales = -125.

## Testar

```sh
ruby test.rb
```

Licença [MIT](../LICENSE).
