#include "arena.h"
#include <stdlib.h>

int arena_init(Arena *arena, size_t capacity) {
    *arena = (Arena){0};
    if (!capacity || !(arena->data = malloc(capacity))) return 0;
    arena->capacity = capacity;
    return 1;
}

void *arena_alloc(Arena *arena, size_t size) {
    const size_t align = _Alignof(max_align_t);
    size_t padding = (align - arena->used % align) % align;
    size_t remaining = arena->capacity - arena->used;
    if (!size || padding > remaining || size > remaining - padding) {
        ++arena->rejected;
        return NULL;
    }
    size_t offset = arena->used + padding;
    arena->used = offset + size;
    if (arena->used > arena->peak) arena->peak = arena->used;
    ++arena->allocations;
    return arena->data + offset;
}

void arena_reset(Arena *arena) { arena->used = 0; }

void arena_destroy(Arena *arena) {
    free(arena->data);
    *arena = (Arena){0};
}
