# Esquema

Aplica migrações SQL SQLite em uma transação, registra os SHA-256 e detecta alterações retroativas em arquivos já aplicados.

## Executar

Requisitos no Debian. Python 3.10+ com SQLite. Execute os comandos a partir deste diretório.

```sh
mkdir -p .build
python3 -B main.py .build/demo.sqlite example
python3 -B main.py .build/demo.sqlite example
```

Use arquivos UTF-8 numerados desde 0001, com uma instrução SQL encerrada por linha. Instruções podem ocupar várias linhas. Controle explícito de transações, PRAGMA, ATTACH, gatilhos e tabelas virtuais ficam fora do formato. Use catálogos SQL locais de confiança.

## Testar

```sh
python3 -B -m unittest -v
```

Licença [MIT](../LICENSE).
