"""ast.py

I thought about how Julia made everything Expressions.
I thought about whether I wanted to do that.
I think doing things this way might keep things easy and simple.
"""

"""
# What I think the x4 language is going to look like in my head.

include prelude

class House Object(size Number)

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
  for (var arg in args) {
    Print(arg);
  }
}

Print(arg Number) {
  // ... Some code here on printing numbers
  // Maybe this could be a builtin.
}

"""

class Ast(object):

  def __init__(self, *args):
    for name, arg in zip(self.attributes, args):
      setattr(self, name, arg)

  def __repr__(self):
    return '%s(%s)' % (type(self).__name__, ', '.join(repr(getattr(self, attr)) for attr in self.attributes))

  def __eq__(self, other):
    return type(self) == type(other) and all(getattr(self, attr) == getattr(other, attr) for attr in self.attributes)


class Module(Ast):
  attributes = (
      'classes',             # [Class]
      'functions',           # [Function]
  )


class Class(Ast):
  attributes = (
      'name',                # str
      'supers',              # {str}
      'members',             # {str}
  )


class Function(Ast):
  attributes = (
      'name',                # str
      'arguments',           # [(str, str|None)]
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


class IfElse(Statement):
  attributes = (
      'condition',           # Expression
      'first',               # Statement
      'second',              # Statement
  )


class Expression(Ast):
  pass


class MethodInvocation(Expression):
  attributes = (
      'name',                # str
      'arguments',           # [(Expression, str|None)]
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
