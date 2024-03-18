#include <stdio.h>

HELLO_GLOBAL_VAR = 10;

typedef struct hello_struct{
    int a;
    int b;
} HS;

enum status {
    OK,
    ERROR
};

typedef union hello_union {
    int a;
    float b;
} HU;

int main() {
    printf("Hello, World!\n");
    printf("HELLO_GLOBAL_VAR: %d\n", HELLO_GLOBAL_VAR);
    HS hs;
    hs.a = 1;
    hs.b = 2;
    printf("hs.a: %d, hs.b: %d\n", hs.a, hs.b);
    printf("OK: %d, ERROR: %d\n", OK, ERROR);
    HU hu;
    hu.a = 1;
    printf("hu.a: %d\n", hu.a);
    return 0;
}