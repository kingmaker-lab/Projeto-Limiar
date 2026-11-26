#include "pulse.h"

#include <inttypes.h>
#include <limits.h>
#include <stdio.h>
#include <string.h>

static void usage(FILE *stream)
{
    fputs("Uso: pulse run|bench [--tasks N] [--words N] [--workers N]\n"
          "       [--budget-bytes N] [--seed N] [--target-ms N]\n"
          "       [--repeat N (bench)]\n"
          "Saida: um objeto JSON por amostra. --target-ms 0 desativa ajuste.\n",
          stream);
}

static int parse_uint(const char *input, uintmax_t limit, uintmax_t *output)
{
    uintmax_t value = 0;
    if (!*input)
        return -1;
    for (; *input; ++input) {
        if (*input < '0' || *input > '9')
            return -1;
        unsigned digit = (unsigned)(*input - '0');
        if (value > limit / 10 || (value == limit / 10 && digit > limit % 10))
            return -1;
        value = value * 10 + digit;
    }
    *output = value;
    return 0;
}

static int set_option(PulseConfig *config, size_t *repeat, int bench,
                      const char *name, const char *input)
{
    uintmax_t value;
    if (parse_uint(input, UINTMAX_MAX, &value))
        return -1;

    if (!strcmp(name, "--tasks") && value > 0 && value <= SIZE_MAX)
        config->tasks = (size_t)value;
    else if (!strcmp(name, "--words") && value > 0 && value <= SIZE_MAX)
        config->words = (size_t)value;
    else if (!strcmp(name, "--budget-bytes") && value <= SIZE_MAX)
        config->budget_bytes = (size_t)value;
    else if (!strcmp(name, "--workers") && value > 0 && value <= PULSE_MAX_WORKERS)
        config->workers = (unsigned)value;
    else if (!strcmp(name, "--seed") && value <= UINT64_MAX)
        config->seed = (uint64_t)value;
    else if (!strcmp(name, "--target-ms") && value <= UINT_MAX)
        config->target_ms = (unsigned)value;
    else if (bench && !strcmp(name, "--repeat") && value > 0 && value <= SIZE_MAX)
        *repeat = (size_t)value;
    else
        return -1;
    return 0;
}

int main(int argc, char **argv)
{
    if (argc == 2 && !strcmp(argv[1], "--help")) {
        usage(stdout);
        return 0;
    }
    const int bench = argc >= 2 && !strcmp(argv[1], "bench");
    if (argc < 2 || (!bench && strcmp(argv[1], "run"))) {
        usage(stderr);
        return 2;
    }

    PulseConfig config = {
        .tasks = 32, .words = 65536, .budget_bytes = 8u * 1024 * 1024,
        .workers = 1, .seed = 1
    };
    size_t repeat = bench ? 5 : 1;
    for (int i = 2; i < argc; ++i) {
        if (argc - i < 2 || set_option(&config, &repeat, bench, argv[i], argv[i + 1])) {
            fprintf(stderr, "Opcao invalida: %s\n", argv[i]);
            return 2;
        }
        ++i;
    }
    for (size_t i = 0; i < repeat; ++i) {
        PulseResult result;
        PulseStatus status = pulse_run(&config, &result);
        if (status != PULSE_OK) {
            fprintf(stderr, "pulse: %s\n", pulse_status_message(status));
            return 1;
        }
        if (pulse_print_json(&config, &result, i + 1)) {
            fputs("pulse: falha ao gravar telemetria\n", stderr);
            return 1;
        }
    }
    return 0;
}
