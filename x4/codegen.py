from . import ast

def GenerateCee(a):
  if isinstance(a, ast.Module):
    pass
  else:
    raise TypeError(a)

def AnnotateClasses(clss):
  cd = dict()
  for cls in clss:
    for base in cls.supers:
      cls.members |= cd[base].members
    cd[cls] = cls

