#include <stdio.h>
#include <error.h>
#include <errno.h>
#include <string.h>
#include <sys/stat.h>
#include <time.h>
#include <stdbool.h>
#include <dirent.h>
#include <stdlib.h>

void print_error(int error_number)
{
    char *error_message = strerror(error_number);
    printf("%d: %s\n", error_number, error_message);
}

bool update_me()
{
    int errorno = errno;
    if (errorno == 0)
    {
        printf("Everything went well.\n");
        return true;
    }
    printf("Something went wrong: [%d] -> %s\n", errorno, strerror(errorno));
    return false;
}

long print_file_stat(const char *filename, struct stat *_buf)
{
    printf("------------------[ %s ]------------------\n", filename);
    printf("\tSize: %ld\n", _buf->st_size);
    struct tm *atime = localtime(&_buf->st_atime);
    printf("\tatime: %s", asctime(atime));
    atime = localtime(&_buf->st_ctime);
    printf("\tctime: %s", asctime(atime));
    atime = localtime(&_buf->st_mtime);
    printf("\tmtime: %s", asctime(atime));
    return _buf->st_size;
}

int main(int argc, char **argv)
{
    const char *filename = "main.c";
    // for (int i = 0; i <= 133; i++)
    // print_error(i);
    FILE *file = fopen(filename, "rb");
    if (update_me())
    {
        struct stat buf;
        stat(filename, &buf);
        long file_size = print_file_stat(filename, &buf);
        char *content_buf = malloc((size_t)file_size + 2);
        content_buf[-1] = '\0';
        size_t size_read = fread(content_buf, file_size, file_size, file);
        printf("Size Read: %ld\n", (long)size_read);
        printf("File Content:\"\"\"\n%s\n\"\"\"\n", content_buf);
        free(content_buf);
        fclose(file);
    }
}