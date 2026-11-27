# Inventário

Gera um manifesto SHA-256 ordenado por caminho relativo e separado por NUL, preservando nomes com espaços e quebras de linha. Links simbólicos ficam fora do inventário.

## Executar

Requisitos no Debian. Bash e utilitários GNU coreutils/findutils. Execute os comandos a partir deste diretório.

```sh
work=$(mktemp -d)
printf 'amostra\n' > "$work/arquivo.txt"
bash inventory.sh "$work" | tr '\0' '\n'
rm -r -- "$work"
```

Para comparar dois manifestos completos, use cmp. Gere as saídas fora do diretório inventariado e mantenha a árvore estável durante a leitura. A conversão com tr é apenas para exibir nomes simples. Em caso de erro de leitura, descarte a saída parcial.

## Testar

```sh
bash test.sh
```

Licença [MIT](../LICENSE).
