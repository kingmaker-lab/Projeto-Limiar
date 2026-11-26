#include "internal.h"

PulseStatus pulse_plan(const PulseConfig *config, unsigned *limit, size_t *bytes)
{
    if (!config || !config->tasks || !config->words || !config->workers ||
        config->workers > PULSE_MAX_WORKERS ||
        config->words > SIZE_MAX / sizeof(uint64_t))
        return PULSE_INVALID;

    const size_t task_bytes = config->words * sizeof(uint64_t);
    size_t slots = config->budget_bytes / task_bytes;
    if (!slots)
        return PULSE_BUDGET;
    if (slots > config->tasks)
        slots = config->tasks;
    if (slots > config->workers)
        slots = config->workers;

    *limit = (unsigned)slots;
    *bytes = slots * task_bytes;
    return PULSE_OK;
}
