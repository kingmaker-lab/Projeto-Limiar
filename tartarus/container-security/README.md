# TAR-004 · Charon

Avalie um inventário sintético com UID, privilégios, montagens do host, capacidades adicionadas e limite de memória. O controle exige UID maior que zero e limite entre 1 e 512 MiB. A entrada é um inventário simplificado em JSON. A auditoria de Docker Compose real permanece como atividade de pesquisa.

Execute `make -s -C tartarus run TAR=TAR-004` da raiz. Os casos e os resultados esperados estão no [inventário de cenários](../research/scenarios.json).
