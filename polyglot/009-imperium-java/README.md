# Imperium

Processa movimentos de estoque em memória a partir de stdin. Transferências preservam o total e validam saldo, depósito, SKU e overflow antes de debitar a origem. O relatório é ordenado por depósito e SKU.

## Executar

Requisitos de execução e compilação. JDK 17+.

Execute os comandos a partir deste diretório.

```sh
mkdir -p .build
javac -d .build Inventory.java Main.java
printf 'receive A PART 10\ntransfer A B PART 3\nreport\n' | java -cp .build Main
```

## Testar

```sh
mkdir -p .build
javac -d .build Inventory.java InventoryTest.java
java -ea -cp .build InventoryTest
```

Licença [MIT](../LICENSE).
