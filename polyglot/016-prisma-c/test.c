#include "histogram.h"
#include <assert.h>

static int read_text(const char *text, Histogram *result) {
    FILE *file = tmpfile();
    assert(file);
    assert(fputs(text, file) >= 0);
    rewind(file);
    int ok = histogram_read(file, result);
    fclose(file);
    return ok;
}

int main(void) {
    Histogram histogram;
    assert(read_text("P2\n# comment\n2 2\n255\n0 20 20 255\n", &histogram));
    assert(histogram.bins[20] == 2 && histogram_percentile(&histogram, 50) == 20);
    assert(histogram_percentile(&histogram, 95) == 255);
    assert(!read_text("P2 2 2 255 0 1 2", &histogram));
    assert(!read_text("P2 1 1 2 3", &histogram));
    assert(!read_text("P2 1 1 2 2 1", &histogram));
}
