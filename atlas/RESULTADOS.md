# Execução de referência

Em 27 de novembro de 2026, o laboratório foi testado em Debian 13.6, Linux amd64, Go 1.24.4 e Intel Celeron N4020 a 1,10 GHz. O binário estático, compilado com o comando do guia, ocupou 3.354.808 bytes.

| Verificação | Resultado |
| --- | --- |
| Demonstração pelo CLI | Duas carteiras e dois blocos, 100 unidades emitidas. Alice terminou com 83 e Bob com 17. O comando de replay falhou por nonce incorreto e um novo processo reabriu o histórico |
| Testes em Go e `go vet` | Aprovados. Casos cobrem adulteração, chave alheia, saldo insuficiente, nonce futuro, outra rede, replay, conflito entre gastos, cadeia inválida, concorrência e reabertura |
| Testes originais em Node 24.22.1 | 11 aprovados, quatro de PoW e sete de assinaturas. Os sete arquivos preservados foram comparados ao conteúdo da revisão original no GitHub |
| Auditoria de 1.024 blocos | Média de 250 ms em três auditorias, com 1.023 assinaturas P-256. Cerca de 5,54 MB de alocações acumuladas por auditoria, conforme `-benchmem` |

Para reproduzir a medição em um único núcleo, substitua `0` por um núcleo disponível, se necessário:

```sh
GOMAXPROCS=1 GOMEMLIMIT=32MiB taskset -c 0 sh demo.sh ./atlas
GOMAXPROCS=1 GOMEMLIMIT=32MiB taskset -c 0 go test -run '^$' -bench BenchmarkAudit1024 -benchmem -benchtime=3x
```

A demonstração completa levou 0,58 s nessa configuração. O limite de memória é uma meta do runtime Go. As alocações do benchmark representam o total acumulado por operação e não medem o pico de memória residente. O benchmark mede o replay de blocos em memória, sem incluir leitura e regravação do arquivo.

Os READMEs originais registram as publicações no Cloudflare Pages. Para o EXP-003, relatam 15 verificações de protocolo e 10 de interface na prévia HTTPS. A execução acima repetiu as suítes Node preservadas. A implantação Cloudflare e os testes de navegador ficaram fora desta rodada.

## Sincronização local

- `go test -count=1 -v ./...` e `go vet ./...` passaram. A suíte de rede abriu portas reais em `127.0.0.1` e verificou atualização, repetição, par atrasado, divergência, rede incorreta, adulteração, redirecionamento, limite de tamanho e conteúdo adicional.
- `sh demo-sync.sh ./atlas` passou duas vezes. A origem foi reiniciada em outra porta e a réplica terminou com o mesmo arquivo de ledger, dois blocos, emissão de 100 unidades e 17 unidades na conta de Bob. O fluxo original também passou.
- No mesmo Celeron N4020, com afinidade a um núcleo e meta de memória de 32 MiB, uma execução completa de `demo-sync.sh` levou 0,71 s. O binário estático com suporte HTTP ficou em 6.467.768 bytes.

```sh
GOMAXPROCS=1 GOMEMLIMIT=32MiB taskset -c 0 sh demo-sync.sh ./atlas
```

## Interoperabilidade

O ensaio usou Go 1.24.4, Node 24.22.1 e Ruby 3.3.13 com OpenSSL 3.5.7. JavaScript e Ruby consultaram o servidor Go em loopback. Ambos reconstruíram o mesmo estado completo apresentado pelo CLI, incluindo a ponta e os nonces.

- Uma transferência de 17 unidades foi assinada em Go e verificada nos dois clientes.
- Uma transferência de volta de 5 unidades foi assinada em JavaScript, minerada pelo nó Go e verificada também em Ruby.
- O estado final teve três blocos, 150 unidades emitidas, Alice com 138 e Bob com 12. Cada conta tinha nonce 1.
- Os três verificadores rejeitaram valor adulterado, replay e hash de bloco inválido. O executor refez a prova de trabalho nos casos de adulteração e replay para isolar a falha de assinatura ou nonce.

```sh
node interop/check.mjs ./atlas
```
