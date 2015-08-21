#define TYPE_INT 0
#define TYPE_FLOAT 1
#define TYPE_STR 2
#define TYPE_LIST 3

typedef Object Object;
typedef List List;
typedef String String;

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

int main() {
}
