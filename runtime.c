/* gcc -Wall -Werror -Wpedantic --std=c89 runtime.c  */
#include <stdarg.h>
#include <stdlib.h>

#define MAX_NUM_CLASSES 100
#define MAX_NUM_METHODS 100
#define MAX_ARG_LEN 20

int num_classes;
int supers_table[MAX_NUM_CLASSES][MAX_NUM_CLASSES];
int class_member_index_table[MAX_NUM_CLASSES][MAX_NUM_ATTRIBUTES];
int class_members_table[MAX_NUM_CLASSES][MAX_NUM_ATTRIBUTES];

/* classes are determined by two lists of things:
 * its super classes, and its attributes */
void register_class(int nsuper, int nmember, ...) {
  va_list ap;
  int cls = num_classes++, i, mp = 0;

  va_start(ap, nmember);

  for (i = 0; i < nsuper; i++)
    supers_table[cls][va_arg(ap, int)] = 1;

  for (i = 0; i < nmember; i++) {
    int member = va_arg(ap, int);

    class_member_index_table[cls][member] = mp;
  }

  va_end(ap);
}

int main() {
}
