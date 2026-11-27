# ATLAS · GENESIS

Protocolo experimental de blockchain e moeda nativa para execução local em Linux. ATLAS é um nome provisório. Este laboratório integra o Projeto Limiar em `atlas/`, com dados e formato próprios. O componente ATLAS do CERBERUS e a publicação homônima do ICARUS pertencem a outras frentes do Limiar.

## Do Crypto Lab ao GENESIS

A origem é [The Workshop, em `web/crypto-lab`](https://github.com/kingmaker-lab/The-Workshop./tree/d8094def8dbea7c93e52051d1e596dbb192e3b09/web/crypto-lab). O nome canônico do repositório tem ponto final.

| Experimento | Trabalho existente | Aplicação no GENESIS |
| --- | --- | --- |
| EXP-001 | SHA-256, encadeamento e demonstração de adulteração no navegador | Validação do vínculo anterior e do hash de cada bloco ao reabrir o ledger |
| EXP-002 | Worker com alvo de prefixo hexadecimal, serialização posicional e até 500.000 tentativas | Portabilidade para Go, com dificuldade fixa de dois zeros hexadecimais e emissão por bloco válido |
| EXP-003 | ECDSA P-256/SHA-256, SPKI, assinatura bruta e auditoria de saldo e nonce | Carteiras em disco, domínio e rede no payload, replay integral do histórico e rejeição de nonce reutilizado |
| EXP-004 e EXP-005 | UTXO, mempool e P2P constam como trabalho planejado | GENESIS conserva o modelo de contas que já tinha testes. A seção de evolução define o próximo passo |

[`legacy/`](legacy/) preserva os READMEs, as implementações JavaScript e as suítes Node dos EXP-002/003. Os arquivos são cópias da revisão citada, inclusive os comandos e os relatos históricos de publicação. A interface web e o Worker de publicação ficam na origem. O Crypto Lab oferece chaves efêmeras e saldos de sessão. Comece o GENESIS com duas carteiras novas e gere a emissão pela mineração local. Os formatos, domínios de assinatura e endereços são diferentes.

Go concentra ledger, mineração e CLI em um binário sem dependências externas. JavaScript permanece como referência executável dos laboratórios. Um explorador TypeScript pode consumir os mesmos vetores de protocolo quando a interface de leitura estiver estável.

## Reproduzir

Requer Linux e Go 1.24 ou superior. Node 22 ou superior executa as suítes legadas. A partir da raiz do Limiar:

```sh
cd atlas
go test ./...
go vet ./...
CGO_ENABLED=0 go build -buildvcs=false -trimpath -ldflags='-s -w' -o ./atlas ./cmd/atlas
sh demo.sh ./atlas
node --test legacy/pow/tests/pow.test.cjs legacy/signatures/tests/protocol.test.cjs
```

A demonstração cria duas carteiras, minera para Alice, assina uma transferência de 17 unidades para Bob, inclui a transferência em um segundo bloco e tenta repeti-la. Um novo processo reabre o ledger. O resultado esperado é altura 2, emissão 100, saldo de Alice 83 e saldo de Bob 17. A demonstração usa arquivos descartáveis.

Para manter um ledger experimental:

```sh
umask 077
./atlas init
alice=$(./atlas wallet alice.pem)
bob=$(./atlas wallet bob.pem)
./atlas mine "$alice"
./atlas sign alice.pem "$bob" 17 > transferencia.json
./atlas mine "$alice" transferencia.json
./atlas status
```

O arquivo `.atlas/ledger.json` guarda os blocos completos. Use `./atlas -dir CAMINHO COMANDO` para escolher outro diretório, com a opção antes do comando. `status` revalida a cadeia e mostra rede, altura, ponta, emissão e contas. `wallet` cria um PEM privado com modo 0600 e recusa sobrescrever a chave. Os arquivos de chave são experimentais, sem criptografia em repouso. Para preservar o laboratório, faça backup do ledger e das carteiras em um diretório privado. Depois de uma falha de gravação, consulte `status` antes de repetir a operação.

## Regras e persistência

- `init` gera um identificador de rede aleatório de 32 bytes em hexadecimal minúsculo. A âncora é SHA-256 de `["ATLAS_GENESIS_V1/genesis", network]`. A altura inicial e a emissão são zero.
- A carteira usa chave pública P-256 em SPKI DER. O endereço é `atl_` seguido de SHA-256 do DER canônico em hexadecimal minúsculo. Assina-se o SHA-256 do JSON posicional `["ATLAS_GENESIS_V1/transfer", network, from, to, amount, nonce]`. A assinatura tem 64 bytes em formato `r || s`, com cada inteiro de 32 bytes em big-endian. Chave pública e assinatura usam Base64 padrão no JSON.
- O bloco usa SHA-256 de `["ATLAS_GENESIS_V1/block", network, height, previous, miner, transfer, nonce]`. O valor de `transfer` é `null` ou o array `[from, to, amount, nonce, publicKey, signature]`. O PoW exige primeiro byte zero e nonce de bloco de 0 a 499.999. Os arrays são JSON UTF-8 sem espaços entre campos.
- Um bloco inclui até uma transferência. Antes da recompensa, a operação precisa de assinatura válida, contas distintas, valor inteiro positivo disponível e nonce imediatamente posterior ao último aceito do remetente. O nonce do primeiro gasto é 1. Dois gastos concorrentes com o mesmo nonce são incompatíveis; um gasto posterior com nonce novo continua sujeito ao saldo restante.
- A emissão é de 50 unidades inteiras por bloco aceito, incluído aquele que registra uma transferência. A recompensa é creditada depois do gasto. A auditoria deriva a emissão da altura e reconstrói saldos do zero. Com até 4.096 blocos, o máximo verificável é 204.800 unidades por ledger. Os valores ficam abaixo do limite de precisão inteira do JavaScript. Não há taxas, casas decimais ou pré-alocação.
- Cada escrita adquire trava exclusiva sobre o diretório, relê o arquivo e revalida antes da troca atômica. A gravação sincroniza o temporário e o diretório em disco. Leitores abrem um instantâneo do arquivo, limitado a 8 MiB. A auditoria e a regravação crescem linearmente com a altura. A persistência assume um diretório privado em um sistema de arquivos local Linux e processos cooperantes.

A dificuldade baixa permite reescrita rápida por quem controla o diretório. O identificador de rede isola assinaturas entre ledgers inicializados separadamente. Cópias da mesma rede podem divergir e aceitar gastos conflitantes se operadas em diretórios diferentes. GENESIS tem um escritor por ledger local, corrida resolvida pela trava, sem consenso distribuído, finalidade econômica ou garantias de produção. Use chaves descartáveis e moeda sem valor financeiro.

## Evolução

1. **Protocolo e intercâmbio.** Congelar vetores cruzados Go/TypeScript, acrescentar exportação com versão e impor limites antes de aceitar mensagens. Critério de aceite: implementações independentes calculam a mesma âncora, os mesmos hashes e verificam as mesmas assinaturas.
2. **P2P em loopback.** Usar a mesma gênese em dois nós, com handshake por versão e rede, limites de mensagens e sincronização por lotes, validando cada bloco antes da troca de estado. Critério: dois processos reiniciam e retomam a sincronização a partir de armazenamento independente.
3. **Consenso experimental.** Especificar seleção por trabalho acumulado, empates, reorganizações e revalidação de transações pendentes. Exercitar partições, blocos conflitantes e reconvergência. Avaliar UTXO em uma versão separada se a pesquisa exigir validação por saída, com vetores de gasto duplo por referência.
4. **Integração.** Acrescentar exploração somente leitura em TypeScript e publicar evidências no portal após os ensaios locais. Uma pesquisa de consenso inspirada em Ouroboros exige especificação própria. A rede de Feistel sintética estudada no Limiar é um experimento diferente.

Consulte [a execução de referência](RESULTADOS.md).
