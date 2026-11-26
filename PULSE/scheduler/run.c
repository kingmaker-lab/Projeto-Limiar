#include "internal.h"

#include <pthread.h>
#include <stdlib.h>

typedef struct {
    uint64_t *workspace;
    size_t words;
    size_t index;
    uint64_t seed;
    uint64_t output;
} Job;

static void *run_job(void *argument)
{
    Job *job = argument;
    job->output = pulse_task(job->seed, job->index, job->workspace, job->words);
    return NULL;
}

static PulseStatus run_batch(Job *jobs, unsigned count)
{
    pthread_t threads[PULSE_MAX_WORKERS - 1];
    unsigned started = 0;
    for (; started + 1 < count; ++started) {
        if (pthread_create(&threads[started], NULL, run_job, &jobs[started + 1]))
            break;
    }

    run_job(&jobs[0]);
    for (unsigned i = 0; i < started; ++i)
        pthread_join(threads[i], NULL);

    return started + 1 == count ? PULSE_OK : PULSE_THREAD;
}

PulseStatus pulse_run(const PulseConfig *config, PulseResult *result)
{
    PulseResult run = {0};
    if (!result)
        return PULSE_INVALID;
    PulseStatus status = pulse_plan(config, &run.worker_limit,
                                    &run.peak_workspace_bytes);
    if (status != PULSE_OK)
        return status;

    double start;
    if (pulse_now_ms(&start))
        return PULSE_CLOCK;
    uint64_t *workspace = malloc(run.peak_workspace_bytes);
    if (!workspace)
        return PULSE_ALLOCATION;

    unsigned width = run.worker_limit;
    Job jobs[PULSE_MAX_WORKERS];
    double end = start;
    while (run.completed < config->tasks) {
        size_t remaining = config->tasks - run.completed;
        unsigned count = remaining < width ? (unsigned)remaining : width;
        for (unsigned i = 0; i < count; ++i) {
            jobs[i] = (Job){
                .workspace = workspace + i * config->words,
                .words = config->words,
                .index = run.completed + i,
                .seed = config->seed
            };
        }

        double batch_start;
        if (pulse_now_ms(&batch_start)) {
            status = PULSE_CLOCK;
            break;
        }
        status = run_batch(jobs, count);
        if (status != PULSE_OK)
            break;
        if (pulse_now_ms(&end)) {
            status = PULSE_CLOCK;
            break;
        }

        for (unsigned i = 0; i < count; ++i)
            run.checksum = pulse_mix(run.checksum ^ jobs[i].output);
        run.completed += count;
        ++run.batches;
        if (count > run.peak_workers)
            run.peak_workers = count;
        run.final_workers = count;
        if (run.completed < config->tasks) {
            unsigned next = pulse_next_width(width, run.worker_limit,
                                             end - batch_start, config->target_ms);
            run.adjustments += next != width;
            width = next;
        }
    }

    free(workspace);
    if (status == PULSE_OK && pulse_now_ms(&end))
        status = PULSE_CLOCK;
    if (status == PULSE_OK) {
        run.elapsed_ms = end - start;
        *result = run;
    }
    return status;
}
