#ifndef ARENA_H
#define ARENA_H
#include <stddef.h>
typedef struct {
    unsigned char *data;
    size_t capacity, used, peak, allocations, rejected;
} Arena;
int arena_init(Arena *arena, size_t capacity);
void *arena_alloc(Arena *arena, size_t size);
void arena_reset(Arena *arena);
void arena_destroy(Arena *arena);
#endif
