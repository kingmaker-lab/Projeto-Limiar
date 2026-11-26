CFLAGS ?= -O2
CFLAGS += -std=c17 -Wall -Wextra -Wpedantic
LDLIBS ?= -lsqlite3

.PHONY: all test clean
all: cerberus-backup

cerberus-backup: backup.c
	$(CC) $(CPPFLAGS) $(CFLAGS) $(LDFLAGS) -o $@ $< $(LDLIBS)

test: all
	python3 -m unittest -v test_backup

clean:
	rm -f -- cerberus-backup
