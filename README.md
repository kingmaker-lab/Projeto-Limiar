# Projeto Limiar

**Beyond Limits · Laboratório de pesquisa experimental da The Workshop**

O Limiar investiga o que arquiteturas compactas conseguem fazer sob restrições reais de computação. Cada frente parte de uma pergunta verificável, registra seus critérios de avaliação e publica evidências para que outras pessoas possam reproduzir os testes e examinar os limites dos resultados.

[Portal do Projeto Limiar](https://workshop-limiar.wolfpackworkshop.workers.dev/) · [Publicações versionadas](pesquisa/README.md) · [Mapa histórico da The Workshop](https://github.com/kingmaker-lab/The-Workshop./blob/main/docs/MAPA-DO-REPOSITORIO.md)

## Frentes de pesquisa

| Frente | Pergunta de pesquisa | Onde começar |
| --- | --- | --- |
| **ICARUS** · Eficiência computacional | Quanto trabalho pode ser evitado com computação seletiva dentro de um limite de perda de qualidade? | [Seis experimentos do Ciclo I e publicações de ATHENA, GAUSS, ATLAS e OMEGA](pesquisa/README.md) |
| **CERBERUS Fase II** · Resiliência de software | Como validar, ativar e restaurar configurações preservando a consistência do serviço? | [Serviço local, CLI, testes e modelos executáveis](cerberus/phase-ii/README.md) |
| **OUROBOROS Fase II** · O Limiar da Serpente | Que propriedades uma rede de Feistel de 16 bits apresenta em condições experimentais controladas? | [Laboratório offline, dados sintéticos e roteiro de reprodução](ouroboros/phase2/README.md) |
| **JANUS** · Beyond Language | Uma arquitetura compacta consegue representar significado, interpretar contexto e produzir inferências verificáveis sem depender de um LLM em execução? | [Protocolo, hipóteses e roadmap](janus/README.md) |
| **TARTARUS** · Segurança defensiva | Como validar controles e detecções com evidências sintéticas em uma máquina de recursos limitados? | [Protocolo, trilhas e laboratório offline](tartarus/README.md) |

## JANUS · Beyond Language

Derivado do **Argus Project v0.4**, JANUS começa pela auditoria do tokenizador e dos mecanismos de análise. O relatório da auditoria orientará o reaproveitamento do Argus e a definição de uma linha de base reproduzível.

| Etapa | O que investiga | Estado |
| --- | --- | --- |
| **JAN-001 · LOGOS** | Tokenização e representação semântica | Aberta · auditoria inicial pendente |
| **JAN-002 · MNEMOSYNE** | Memória semântica persistente | Programada |
| **JAN-003 · HERMENEUS** | Interpretação contextual | Programada |
| **JAN-004 · SOPHIA** | Inferência lógica e relacional verificável | Programada |

O roteiro segue com **NOESIS** para avaliar generalização, **GNOSIS** para integrar os mecanismos e **JAN-OMEGA** para validar a arquitetura completa.

[Entregáveis, critérios de aceite e metodologia](janus/README.md) · [JANUS no portal](https://workshop-limiar.wolfpackworkshop.workers.dev/#janus)

## Como consultar e reproduzir

- **Consultar resultados.** O [índice de publicações](pesquisa/README.md) aponta para os commits da The Workshop que registram os experimentos e artigos.
- **Executar os laboratórios.** Os guias de [CERBERUS](cerberus/phase-ii/README.md) e [OUROBOROS](ouroboros/phase2/README.md) registram requisitos, comandos e procedimentos de teste. O laboratório de OUROBOROS usa dados sintéticos e tem finalidade de pesquisa.
- **Acompanhar hipóteses abertas.** A [metodologia do JANUS](janus/README.md#metodologia-experimental) descreve como comparar qualidade, generalização, latência e consumo de recursos. O protocolo prevê a publicação de resultados negativos e inconclusivos.
