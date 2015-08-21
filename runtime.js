// KISS. Don't worry about performance for now. Even asymptotically.
// I've thought about it a bit, and I think I have algorithms for
// eliminating basically all of these linear inefficiencies leaving
// only amortized constant overheads.
var CLASSES = [] // list of classes
var METHODS = [] // list of methods

function ContainsElement(array, element) {
  return array.indexOf(element) > -1
}

function RemoveDuplicates(values) {
  var new_values = [], i

  for (i = 0; i < values.length; i++) {
    if (!ContainsElement(new_values, values[i])) {
      new_values.push(values[i])
    }
  }
  return new_values
}

function DeclareClass(name, bases, members) {
  var i, cls

  for (i = 0; i < CLASSES.length; i++) {
    cls = CLASSES[i]
    if (ContainsElement(bases, cls.name)) {
      bases = bases.concat(cls.bases)
      members = members.concat(cls.members)
    }
  }
  CLASSES.push({
    name: name,
    bases: RemoveDuplicates(bases),
    members: RemoveDuplicates(members),
    index: CLASSES.length
  })
}

function IsSubclass(cls, base) {
  return cls.name === base.name || ContainsElement(cls.bases, base.name)
}

function FindClass(name) {
  var i

  for (i = 0; i < CLASSES.length; i++)
    if (CLASSES[i].name === name)
      return CLASSES[i]
}

function CalculateMethodScore(method) {
  var indices = [], score = 0, i, argtypes = method.argtypes

  for (i = 0; i < argtypes.length; i++)
    indices.push(FindClass(argtypes[i]).index)

  for (i = argtypes.length-1; i >= 0; i--)
    score = CLASSES.length * score + indices[i]

  return score
}

function DeclareMethod(name, argtypes, impl) {
  METHODS.push({
    name: name,
    argtypes: argtypes,
    impl: impl
  })
}

function InvokeMethod(name, args) {
  return FindMethod(name, args).impl.apply(null, args)
}

function FindMethod(name, args) {
  var method = null, score = -1, types = [], i

  for (i = 0; i < args.length; i++)
    types.push(args[i].__type__)

  for (i = 0; i < METHODS.length; i++) {
    if (score < CalculateMethodScore(METHODS[i]) && MethodMatches(METHODS[i], name, types)) {
      method = METHODS[i]
      score = method.score
    }
  }

  return method
}

function MethodMatches(method, name, types) {
  var i

  if (method.name !== name)
    return false

  if (method.argtypes.length !== types.length)
    return false

  for (i = 0; i < types.length; i++) {
    if (!IsSubclass(FindClass(types[i]), FindClass(method.argtypes[i])))
      return false
  }

  return true
}

DeclareClass('Object', [], [])
DeclareClass('None', [], [])
DeclareClass('ValPrintable', ['Object'], [])
DeclareClass('Number', ['Object', 'ValPrintable'], [])
DeclareClass('Int', ['Number'], ['__val__'])
DeclareClass('Float', ['Number'], ['__val__'])
DeclareClass('String', ['Number'], ['__val__'])
DeclareClass('List', ['Object'], ['__val__'])

DeclareMethod('Print', ['ValPrintable'], function(val) {
  process.stdout.write(val.__val__.toString())
})

DeclareMethod('Print', ['List'], function(val) {
  var list = val.__val__

  process.stdout.write('[')
  for (var i = 0; i < list.length; i++) {
    InvokeMethod('Print', [list[i]])
    process.stdout.write(', ')
  }
  process.stdout.write(']')
})

DeclareMethod('Size', ['List'], function(list) {
  return {__type__: 'Int', __val__: list.__val__.length}
})

DeclareMethod('Append', ['List', 'Object'], function(list, item) {
  list.__val__.push(item)
  return list
})

// console.log(FindClass('List'))
// console.log(IsSubclass(FindClass('List'), FindClass('ValPrintable')))
// console.log(InvokeMethod('Size', [{__type__: 'List', __val__: []}]))
InvokeMethod('Print', [{__type__: 'Int', __val__: 5}])
InvokeMethod('Print', [{__type__: 'List', __val__: [
  {__type__: 'Int', __val__: 5}
]}])
