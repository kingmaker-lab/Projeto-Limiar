# Protocolo JANUS

*Beyond Language*

**Estado:** primeiras quatro etapas lançadas · LOGOS aberta para auditoria do Argus.

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

## Lançamento das quatro primeiras etapas

LOGOS está aberta para a auditoria. MNEMOSYNE, HERMENEUS e SOPHIA têm escopo publicado e entram em execução à medida que suas dependências forem atendidas. Cada etapa publica o protocolo de avaliação antes da rodada final e fecha com artefatos reproduzíveis e uma decisão registrada sobre a hipótese. A conclusão da etapa e o apoio à hipótese são decisões distintas.

### JAN-001 · LOGOS

**Estado:** aberta para auditoria.

- **Trabalho:** localizar e fixar a revisão do Argus v0.4, reproduzir tokenização e análise e executar a [auditoria inicial](#auditoria-inicial-do-argus-v04). Com o relatório publicado, definir a saída versionada do tokenizador e da representação semântica e implementar o primeiro motor.
- **Entregáveis:** relatório de auditoria, comandos de reprodução, conjunto anotado de pares equivalentes e relações entre termos, comparador lexical, motor e relatório de H1. Registrar a referência do Argus nas tarefas que a revisão auditada suporta.
- **Aceite:** uma execução documentada aplica o comparador e o motor à mesma partição reservada e gera F1 macro, latência e pico de memória. Publicar o resultado diante do limiar de melhoria e do orçamento fixados previamente. Se a referência do Argus for irrecuperável, exigir justificativa documentada para a linha de base substituta antes da avaliação.

### JAN-002 · MNEMOSYNE

**Estado:** programada · depende do formato versionado de representação de LOGOS.

- **Trabalho:** persistir unidades semânticas, relações e sua origem em armazenamento local. Definir como gravar, consultar e reabrir a memória. Usar a mesma coleção de fatos para avaliar a memória antes e depois de reiniciar o processo.
- **Entregáveis:** formato de armazenamento, implementação mínima, casos de recuperação e relatório com taxa de acerto entre os primeiros resultados, latência e tamanho em disco.
- **Aceite:** em um processo novo, a memória recupera as mesmas relações e origens esperadas após reabrir a coleção. Os casos incluem consultas sem correspondência. Publicar a comparação com uma referência de busca exata no mesmo conjunto.

### JAN-003 · HERMENEUS

**Estado:** programada · depende da consulta versionada de MNEMOSYNE e da representação de LOGOS.

- **Trabalho:** interpretar uma expressão ambígua a partir do contexto fornecido e das relações recuperadas. Preparar pares com a mesma expressão-alvo e contextos que exigem interpretações distintas. Agrupar variações por família na divisão entre desenvolvimento e teste.
- **Entregáveis:** conjunto de pares anotados, interpretador com rastro dos trechos e relações usados e relatório de H2.
- **Aceite:** executar a mesma arquitetura com e sem acesso ao contexto explícito, mantendo dados e orçamento. Reportar a proporção de pares com as duas interpretações corretas, a variação entre condições e os erros do conjunto reservado. Confrontar o ganho com o limiar definido antes do teste.

### JAN-004 · SOPHIA

**Estado:** programada · depende das relações de MNEMOSYNE e da saída contextual de HERMENEUS.

- **Trabalho:** aplicar um conjunto versionado de regras a fatos com origem registrada. Emitir a conclusão acompanhada dos fatos e das regras aplicadas, ou registrar que as premissas são insuficientes.
- **Entregáveis:** catálogo de regras, motor de inferência, verificador de passos e coleção de casos válidos, contraexemplos e casos com premissas insuficientes.
- **Aceite:** o verificador confirma cada passo das conclusões emitidas. Medir acerto nos casos válidos, rejeição nos contraexemplos e abstenção quando faltam premissas, além do custo de execução. Publicar as falhas e as regras envolvidas para orientar a avaliação de generalização em NOESIS.

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
