#include "histogram.h"
#include <ctype.h>
#include <string.h>

static int token(FILE *input, char output[32]) {
    int c;
    do {
        c = fgetc(input);
        if (c == '#') while (c != '\n' && c != EOF) c = fgetc(input);
    } while (c != EOF && isspace(c));
    if (c == EOF) return ferror(input) ? -1 : 0;
    size_t length = 0;
    while (c != EOF && !isspace(c)) {
        if (length == 31 || c == 0 || c == '#') return -1;
        output[length++] = (char)c;
        c = fgetc(input);
    }
    output[length] = 0;
    return ferror(input) ? -1 : 1;
}

static int number(FILE *input, unsigned bound, unsigned *result) {
    char word[32];
    if (token(input, word) != 1) return 0;
    unsigned value = 0;
    for (size_t i = 0; word[i]; i++) {
        if (word[i] < '0' || word[i] > '9') return 0;
        unsigned digit = (unsigned)(word[i] - '0');
        if (digit > bound || value > (bound - digit) / 10) return 0;
        value = value * 10 + digit;
    }
    *result = value;
    return 1;
}

int histogram_read(FILE *input, Histogram *result) {
    Histogram next = {0};
    char word[32];
    if (token(input, word) != 1 || strcmp(word, "P2") ||
        !number(input, 10000, &next.width) || !next.width ||
        !number(input, 10000, &next.height) || !next.height ||
        !number(input, 255, &next.maximum) || !next.maximum) return 0;
    uint64_t pixels = (uint64_t)next.width * next.height;
    if (pixels > 10000000) return 0;
    for (uint64_t i = 0; i < pixels; i++) {
        unsigned intensity;
        if (!number(input, next.maximum, &intensity)) return 0;
        next.bins[intensity]++;
    }
    if (token(input, word) != 0) return 0;
    *result = next;
    return 1;
}

unsigned histogram_percentile(const Histogram *result, unsigned percent) {
    uint64_t total = (uint64_t)result->width * result->height;
    uint64_t rank = (total * percent + 99) / 100;
    uint64_t accumulated = 0;
    for (unsigned i = 0; i <= result->maximum; i++) {
        accumulated += result->bins[i];
        if (accumulated >= rank && accumulated) return i;
    }
    return result->maximum;
}
