#include "internal.h"

#include <stdio.h>

#define CHECK(condition) do { \
    if (!(condition)) { \
        fprintf(stderr, "linha %d: %s\n", __LINE__, #condition); \
        return 1; \
    } \
} while (0)

int main(void)
{
    PulseConfig config = {.tasks = 11, .words = 32, .budget_bytes = 2048,
                          .workers = 1, .seed = 42};
    PulseResult sequential;
    CHECK(pulse_run(&config, &sequential) == PULSE_OK);
    CHECK(sequential.batches == 11 && sequential.completed == 11);
    CHECK(sequential.peak_workspace_bytes == 256);
    CHECK(sequential.checksum == UINT64_C(0xc524fe3aabba2d06));

    PulseResult parallel;
    config.workers = 4;
    CHECK(pulse_run(&config, &parallel) == PULSE_OK);
    CHECK(parallel.checksum == sequential.checksum);
    CHECK(parallel.batches == 3 && parallel.final_workers == 3);
    CHECK(parallel.peak_workers == 4 && parallel.worker_limit == 4);

    config.budget_bytes = 767;
    config.target_ms = 1;
    CHECK(pulse_run(&config, &parallel) == PULSE_OK);
    CHECK(parallel.worker_limit == 2 && parallel.peak_workspace_bytes == 512);
    CHECK(parallel.completed == 11 && parallel.checksum == sequential.checksum);

    config.budget_bytes = 256;
    CHECK(pulse_run(&config, &parallel) == PULSE_OK);
    CHECK(parallel.worker_limit == 1 && parallel.peak_workspace_bytes == 256);
    CHECK(parallel.checksum == sequential.checksum);

    config.budget_bytes = 255;
    CHECK(pulse_run(&config, &parallel) == PULSE_BUDGET);
    CHECK(parallel.completed == 11);
    config.words = SIZE_MAX;
    CHECK(pulse_run(&config, &parallel) == PULSE_INVALID);
    CHECK(pulse_run(NULL, &parallel) == PULSE_INVALID);
    CHECK(pulse_run(&config, NULL) == PULSE_INVALID);

    CHECK(pulse_next_width(4, 8, 11.0, 10) == 3);
    CHECK(pulse_next_width(4, 8, 4.0, 10) == 5);
    CHECK(pulse_next_width(4, 8, 5.0, 10) == 4);
    CHECK(pulse_next_width(4, 8, 10.0, 10) == 4);
    CHECK(pulse_next_width(1, 8, 11.0, 10) == 1);
    CHECK(pulse_next_width(8, 8, 4.0, 10) == 8);
    CHECK(pulse_next_width(4, 8, 11.0, 0) == 4);
    return 0;
}
