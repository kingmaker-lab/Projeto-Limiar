# Logos

Parser de aritmética racional exata com precedência, sinais, decimais e parênteses. Regras comparam duas expressões e a API permite fornecer variáveis nomeadas.

## Executar

Requisitos de execução e compilação. GHC e biblioteca base.

Execute os comandos a partir deste diretório.

```sh
mkdir -p .build
ghc -Wall -outputdir .build -o .build/logos Main.hs
.build/logos eval '1.5 + 3 * (2 - 1)'
.build/logos rule '>=' '1/3;0.3'
```

## Testar

```sh
mkdir -p .build
runghc Test.hs
```

Licença [MIT](../LICENSE).
