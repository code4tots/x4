// g++ -Wall -Werror -Wpedantic -std=c++11 runtime.cc
#include <cstdint>
#include <initializer_list>
#include <iostream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

struct Object;

typedef std::uint_least32_t MethodId;
typedef std::uint_least32_t ClassId;
typedef std::uint_least32_t TypeId;
typedef std::uint_least32_t AttributeId;
typedef std::uint_least32_t MethodNameId;
typedef std::string MethodSignature;
typedef Object *Pointer;
typedef Object *StackPointer;
typedef Object *AttributePointer;

typedef Pointer (*Implementation)(std::initializer_list<Pointer> args);

struct Object {
  ClassId class_id;
  union {
    AttributePointer *attributes;
  } value;
};

void DeclareClass(std::initializer_list<ClassId> supers, std::initializer_list<ClassId> attributes); // supers should include all ancestors and provided in order. Same goes for attributes.
Pointer GetAttribute(Pointer self, AttributeId attribute);
void DeclareMethod(MethodSignature signature, Implementation implementation);
MethodSignature MakeMethodSignature(MethodNameId name, std::initializer_list<ClassId> types);
MethodId FindMethod(MethodSignature signature);
Pointer InvokeMethod(MethodNameId name, std::initializer_list<Pointer> args);

void DeclareUserClasses(); // to be implemented by ccl program
void DeclareUserMethods(); // ''

size_t number_of_classes;
std::vector< std::vector<ClassId> > SUPERS; // ClassId -> List of all superclasses of given class, including ancestors, ordered by order ClassId.
std::vector< std::unordered_map<AttributeId, int> > OFFSET_TABLE; // ClassId -> AttributeId -> index of symbol in instance of class.
std::unordered_map<MethodSignature, MethodId> DISPATCH_CACHE;
std::vector<Implementation> IMPLEMENTATIONS;

void DeclareClass(std::initializer_list<ClassId> supers, std::initializer_list<ClassId> attributes) {
  SUPERS.emplace_back(supers);
  OFFSET_TABLE.push_back(std::unordered_map<AttributeId, int>());
  int offset = 0;
  for (ClassId id : attributes)
    OFFSET_TABLE.back()[id] = offset++;
}

Pointer GetAttribute(Pointer self, AttributeId attribute) {
  return *(self->value.attributes + OFFSET_TABLE[self->class_id][attribute]);
}

void DeclareMethod(MethodSignature signature, Implementation implementation) {
  MethodId id = IMPLEMENTATIONS.size();
  DISPATCH_CACHE[signature] = id;
  IMPLEMENTATIONS.push_back(implementation);
}

MethodId FindMethod(MethodSignature signature) {

}

int main() {
  DeclareClass({1, 2, 3}, {3, 4, 5});
  std::cout << SUPERS.size() << std::endl;
}

// -- Generated from ccl program below this line

void DeclareUserClasses() {
}

void DeclareUserMethods() {
}

