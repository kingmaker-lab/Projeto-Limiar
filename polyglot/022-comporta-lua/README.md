# Comporta

Simula limitação de taxa por chave com token bucket, créditos inteiros e timestamps reproduzíveis em milissegundos. Informa quanto esperar para o pedido seguinte, assumindo ausência de consumo adicional.

## Executar

Requisitos no Debian. Lua 5.4. Execute os comandos a partir deste diretório.

```sh
lua5.4 main.lua 3 2 < example.txt
```

Os argumentos são taxa em tokens por segundo e capacidade inicial. As linhas têm timestamp, chave e custo. O simulador aceita até 10 mil chaves na mesma execução.

## Testar

```sh
lua5.4 test.lua
```

Licença [MIT](../LICENSE).
