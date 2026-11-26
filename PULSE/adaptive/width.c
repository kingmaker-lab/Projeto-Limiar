#include "internal.h"

unsigned pulse_next_width(unsigned width, unsigned limit, double batch_ms,
                          unsigned target_ms)
{
    if (!target_ms)
        return width;
    if (batch_ms > target_ms && width > 1)
        return width - 1;
    if (batch_ms < target_ms / 2.0 && width < limit)
        return width + 1;
    return width;
}
