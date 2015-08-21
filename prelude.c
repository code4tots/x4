#define TYPE_INT 0
#define TYPE_FLOAT 1
#define TYPE_STR 2
#define TYPE_LIST 3

typedef struct ObjectStub ObjectStub;
struct ObjectStub {
  int type;
};

typedef struct Object Object;
struct Object {
  int type;
  ObjectStub buffer[1];
};

int main() {
}
