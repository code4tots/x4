"""ast.py"""

"""
# What I think the x4 language is going to look like in my head.

include prelude

class House(size Number)

Main() {
  var house = House(add(4, 5));
  Print(house.size, "\n");
}

SayHello(name String) {
  Print("hello!", name, "\n");
}

Add(n Number, m Number) = n + m;

Print(arg, args...) {
  Print(arg);
  for (var arg : args) {
    Print(arg);
  }
}

Print(arg Number) {
  // ... Some code here on printing numbers
  // Maybe this could be a builtin.
}

"""

class Ast(object):
  pass


class Class(Ast):
  attributes = (
      'name',                # str
      'supers',              # [str]
      'members',             # [str]
  )


class Function(Ast):
  attributes = (
      'name',                # str
      'arguments',           # [(str, str)]
      'body',                # Statement
  )


class Statement(Ast):
  pass


class ExpressionStatement(Statement):
  attributes = (
      'expression',          # Expression
  )


class VariableDeclaration(Statement):
  attributes = (
      'name',                # str
  )


class Block(Statement):
  attributes = (
      'statements',          # [Statement]
  )


class Return(Statement):
  attributes = (
      'expression',          # Expression
  )


class Break(Statement):
  attributes = ()


class While(Statement):
  attributes = (
      'condition',           # Expression
      'body',                # Statement
  )


class Expression(Ast):
  pass


class MethodInvocation(Expression):
  attributes = (
      'name',                # str
      'arguments',           # [Expression]
  )


class Assignment(Expression):
  attributes = (
      'name',                # str
      'value',               # Expression
  )


class Int(Expression):
  attributes = (
      'value',               # int
  )


class Float(Expression):
  attributes = (
      'value',               # float
  )


class Str(Expression):
  attributes = (
      'value',               # str
  )


class Name(Expression):
  attributes = (
      'value',               # str
  )
