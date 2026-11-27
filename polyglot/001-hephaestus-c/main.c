#include "arena.h"
#include <stdio.h>
#include <string.h>
#include <time.h>

int main(int argc, char **argv) {
    Arena arena;
    if (!arena_init(&arena, 4096)) return 1;
    size_t rounds = argc == 2 && !strcmp(argv[1], "--bench") ? 1000000 : 1;
    clock_t start = clock();
    for (size_t i = 0; i < rounds; ++i) {
        if (!arena_alloc(&arena, 64) || !arena_alloc(&arena, 128)) {
            arena_destroy(&arena);
            return 1;
        }
        arena_reset(&arena);
    }
    printf("allocations=%zu peak=%zu rejected=%zu cpu_seconds=%.6f\n",
           arena.allocations, arena.peak, arena.rejected,
           (double)(clock() - start) / CLOCKS_PER_SEC);
    arena_destroy(&arena);
}
