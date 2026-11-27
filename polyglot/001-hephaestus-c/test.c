#include "arena.h"
#include <assert.h>
#include <stdint.h>

int main(void) {
    Arena arena;
    assert(arena_init(&arena, 256));
    void *first = arena_alloc(&arena, 1);
    void *second = arena_alloc(&arena, sizeof(max_align_t));
    assert(first && second && first != second);
    assert((uintptr_t)second % _Alignof(max_align_t) == 0);
    assert(!arena_alloc(&arena, SIZE_MAX));
    assert(!arena_alloc(&arena, 0));
    assert(arena.rejected == 2 && arena.allocations == 2);
    size_t peak = arena.peak;
    arena_reset(&arena);
    assert(arena.used == 0 && arena.peak == peak);
    assert(arena_alloc(&arena, 1) == first);
    arena_destroy(&arena);
}
