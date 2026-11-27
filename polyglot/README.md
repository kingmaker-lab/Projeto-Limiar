# Operação Polyglot

Quinze aplicações independentes do Projeto Limiar, cada uma implementada e testada na sua linguagem. Os guias por projeto indicam os requisitos, o comando de execução e a suíte local. Instale só a ferramenta do projeto que for usar.

| Projeto | Linguagem | Aplicação |
| --- | --- | --- |
| [001 · Hephaestus](001-hephaestus-c/) | C | Arena de memória com telemetria |
| [002 · Titan](002-titan-cpp/) | C++ | Simulação de partículas e colisões 2D |
| [003 · Aegis](003-aegis-rust/) | Rust | Integridade SHA-256 e auditoria local |
| [004 · Hermes](004-hermes-go/) | Go | Mensageria HTTP concorrente persistente |
| [005 · Midas](005-midas-ruby/) | Ruby | Faturamento em centavos e regras de desconto |
| [006 · Vulcan](006-vulcan-zig/) | Zig | Armazenamento persistente chave–valor |
| [007 · Daedalus](007-daedalus-asm/) | Assembly | Biblioteca matemática x86-64 |
| [008 · Pulse](008-pulse-kotlin/) | Kotlin | Diagnóstico Android sem permissões declaradas |
| [009 · Imperium](009-imperium-java/) | Java | Estoque e transferências entre depósitos |
| [010 · Nexum](010-nexum-typescript/) | TypeScript | Editor e visualizador de arquitetura |
| [011 · Hydra](011-hydra-elixir/) | Elixir | Pub/sub em tempo real com recuperação supervisionada |
| [012 · Logos](012-logos-haskell/) | Haskell | Expressões racionais e regras de comparação |
| [013 · Athena](013-athena-julia/) | Julia | Simulação estatística e intervalo de confiança |
| [014 · Chronos](014-chronos-lua/) | Lua | Eventos, missões e NPCs determinísticos |
| [015 · Gaia](015-gaia-python/) | Python | Agregação climática mensal e anomalias |

O [workflow](../.github/workflows/polyglot.yml) roda um job por linguagem. As aplicações de terminal usam Debian 13 no CI. O Android usa o SDK em um runner Ubuntu, sem emulador. Consulte os [resultados e limites da verificação local](VERIFICACAO.md).

A [licença MIT](LICENSE) cobre os arquivos da operação.
