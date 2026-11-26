# Histórico e integração GitHub

A primeira publicação da Fase II foi preparada em [The Workshop · PR #56](https://github.com/kingmaker-lab/The-Workshop./pull/56), a partir de [14a93df](https://github.com/kingmaker-lab/The-Workshop./commit/14a93df38c10de66f3233c98092ee093d23b892b). A implementação neste repositório fica em `cerberus/phase-ii/`.

| Origem | Contrato verificado | Decisão na FASE II |
| --- | --- | --- |
| [Portal v0.1](https://github.com/kingmaker-lab/The-Workshop./commit/b563df136af87c60e32090aa7d7beaa7886a5e0a) | Worker estático e registro de projetos. | Publicar evidência estática na página do LIMIAR. |
| [CERBERUS 02](https://github.com/kingmaker-lab/The-Workshop./commit/a2b0a9457353a9df11eac83c51cd2ac58a5a5f6c) | Casos de uso em Python com adaptadores SQLite, JSON e CLI. | Manter o CLI como entrada operacional e o SQLite como armazenamento local. |
| [CERBERUS 03](https://github.com/kingmaker-lab/The-Workshop./commit/5f5f8670c63d8cee210db60e9f4357cac59f1f6c) | Bancada outbox com SQLite e consumidor HTTP em loopback, cenários de reinício e deduplicação. | Testar interrupção e concorrência no fluxo unificado de política. |
| [CERBERUS 04 · v0.5](https://github.com/kingmaker-lab/The-Workshop./commit/18658a4e7260a25e9124f1f40ac3be64ffc4682b) | Aggregate Schedule, estratégia, porta load/commit e adaptadores de comunicação. O portal mantém contratos GET/HEAD. | Definir responsabilidades de validação, persistência e recuperação para uma mesma revisão. O código e as rotas do legado são preservados no repositório. |

Os experimentos registraram abordagens de arquitetura distintas. A FASE II tem um único contrato executável com revisão autenticada, geração esperada e admissão de sessões no consumidor. O Worker publica apenas o relatório da execução local.
