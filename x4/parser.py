import collections

from . import ast

Token = collections.namedtuple('Token', 'type value')

KEYWORDS = (
    'class', 'as',
)

SYMBOLS = (
    '(', ')', '{', '}',
    ',', ';',
)


class Parser:
  def __init__(self, string, source):
    self.string = string
    self.source = source
    self.mark = 0
    self.position = 0
    self.peek = NextToken(self)


def Done(p):
  return p.position >= len(p.string)


def Char(p, diff=0):
  position = p.position + diff
  return p.string[position] if position < len(p.string) else ''


def StartsWith(p, prefix):
  return p.string.startswith(prefix, p.position)


def IsNameChar(c):
  return c.isalnum() or c == '_'


def SkipSpaces(p):
  while Char(p) and Char(p).isspace():
    p.position += 1
  p.mark = p.position


def Cut(p):
  value = p.string[p.mark:p.position]
  p.mark = p.position
  return value


def NextToken(p):
  SkipSpaces(p)

  if Done(p):
    return None

  if StartsWith(p, ('r"', "r'", "'", '"')):
    raw = False
    if Char(p) == 'r':
      raw = True
      p.position += 1

    quote = p.string[p.position:p.position+3] if StartsWith(p, ('"""', "'''")) else Char(p)
    p.position += len(quote)
    while not StartsWith(p, quote):
      p.position += 2 if raw and Char(p) == '\\' else 1
    p.position += len(quote)

    return Token('str', eval(Cut(p)))

  for symbol in SYMBOLS:
    if StartsWith(p, symbol):
      p.position += len(symbol)
      return Token(Cut(p), None)

  if Char(p).isdigit() or (Char(p) == '.' and Char(p, 1).isdigit()):
    while Char(p).isdigit():
      p.position += 1

    if Char(p) == '.':
      p.position += 1
      while Char(p).isdigit():
        p.position += 1
      return Token('float', float(Cut(p)))
    else:
      return Token('int', int(Cut(p)))

  if IsNameChar(Char(p)):
    while IsNameChar(Char(p)):
      p.position += 1
    name = Cut(p)
    if name in KEYWORDS:
      return Token(name, None)
    else:
      return Token('name', name)

  while Char(p) and not Char(p).isspace():
    p.position += 1
  raise SyntaxError(Cut(p))


def GetToken(p):
  tok = p.peek
  p.peek = NextToken(p)
  return tok


def GetTokens(p):
  toks = []
  while p.peek is not None:
    toks.append(GetToken(p))
  return toks


assert GetTokens(Parser("class Thing()", 'xx')) == [Token('class', None), Token('name', 'Thing'), Token('(', None), Token(')', None)]


def At(p, tok):
  return p.peek.type == tok


def Consume(p, tok):
  if At(p, tok):
    return GetToken(p)


def Expect(p, tok):
  if not At(p, tok):
    raise SyntaxError('Expected %s got %s' % (tok, p.peek))
  return GetToken(p)


def ParseModule(p):
  clss = []
  funcs = []
  while not Done(p):
    if At(p, 'class'):
      clss.append(ParseClass(p))
    else:
      funcs.append(ParseFunction(p))
  return ast.Module(clss, funcs)


def ParseClass(p):
  Expect(p, 'class')
  name = Expect(p, 'name').value
  Consume(p, ':')
  supers = set()
  while not Consume(p, '('):
    supers.add(Expect(p, 'name').value)
    Consume(p, ',')
  members = set()
  while not Consume(p, ')'):
    members.add(Expect(p, 'name').value)
    Consume(p, ',')
  return ast.Class(name, supers, members)


def ParseFunction(p):
  name = Expect(p, 'name').value
  args = []
  Expect(p, '(')
  while not Consume(p, ')'):
    argname = Expect(p, 'name').value
    argtype = Consume(p, 'name').value if At(p, 'name') else None
    args.append((argname, argtype))
    Consume(p, ',')
  body = ParseStatement(p)
  return ast.Function(name, args, body)


def ParseStatement(p):
  if At(p, '{'):
    return ParseBlock(p)
  else:
    return ParseExpressionStatement(p)


def ParseBlock(p):
  Expect(p, '{')
  stmts = []
  while not Consume(p, '}'):
    stmts.append(ParseStatement())
  return ast.Block(stmts)


def ParseExpressionStatement(p):
  expr = ParseExpression(p)
  Expect(p, ';')
  return ast.ExpressionStatement(expr)


def ParseExpression(p):
  return ParsePostfixExpression(p)


def ParsePostfixExpression(p):
  expr = ParsePrimaryExpression(p)
  while True:
    if Consume(p, '('):
      if not isinstance(expr, ast.Name):
        raise ValueError('variable methods not yet supported')
      args = []
      while not Consume(p, ')'):
        argval = ParseExpression(p)
        argtype = None
        if Consume(p, 'as'):
          argtype = Expect(p, 'name').value
        args.append((argval, argtype))
        Consume(p, ',')
      expr = ast.MethodInvocation(expr, args)
    else:
      break
  return expr


def ParsePrimaryExpression(p):
  if At(p, 'name'):
    return ast.Name(GetToken(p).value)
  elif At(p, 'int'):
    return ast.Int(GetToken(p).value)
  elif At(p, 'float'):
    return ast.Float(GetToken(p).value)
  elif At(p, '('):
    expr = ParseExpression(p)
    Expect(p, ')')
    return expr
  else:
    raise SyntaxError('Expected expression')


def Parse(string, source):
  return ParseModule(Parser(string, source))

assert(Parse("""
class X Object, Thing(a, b c)
Main(argc Int, argv) {}
""", '') == ast.Module([ast.Class('X', {'Object', 'Thing'}, {'a', 'b', 'c'})], [ast.Function('Main', [('argc', 'Int'), ('argv', None)], ast.Block([]))]))
