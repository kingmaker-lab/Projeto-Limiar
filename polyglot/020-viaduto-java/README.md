# Viaduto

Calcula rota de menor custo por Dijkstra com fila de prioridade, em um grafo direcionado de custos inteiros não negativos.

## Executar

Requisitos no Debian. JDK 17+. Execute os comandos a partir deste diretório.

```sh
mkdir -p .build
javac -d .build Network.java Main.java
java -cp .build Main A B < example.txt
```

Cada linha contém origem, destino e custo. O exemplo prefere A → C → B com custo 5. Destino inalcançável tem código de saída 1, e entrada inválida tem código 2.

## Testar

```sh
mkdir -p .build
javac -d .build Network.java NetworkTest.java
java -ea -cp .build NetworkTest
```

Licença [MIT](../LICENSE).
