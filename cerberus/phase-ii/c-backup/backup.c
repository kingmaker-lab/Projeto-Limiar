#define _POSIX_C_SOURCE 200809L
#include <fcntl.h>
#include <sqlite3.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

static int open_db(sqlite3 **db, const char *path, int flags)
{
    if (sqlite3_open_v2(path, db, flags, NULL) != SQLITE_OK) {
        fprintf(stderr, "SQLite: %s\n", *db ? sqlite3_errmsg(*db) : "sem memória");
        return -1;
    }
    return 0;
}

static int verify(sqlite3 *db)
{
    sqlite3_stmt *stmt = NULL;
    const char *check = "PRAGMA quick_check(1)";
    int result = -1;
    if (sqlite3_prepare_v2(db, check, -1, &stmt, NULL) == SQLITE_OK &&
        sqlite3_step(stmt) == SQLITE_ROW) {
        const unsigned char *message = sqlite3_column_text(stmt, 0);
        if (message && strcmp((const char *)message, "ok") == 0)
            result = 0;
    }
    sqlite3_finalize(stmt);
    if (result != 0) {
        fprintf(stderr, "O SQLite recusou a verificação estrutural.\n");
        return -1;
    }
    const char *schema = "SELECT generation, policy, action, source, mac "
                         "FROM revisions ORDER BY generation DESC LIMIT 1";
    stmt = NULL;
    result = sqlite3_prepare_v2(db, schema, -1, &stmt, NULL);
    if (result == SQLITE_OK)
        result = sqlite3_step(stmt);
    sqlite3_finalize(stmt);
    if (result != SQLITE_ROW) {
        fprintf(stderr, "Banco sem revisão CERBERUS legível.\n");
        return -1;
    }
    return 0;
}

static int copy_db(const char *source, const char *temp)
{
    sqlite3 *src = NULL;
    sqlite3 *dst = NULL;
    int result = -1;
    if (open_db(&src, source, SQLITE_OPEN_READONLY) != 0 ||
        open_db(&dst, temp, SQLITE_OPEN_READWRITE) != 0)
        goto done;

    sqlite3_backup *backup = sqlite3_backup_init(dst, "main", src, "main");
    if (!backup) {
        fprintf(stderr, "SQLite backup: %s\n", sqlite3_errmsg(dst));
        goto done;
    }

    int step = sqlite3_backup_step(backup, -1);
    int finish = sqlite3_backup_finish(backup);
    if (step != SQLITE_DONE || finish != SQLITE_OK) {
        fprintf(stderr, "SQLite backup: %s\n", sqlite3_errstr(step != SQLITE_DONE ? step : finish));
        goto done;
    }
    /* O destino deve ser um arquivo autossuficiente, mesmo se a origem usar WAL. */
    if (sqlite3_exec(dst, "PRAGMA journal_mode=DELETE", NULL, NULL, NULL) != SQLITE_OK) {
        fprintf(stderr, "SQLite journal: %s\n", sqlite3_errmsg(dst));
        goto done;
    }
    result = verify(dst);

done:
    sqlite3_close(dst);
    sqlite3_close(src);
    return result;
}

static int sync_file(const char *path)
{
    int fd = open(path, O_RDONLY);
    if (fd < 0) {
        perror(path);
        return -1;
    }
    int result = fsync(fd);
    if (result != 0)
        perror(path);
    close(fd);
    return result;
}

static int publish(const char *source, const char *target)
{
    const char *suffix = ".partial.XXXXXX";
    size_t size = strlen(target) + strlen(suffix) + 1;
    char *temp = malloc(size);
    if (!temp) {
        perror("malloc");
        return 1;
    }
    char *parent = strdup(target);
    if (!parent) {
        perror("strdup");
        free(temp);
        return 1;
    }
    char *slash = strrchr(parent, '/');
    if (slash == parent)
        slash[1] = '\0';
    else if (slash)
        *slash = '\0';
    else
        strcpy(parent, ".");

    snprintf(temp, size, "%s%s", target, suffix);
    int result = 1;
    int fd = mkstemp(temp);
    if (fd < 0) {
        perror("arquivo temporário");
        goto done;
    }
    close(fd);
    if (copy_db(source, temp) == 0 && sync_file(temp) == 0) {
        if (link(temp, target) != 0) {
            perror("publicação do backup");
        } else {
            result = 0;
        }
    }
    if (unlink(temp) != 0) {
        perror("remoção do arquivo temporário");
        result = 1;
    }
    if (sync_file(parent) != 0)
        result = 1;

done:
    free(parent);
    free(temp);
    return result;
}

int main(int argc, char **argv)
{
    if (argc != 3 || !argv[1][0] || !argv[2][0]) {
        fprintf(stderr, "uso: cerberus-backup BANCO_ORIGEM BACKUP_NOVO\n");
        return 64;
    }
    return publish(argv[1], argv[2]);
}
