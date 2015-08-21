from . import ast

def genc(a):
  if isinstance(a, ast.Module):
    pass
  else:
    raise TypeError(a)

def annotate_classes(clss):
  cd = dict()
  for cls in clss:
    cd[cls.name] = set()
    for base in cls.supers:
      cd[cls.name] |= bases
  