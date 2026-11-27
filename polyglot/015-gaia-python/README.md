# Gaia

Agrupa observações diárias de uma estação por mês e compara a temperatura média com o mês equivalente do ano-base. Reporta cobertura em dias. Meses sem referência recebem anomalia nula e lacunas não são preenchidas.

## Executar

Requisitos de execução e compilação. Python 3.10+ e biblioteca padrão.

Execute os comandos a partir deste diretório.

```sh
mkdir -p .build
python3 -B main.py example.csv --baseline 2020
```

## Testar

```sh
mkdir -p .build
python3 -B -m unittest -v
```

Licença [MIT](../LICENSE).
