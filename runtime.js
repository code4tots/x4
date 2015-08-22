
function GenericFunction() {
  function Func() {
    var i, types = [], errmsg, result, key, found = false;

    for (i = 0; i < arguments.length; i++)
      types.push(GetTypeOf(arguments[i]))

    key = StrigifySignature(types)

    if (!Func.cache.hasOwnProperty(key)) {

      console.log(key, 'not in cache')

      for (i = 0; i < Func.sigs.length; i++) {
        if (SignatureMatchesTypes(Func.sigs[i], types)) {
          Func.cache[key] = Func.impls[i]
          console.log(Func.cache, 'updated cache')
          found = true
          break
        }
      }

      if (!found)
        throw 'No implementation for: ' + key
    }

    return Func.cache[key].apply(null, arguments)

  }
  Func.sigs = []
  Func.impls = []
  Func.cache = {}
  Func.addImplementation = function(sig, impl) {
    Func.sigs.push(sig)
    Func.impls.push(impl)
    Func.cache = {} // Invalidate the old cache.
  }
  return Func
}

function GetTypeOf(x) {
  switch (typeof x) {
    case 'number': return CCL_SYMBOL_Number
    case 'string': return CCL_SYMBOL_String
    default:
      if (x.hasOwnProperty('type'))
        return x.type
      throw x
  }
}

function SignatureMatchesTypes(sig, types) {
  if (sig.length !== types.length)
    return false

  for (var i = 0; i < sig.length; i++)
    if (!IsSuperOf(sig[i], types[i]))
      return false

  return true
}

function IsSuperOf(sup, type) {
  return sup === type || type.supers.indexOf(sup) > -1
}

function StrigifySignature(sig) {
  var s = '', i
  for (i = 0; i < sig.length; i++)
    s += sig[i].name + ','
  return s
}

var CCL_SYMBOL_Object = {name: 'CCL_SYMBOL_Object', supers: []}
var CCL_SYMBOL_Number = {name: 'CCL_SYMBOL_Number', supers: [CCL_SYMBOL_Object]}
var CCL_SYMBOL_String = {name: 'CCL_SYMBOL_String', supers: [CCL_SYMBOL_Object]}

var CCL_SYMBOL_f = GenericFunction();

CCL_SYMBOL_f.addImplementation([CCL_SYMBOL_String], function(a) {
  console.log('CCL_SYMBOL_String')
})

CCL_SYMBOL_f.addImplementation([CCL_SYMBOL_Number], function(a) {
  console.log('CCL_SYMBOL_Number', a)
})

// console.log(CCL_SYMBOL_f.sigs)

CCL_SYMBOL_f(5)
CCL_SYMBOL_f(5)
