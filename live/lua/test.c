#include <stdio.h>
// #include <stdlib.h>

typedef void(*HelloType)();

struct Hello {
    HelloType hello;
};

void hello() {
    printf("Hello From ANSI C\n");
}

void luaopen_test() {
    printf("Opening test lua package...\n");
    // struct Hello* h = malloc(sizeof(struct Hello));
    // h->hello = hello;
    // return h;
}

void luaclose_test() {
    printf("Closing test lua package...\n");
}