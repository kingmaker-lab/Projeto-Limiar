# PULSE FASE II | Project Genesis

Núcleo computacional da Mobile Division do Projeto Limiar. A CLI executa tarefas sintéticas de CPU e memória em C17, sem acesso de administrador. O núcleo usa apenas a biblioteca padrão C e POSIX para threads e relógio monotônico.

## Compilar e executar

Em Linux, use CMake 3.16 ou posterior, um compilador C17 e um gerador como Make ou Ninja. No Termux, o roteiro proposto é instalar `clang`, `cmake` e `ninja` via `pkg` e compilar dentro da área privada do Termux, onde os binários podem ser executados. A partir da raiz do repositório:

```sh
cmake -S PULSE -B PULSE/build -DCMAKE_BUILD_TYPE=Release
cmake --build PULSE/build --parallel
(cd PULSE/build && ctest --output-on-failure)
PULSE/build/pulse run --tasks 32 --words 65536 --workers 4 --budget-bytes 8388608
PULSE/build/pulse run --tasks 32 --words 65536 --workers 4 --target-ms 2
sh PULSE/benchmarks/compare.sh PULSE/build/pulse 5 4 > pulse.jsonl
```

`run` emite uma amostra. `bench` repete a configuração em execuções independentes (`--repeat`, padrão 5). A saída padrão é JSONL, com diagnósticos em stderr. O código de saída é 0 em sucesso, 1 em falha de execução e 2 para uso inválido. Sem opções, a carga é de 32 tarefas de 65.536 palavras, seed 1, um executor e orçamento de 8 MiB.

## Execução e limites

- Cada tarefa gera e percorre um vetor privado de palavras de 64 bits. A redução dos resultados segue a ordem dos índices. Com a mesma seed, número de tarefas e palavras por tarefa, o checksum é igual em todos os modos.
- `--workers 1` é a referência sequencial. Valores maiores, até 64, executam lotes com a thread chamadora e threads POSIX auxiliares criadas por lote. O custo da criação e da sincronização aparece nas medições. Tarefas pequenas podem favorecer o modo sequencial.
- Cada tarefa precisa de `8 × words` bytes de área de trabalho. O escalonador verifica os produtos e reserva uma única área reutilizável. Limita os executores ao número de tarefas e ao número de vetores que cabem no orçamento. Se um vetor não couber, a execução falha antes de alocar. Pilhas de threads, biblioteca, metadados e RSS ficam fora desse orçamento.
- O ajuste cooperativo começa na largura permitida. Com `--target-ms N`, cada lote acima de N ms reduz a largura seguinte em um. Abaixo de N/2 ms, aumenta em um até o limite. A mudança ocorre entre lotes e a reserva permanece para reutilização. O alvo orienta o ajuste e uma tarefa indivisível pode excedê-lo. A opção 0 desativa o ajuste.
- A telemetria inclui configuração, checksum hexadecimal, tempo total monotônico em ms, bytes reservados, executores solicitados e permitidos, maior largura usada, largura do último lote, lotes e ajustes. Seed e checksum são strings para preservar precisão em leitores JSON.

## Benchmarks e plataforma

O script mede a mesma carga em modo sequencial, paralelo fixo e paralelo adaptativo. Compare os checksums e use a mediana de `elapsed_ms` por configuração. O tempo inclui alocação, tarefas, sincronização e liberação. Registre a máquina e o compilador ao comparar medições. O benchmark não mede temperatura, consumo nem RAM total do processo.

Validação em Debian 13 Linux x86-64, Intel Celeron N4020, GCC 14.2 e CMake 4.4.5. Os dois testes do CTest passaram em Release com avisos tratados como erros e em Debug com UBSan.

Uma rodada Release registrou cinco amostras por modo, com 96 tarefas e 262.144 palavras por tarefa. Todas produziram o checksum `8e6323497322dc74`.

| Modo | Executores solicitados | Mediana (ms) |
| --- | ---: | ---: |
| Sequencial | 1 | 593,188 |
| Paralelo fixo | 4 | 622,793 |
| Adaptativo, alvo de 2 ms | 4 | 476,410 |

O modo adaptativo fez três ajustes por amostra nessa rodada. Os tempos descrevem essa execução local e variam com a carga do ambiente.

O roteiro Termux é preparatório. A execução em Android e ARM, o comportamento térmico e o desempenho sustentado em dispositivo seguem pendentes (GEN-001, GEN-006 e GEN-007).
