#ifndef PRISMA_H
#define PRISMA_H
#include <stdint.h>
#include <stdio.h>
typedef struct {
    unsigned width, height, maximum;
    uint64_t bins[256];
} Histogram;
int histogram_read(FILE *input, Histogram *result);
unsigned histogram_percentile(const Histogram *result, unsigned percent);
#endif
