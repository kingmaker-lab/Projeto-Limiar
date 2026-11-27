# TARTARUS

Laboratório defensivo offline do Projeto Limiar. Os experimentos usam código próprio, configurações revisáveis e dados sintéticos. Sete experimentos verificam controles locais e registram os resultados em JSON versionado.

## Executar no Debian

Requer Python 3.9 ou superior e GNU Make. Cada comando executa um processo curto, sem dependências externas, rede, portas publicadas ou estado persistente. Os comandos podem ser usados separadamente em uma máquina com cerca de 3,7 GiB de RAM.

```sh
make -C tartarus validate
make -C tartarus start
```

`validate` roda os testes. `start` mantém a interface original para o replay de Hades. Os comandos terminam automaticamente. Use Ctrl+C para interromper uma execução ou repita o comando para recomeçar com as mesmas amostras.

```sh
make -s -C tartarus list
make -s -C tartarus run TAR=TAR-004
python3 -B tartarus/run.py > tartarus-report.json
```

O relatório tem `schema_version` igual a `1`, resultado geral em `passed` e resultados por experimento em `experiments`. O comando retorna `0` se os resultados coincidirem com as expectativas, `1` se algum divergir e `2` em caso de seleção ou configuração inválida. O GitHub Actions executa os testes e publica o relatório no log da validação.

Use dados inventados nos ensaios, mantenha credenciais e registros reais fora do repositório e execute como usuário comum. O laboratório opera sobre amostras versionadas e o resultado cobre apenas os critérios de cada cenário.

## Trilhas e experimentos

| Experimento | Trilha | Critério de aceite |
| --- | --- | --- |
| TAR-001 Pandora | [Segurança web](web-security/README.md) | Confirmar cabeçalhos esperados em respostas sintéticas. |
| TAR-002 Hydra | [Segurança de APIs](api-security/README.md) | Confirmar a rejeição de campos fora do contrato. |
| TAR-003 Minotaur | [Segurança de redes](network-security/README.md) | Confirmar que o inventário sintético só permite escutas locais. |
| TAR-004 Charon | [Segurança de contêineres](container-security/README.md) | Revisar privilégios, limites e montagens em uma configuração de exemplo. |
| TAR-005 Medusa | [Análise de binários](binary-analysis/README.md) | Identificar formato, arquitetura e hash de um binário próprio. |
| TAR-006 Hecate | [Perícia digital](digital-forensics/README.md) | Reconstruir a sequência de uma evidência sintética com hash verificável. |
| TAR-007 Nemesis | [Código seguro](secure-coding/README.md) | Validar limites de entrada com testes de regressão. |
| TAR-008 Hades | [Engenharia de detecção](detection-engineering/README.md) | Gerar um alerta para uma alteração rejeitada e nenhum para a alteração aceita. |

Pandora, Hydra, Minotaur, Charon, Hecate, Nemesis e Hades são executáveis. Medusa segue no roteiro de pesquisa. Consulte o [contrato dos eventos](telemetry/README.md) e o [registro de pesquisa e integrações](research/README.md).
