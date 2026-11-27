#include "histogram.h"
#include <inttypes.h>

int main(void) {
    Histogram histogram;
    if (!histogram_read(stdin, &histogram)) {
        fputs("PGM P2 inválido ou fora dos limites\n", stderr);
        return 2;
    }
    printf("width=%u height=%u p50=%u p95=%u\n", histogram.width, histogram.height,
           histogram_percentile(&histogram, 50), histogram_percentile(&histogram, 95));
    for (unsigned i = 0; i <= histogram.maximum; i++)
        if (histogram.bins[i]) printf("%u,%" PRIu64 "\n", i, histogram.bins[i]);
}
