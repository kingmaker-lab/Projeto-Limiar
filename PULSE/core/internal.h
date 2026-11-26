#ifndef PULSE_INTERNAL_H
#define PULSE_INTERNAL_H

#include "pulse.h"

uint64_t pulse_mix(uint64_t value);
uint64_t pulse_task(uint64_t seed, size_t index, uint64_t *workspace, size_t words);
PulseStatus pulse_plan(const PulseConfig *config, unsigned *limit, size_t *bytes);
unsigned pulse_next_width(unsigned width, unsigned limit, double batch_ms,
                          unsigned target_ms);
int pulse_now_ms(double *ms);

#endif
