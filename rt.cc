// g++ -std=c++11 -Wpedantic -Werror -Wall rt.cc
#include <cstdlib>
#include <functional>
#include <initializer_list>
#include <iostream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

typedef std::string Symbol;

std::size_t NUMBER_OF_CLASSES;

struct Class {
  std::size_t id;
  std::unordered_set<Class*> supers;
  Class(std::initializer_list<Class*> supers) : id(NUMBER_OF_CLASSES++), supers(supers) {}
  bool IsSubclassOf(Class *cls) const {
    return this == cls || supers.find(cls) != supers.end();
  }
};

typedef std::vector<Class*> Signature;

struct Object {
  Class *cls;
  Object(Class *cls) : cls(cls) {}
};

typedef std::initializer_list<Object*> Arguments;
typedef std::function<Object*(Arguments)> Implementation;

struct UserObject : public Object {
  std::unordered_map<Symbol*, Object*> attrs;
  UserObject(Class *cls, std::initializer_list< std::unordered_map<Symbol*, Object*>::value_type> attrs) : Object(cls), attrs(attrs) {}
};

bool SignatureMatchesArguments(Signature signature, Arguments args) {
  if (signature.size() != args.size())
    return false;

  auto sigp = signature.begin();
  auto argp = args.begin();

  for (; sigp != signature.end(); ++sigp, ++argp)
    if (!(*argp)->cls->IsSubclassOf(*sigp))
      return false;

  return true;
}

struct Function {
  std::vector< std::pair< std::vector<Class*>, Implementation> > impls;

  Function(std::initializer_list< std::pair< std::vector<Class*>, Implementation> > impls) : impls(impls) {}

  Object *operator()(Arguments args) const {

    for (const auto& pair : impls) {
      if (SignatureMatchesArguments(pair.first, args))
        return pair.second(args);
    }

    std::cerr << "Error **** no matching implementation found" << std::endl;
    std::exit(1);
  }
};

void test();

int main() {
  UserObject obj(nullptr, {});
  std::cout << obj.cls << std::endl;
  test();
}

Class CCL_NAME_xObject({});
Class CCL_NAME_xNumber({
  &CCL_NAME_xObject,
});

Function CCL_NAME_xPrint({
  {
    {},
    [](Arguments args) {
      std::cout << "hi!" << std::endl;
      std::cout << NUMBER_OF_CLASSES << std::endl;
      return nullptr;
    },
  }
});


void test() {
  CCL_NAME_xPrint({});
}
