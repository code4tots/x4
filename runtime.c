#include <stdarg.h>
#include <stdlib.h>
#define TYPE_INT 0
#define TYPE_FLOAT 1
#define TYPE_STR 2
#define TYPE_LIST 3

typedef struct Object Object;
typedef struct List List;
typedef struct String String;

struct Object {
  int type;
  union {
    List *list;
    String *string;
    Object **attrs;
    long integer;
    double number;
  } value;
};

typedef struct Arguments Arguments;
struct Arguments {
  int argc;
  Object **argv;
};

extern Object *(*METHOD_TABLE[])(Arguments*);

Object *InvokeMethod(int method, int argc, ...) {
  va_list ap;
  Arguments args;
  int i;
  Object *result;

  args.argc = argc;
  args.argv = (Object**) malloc(sizeof(Object*) * argc);

  va_start(ap, argc);
  for (i = 0; i < argc; i++)
    args.argv[i] = va_arg(ap, Object*);
  va_end(ap);

  result = METHOD_TABLE[method](&args);

  free(args.argv);

  return result;
}

Object *(*METHOD_TABLE[])() = {0, 0, 0};

int main() {
}
