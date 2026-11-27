#include "internal.h"

#include <inttypes.h>
#include <stdio.h>
#include <time.h>

int pulse_now_ms(double *ms)
{
    struct timespec time;
    if (clock_gettime(CLOCK_MONOTONIC, &time))
        return -1;
    *ms = (double)time.tv_sec * 1000.0 + (double)time.tv_nsec / 1000000.0;
    return 0;
}

const char *pulse_status_message(PulseStatus status)
{
    switch (status) {
    case PULSE_OK: return "ok";
    case PULSE_INVALID: return "configuracao invalida ou fora do intervalo";
    case PULSE_BUDGET: return "orcamento insuficiente para uma tarefa";
    case PULSE_ALLOCATION: return "falha ao reservar memoria de trabalho";
    case PULSE_THREAD: return "falha ao criar thread";
    case PULSE_CLOCK: return "falha no relogio monotonico";
    }
    return "erro desconhecido";
}

int pulse_print_json(const PulseConfig *config, const PulseResult *result,
                     size_t sample)
{
    int written = printf(
        "{\"schema\":1,\"sample\":%zu,\"tasks\":%zu,\"words\":%zu,"
        "\"seed\":\"%" PRIu64 "\",\"checksum\":\"%016" PRIx64 "\","
        "\"budget_bytes\":%zu,\"peak_workspace_bytes\":%zu,"
        "\"requested_workers\":%u,\"worker_limit\":%u,\"peak_workers\":%u,"
        "\"final_workers\":%u,\"target_ms\":%u,\"batches\":%zu,"
        "\"adjustments\":%zu,\"elapsed_ms\":%.3f}\n",
        sample, result->completed, config->words, config->seed, result->checksum,
        config->budget_bytes, result->peak_workspace_bytes, config->workers,
        result->worker_limit, result->peak_workers, result->final_workers,
        config->target_ms, result->batches, result->adjustments, result->elapsed_ms);
    return written < 0 || fflush(stdout) == EOF ? -1 : 0;
}
