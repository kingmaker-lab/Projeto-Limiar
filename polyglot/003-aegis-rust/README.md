# Aegis

SHA-256 em fluxo e verificação com registro de auditoria em stdout. Guarde o digest de referência em local confiável. A verificação retorna 0 para igualdade, 1 para mudança e 2 para erro. Use em arquivos locais estáveis durante a leitura.

## Executar

Requisitos de execução e compilação. Rust 1.85+, Cargo e coreutils.

Execute os comandos a partir deste diretório.

```sh
mkdir -p .build
cargo run -- hash README.md
digest=$(cargo run --quiet -- hash README.md)
cargo run -- check README.md "$digest" >> .build/audit.log
```

## Testar

```sh
mkdir -p .build
cargo test
```

Licença [MIT](../LICENSE).
