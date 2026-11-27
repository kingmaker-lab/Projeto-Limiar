# TARTARUS

Laboratório defensivo offline do Projeto Limiar. Os experimentos usam código próprio, configurações revisáveis e dados sintéticos. O primeiro exercício executável valida eventos de auditoria e reproduz uma detecção de mudança de política rejeitada.

## Executar no Debian

Requer Python 3.9 ou superior e GNU Make. Cada comando executa um processo curto, sem dependências externas, rede, portas publicadas ou estado persistente. Os comandos podem ser usados separadamente em uma máquina com cerca de 3,7 GiB de RAM.

```sh
make -C tartarus validate
make -C tartarus start
```

`validate` roda os testes. `start` lê a amostra e emite um resumo JSON com dois eventos e um identificador de alerta. A execução encerra automaticamente. Para interrompê-la, use Ctrl+C. Para repetir o ensaio desde o início, rode `start` novamente. Caso queira guardar o resumo, redirecione a saída de `python3 tartarus/telemetry/replay.py` para um arquivo à sua escolha.

O replay lê apenas a amostra versionada. Use dados inventados nos ensaios, mantenha credenciais e registros reais fora do repositório e execute como usuário comum. Os seis ambientes vulneráveis citados no planejamento ficaram fora deste incremento.

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

Hades tem amostra e testes executáveis. Os demais critérios definem o roteiro de pesquisa. Consulte o [contrato dos eventos](telemetry/README.md) e o [registro de pesquisa e integrações](research/README.md).
