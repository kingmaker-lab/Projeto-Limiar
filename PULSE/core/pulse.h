#ifndef PULSE_H
#define PULSE_H

#include <stddef.h>
#include <stdint.h>

#define PULSE_MAX_WORKERS 64u

typedef struct {
    size_t tasks;
    size_t words;
    size_t budget_bytes;
    unsigned workers;
    uint64_t seed;
    unsigned target_ms;
} PulseConfig;

typedef struct {
    uint64_t checksum;
    double elapsed_ms;
    size_t peak_workspace_bytes;
    size_t completed;
    size_t batches;
    size_t adjustments;
    unsigned worker_limit;
    unsigned peak_workers;
    unsigned final_workers;
} PulseResult;

typedef enum {
    PULSE_OK,
    PULSE_INVALID,
    PULSE_BUDGET,
    PULSE_ALLOCATION,
    PULSE_THREAD,
    PULSE_CLOCK
} PulseStatus;

/* The result is written only on success. */
PulseStatus pulse_run(const PulseConfig *config, PulseResult *result);
const char *pulse_status_message(PulseStatus status);
int pulse_print_json(const PulseConfig *config, const PulseResult *result,
                     size_t sample);

#endif
