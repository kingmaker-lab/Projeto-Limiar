# Verificação local

Execuções realizadas em 26 e 27 de novembro de 2026, no Debian 13 x86-64. Os comandos abaixo registram o que foi verificado antes da publicação.

| Projeto | Evidência |
| --- | --- |
| Hephaestus | GCC 14, teste de alinhamento, rejeição de alocação e reaproveitamento após reset. |
| Titan | GCC 14, teste de impacto, reflexão e passo inválido. |
| Aegis | Cargo e Rust 1.85.1, `cargo test --offline` passou. A CLI calculou e confirmou o SHA-256 do README. |
| Hermes | Go 1.24.4, `go test -race ./...` passou, incluindo publicação concorrente, recarga e validação HTTP. |
| Midas | Ruby 3.3, testes passaram. O exemplo para parceiro totalizou 486 centavos. |
| Vulcan | Zig 0.14.1, teste de snapshot passou. A CLI gravou, leu e removeu uma chave em execuções separadas. |
| Daedalus | GCC e GNU assembler, testes da ABI SysV passaram em x86-64. |
| Pulse | Kotlin 1.9.23 compilou o código de produção contra o SDK 35. Os dois testes JUnit passaram. Sem execução em aparelho ou emulador. |
| Imperium | JDK 21, suite com asserções habilitadas passou. O roteiro deixou 7 peças em A e 3 em B. |
| Nexum | TypeScript 5.7.3 e Node 24, compilação e testes do modelo passaram. O Chromium em modo headless renderizou o exemplo com 3 componentes e 2 conexões. |
| Hydra | Elixir 1.18.3 e OTP 27, ExUnit passou. O escript respondeu `[ops] hello`. |
| Logos | GHC 9.6.6, teste nativo compilado e executado. A regra `1/3 >= 0.3` retornou `True`. |
| Athena | Julia 1.11.5, cinco asserções passaram. Com um milhão de amostras, semente 42 e p=0,4, a taxa foi 0,400127. |
| Chronos | Lua 5.4, testes passaram. A missão demonstrativa avançou de ativa a concluída. |
| Gaia | Python 3.13, dois testes passaram. O exemplo reportou anomalia de 2 °C para janeiro de 2021. |

## Benchmarks locais

| Projeto | Carga | Medição observada |
| --- | --- | --- |
| Hephaestus | Dois milhões de alocações, com reset a cada duas operações | 0,012373 s de CPU, pico de 192 bytes, zero rejeições |
| Titan | 100 discos por mil passos | 0,284712 s de relógio |
| Daedalus | Um milhão de chamadas de MDC | 0,024317 s de CPU, checksum 5.833.298 |
| Athena | Um milhão de sorteios, p=0,4, semente 42 | 0,003531 s na medição da chamada via `@timed` |

As medições são amostras individuais. Para reproduzir, use os comandos nos guias. Para os resultados do GitHub Actions, consulte o workflow no commit publicado.

## Ferramentas 016–025

As dez suítes passaram no Debian 13 x86-64. O Lua 5.4 foi extraído temporariamente de um pacote Debian e o Vigia usou Node.js 24. A matriz do GitHub Actions executa os testes e exemplos em Debian 13.

| Projeto | Caso verificado |
| --- | --- |
| Prisma | Percentis e rejeição de pixels ausentes, fora da faixa ou excedentes. |
| Kairos | Ótimo de 12 no exemplo e equivalência com busca exaustiva em 64 grafos de intervalos sintéticos. |
| Órbita | Ordenação por ondas e rejeição de ciclos, dependências ausentes ou repetidas e chaves duplicadas. |
| Balança | Conciliação em centavos por transação, com rejeição de débitos e créditos compensados apenas entre transações distintas. |
| Viaduto | Rota A → C → B com custo 5, destino inalcançável e rejeição de custo negativo. |
| Vigia | Faixa de p95, contagem de 5xx e rejeição de dados fora da faixa. |
| Comporta | Isolamento por chave, espera de 234 ms e rejeição de retrocesso no relógio. |
| Inventário | Manifestos iguais para árvores equivalentes, caminhos com quebras de linha e detecção de mudança no conteúdo. |
| Esquema | Reaplicação sem alterações, detecção de histórico modificado e reversão completa de lote inválido. |
| Sincronia | Escala mais deslocamento, normalização CRLF e rejeição de intervalos inválidos. |

Nas cargas sintéticas dos guias, o Prisma processou um milhão de pixels em 0,092 s e o Kairos processou 100 mil trabalhos em 0,286 s. Tempos de relógio observados em uma execução de cada binário compilado com `-O2`. A geração das entradas e a compilação ficaram fora da medição.
