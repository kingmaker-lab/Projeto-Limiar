# Nexum

Editor de topologia em JSON com componentes tipados, validação de referências, desenho em Canvas e lista textual de conexões. A posição segue a ordem dos componentes e grafos cíclicos são suportados.

## Executar

Requisitos de execução e compilação. Node.js 18+, npm e navegador.

Execute os comandos a partir deste diretório.

```sh
mkdir -p .build
npm ci --no-audit --no-fund
npm run build
node serve.mjs
# Abra http://127.0.0.1:8080 no navegador.
```

## Testar

```sh
mkdir -p .build
npm test
```

Licença [MIT](../LICENSE).
