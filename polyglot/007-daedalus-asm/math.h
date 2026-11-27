#ifndef DAEDALUS_MATH_H
#define DAEDALUS_MATH_H
#include <stdint.h>
#include <stddef.h>
uint64_t daedalus_gcd(uint64_t a, uint64_t b);
uint64_t daedalus_sum(const uint64_t *items, size_t count);
unsigned daedalus_popcount(uint64_t value);
#endif
