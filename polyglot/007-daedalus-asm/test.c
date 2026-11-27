#include "math.h"
#include <assert.h>
#include <inttypes.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

int main(int argc, char **argv) {
    const uint64_t values[] = {UINT64_MAX, 5, 3};
    if (argc == 2 && !strcmp(argv[1], "--bench")) {
        clock_t start = clock();
        uint64_t checksum = 0;
        for (uint64_t i = 1; i <= 1000000; i++) checksum += daedalus_gcd(i, 96);
        printf("checksum=%" PRIu64 " cpu_seconds=%.6f\n", checksum,
               (double)(clock() - start) / CLOCKS_PER_SEC);
        return 0;
    }
    assert(daedalus_sum(values, 3) == 7);
    assert(daedalus_sum(NULL, 0) == 0);
    assert(daedalus_gcd(48, 18) == 6);
    assert(daedalus_gcd(0, UINT64_MAX) == UINT64_MAX);
    assert(daedalus_gcd(0, 0) == 0);
    assert(daedalus_popcount(UINT64_MAX) == 64);
    assert(daedalus_popcount(0) == 0);
    puts("Daedalus OK");
}
