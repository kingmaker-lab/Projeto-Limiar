#include "internal.h"

uint64_t pulse_mix(uint64_t value)
{
    value ^= value >> 30;
    value *= UINT64_C(0xbf58476d1ce4e5b9);
    value ^= value >> 27;
    value *= UINT64_C(0x94d049bb133111eb);
    return value ^ (value >> 31);
}

uint64_t pulse_task(uint64_t seed, size_t index, uint64_t *workspace, size_t words)
{
    uint64_t state = pulse_mix(seed ^ (uint64_t)index);
    for (size_t i = 0; i < words; ++i) {
        state = pulse_mix(state + UINT64_C(0x9e3779b97f4a7c15));
        workspace[i] = state;
    }

    for (size_t i = words; i > 0; --i)
        state = pulse_mix(state ^ workspace[i - 1] ^ (uint64_t)i);
    return state;
}
