# Protocolo JANUS

*Beyond Language*

**Estado:** proposta de pesquisa · auditoria inicial do Argus pendente.

JANUS é uma frente do Projeto Limiar derivada do **Argus Project v0.4**. Investiga se uma arquitetura compacta consegue representar significado, interpretar informação em contexto e produzir inferências verificáveis sem depender de grandes modelos de linguagem (LLMs) em execução. A pesquisa abrange representação de conhecimento, memória semântica e mecanismos simbólicos ou neuro-simbólicos sob um orçamento computacional limitado.

O ponto de partida proposto é o tokenizador e os mecanismos de análise do Argus. O reaproveitamento de cada componente depende da auditoria da revisão de origem.

## Roadmap proposto

| Etapa | Codinome | Objetivo e evidência esperada |
| --- | --- | --- |
| JAN-001 | **LOGOS** | Tokenização e representação semântica. Estabelecer a referência do Argus e medir um primeiro motor semântico em tarefas de equivalência e relações entre termos. |
| JAN-002 | **MNEMOSYNE** | Memória semântica persistente. Medir recuperação de conhecimento e consistência após reiniciar o processo. |
| JAN-003 | **HERMENEUS** | Interpretação contextual. Medir desambiguação em pares de exemplos nos quais uma mudança de contexto altera a interpretação correta. |
| JAN-004 | **SOPHIA** | Inferência lógica e relacional. Verificar conclusões e seus passos em casos válidos e em contraexemplos. |
| JAN-005 | **NOESIS** | Generalização para contextos desconhecidos. Avaliar domínios ou famílias de exemplos reservados antes do ajuste. |
| JAN-006 | **GNOSIS** | Integração dos mecanismos anteriores. Medir o fluxo completo e repetir a avaliação retirando um componente por vez para estimar sua contribuição. |
| JAN-OMEGA | **JANUS** | Validação científica da arquitetura completa. Reproduzir o protocolo a partir dos artefatos publicados e consolidar resultados, limitações e hipóteses avaliadas. |

A sequência e os codinomes são provisórios. LOGOS é a primeira etapa e começa pela auditoria.

## Hipóteses iniciais

- **H1 · Representação.** Um motor semântico compacto melhora a medida F1 macro sobre a referência lexical em tarefas de equivalência e reconhecimento de relações, dentro do orçamento definido. Medir a diferença no conjunto de teste reservado.
- **H2 · Contexto.** O uso de contexto explícito aumenta a proporção de pares ambíguos em que ambas as interpretações são corretas. Comparar a mesma arquitetura com e sem acesso ao contexto, mantendo os dados e o orçamento.
- **H3 · Eficiência e generalização.** Em tarefas delimitadas e em contextos inéditos, o JANUS consegue operar com menor latência e pico de memória do que um LLM de referência, preservando a qualidade dentro de uma margem previamente definida. Usar o mesmo hardware e contabilizar o processamento necessário para cada resposta.

Os limiares de melhoria, a margem de qualidade, os limites de memória e latência e o critério para resultados inconclusivos serão registrados antes da avaliação final. Uma hipótese fica sem apoio no recorte avaliado quando os resultados deixam de atender aos critérios registrados. Se um comparador não puder ser executado no ambiente definido, a comparação fica pendente.

## Metodologia experimental

1. Auditar o Argus v0.4, fixar a revisão de referência e registrar as limitações de arquitetura e de reprodução.
2. Reproduzir o comportamento disponível no Argus. Usá-lo como linha de base nas tarefas que ele suporta. Para as demais, documentar a cobertura e estabelecer um comparador simples, como correspondência lexical. Selecionar um LLM de referência para a avaliação de H3.
3. Versionar os dados, as anotações, as métricas e os critérios de sucesso e fracasso. Dividir os exemplos em desenvolvimento e teste antes de ajustar o motor. Manter paráfrases e variantes da mesma família na mesma partição e reservar famílias ou domínios inteiros para avaliar generalização.
4. Implementar o primeiro motor semântico funcional em LOGOS sobre a referência auditada. Registrar mudanças de representação e testar sua contribuição contra a linha de base.
5. Executar as comparações com as mesmas entradas, partições e condições de medição. Registrar F1 macro ou acurácia conforme a tarefa, qualidade nos contextos inéditos, latência mediana e p95, pico de memória e consumo de CPU. Documentar hardware, versões, comandos, parâmetros, sementes quando aplicáveis e repetições.
6. Publicar dados redistribuíveis ou instruções de obtenção, comandos, saídas brutas e análise de erros. Incluir resultados negativos, inconclusivos e limites de validade.

## Auditoria inicial do Argus v0.4

**Situação:** pendente. Revisão de origem, linha de base e resultados experimentais ainda aguardam verificação.

- [ ] Localizar o repositório de origem, confirmar a revisão correspondente à v0.4 e registrar URL, commit e licença.
- [ ] Inventariar o tokenizador e os mecanismos de análise, com seus pontos de entrada, formatos, dependências e testes.
- [ ] Tentar reproduzir a execução e os testes em ambiente documentado. Registrar comandos, saídas e bloqueios.
- [ ] Examinar limitações de tokenização, representação e contexto. Identificar o que pode ser reaproveitado e as lacunas para LOGOS.
- [ ] Registrar a linha de base reproduzível e o protocolo da primeira avaliação, incluindo orçamento, limiares e condições de teste. Se a reprodução falhar, documentar a evidência e justificar a referência substituta.

A auditoria se encerra com um relatório versionado que sustente a decisão de reaproveitamento e registre a linha de base de LOGOS ou os bloqueios encontrados.

## Projeto Limiar

- [ICARUS e publicações de pesquisa](../pesquisa/README.md)
- [OUROBOROS Fase II](../ouroboros/phase2/README.md)
- [CERBERUS Fase II](../cerberus/phase-ii/README.md)
