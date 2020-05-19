
-- original ---------------------------------
vocabulary {
    type color constructed from {red, blue}
    type code constructed from {a,b}
    codeOf(color): code
    c:color
} 

theory {
    { !cl[color]: ! cd[code]: codeOf(cl)=cd <- (cl=c & cd=a) | (cl~=c & cd=b). }
    codeOf(red)=b.
}
 
view expanded

-- vocabulary -------------------------------

-- theory -----------------------------------
codeOf(red) == b

Or(codeOf(red) == a, codeOf(red) == b)

Or(codeOf(blue) == a, codeOf(blue) == b)

Or(c == red, c == blue)

And((codeOf(red) == a) == (red == c),
    (codeOf(red) == b) == Not(red == c),
    (codeOf(blue) == a) == (blue == c),
    (codeOf(blue) == b) == Not(blue == c))

-- subtences ------------------------------------
codeOf(red) = b
red = c
codeOf(red) = a
codeOf(blue) = a
codeOf(blue) = b
c = red
c = blue

-- GUILines ------------------------------------
codeOf(red)
codeOf(blue)
c
codeOf(red) = b
red = c
codeOf(red) = a
codeOf(blue) = a
codeOf(blue) = b
c = red
c = blue

-- case -------------------------------------
Type:        
  
Definitions: 
  Rule:∀$codeOf!0$[color],$codeOf$[code]: codeOf($codeOf!0$,$codeOf$) ⇔($codeOf!0$ = c ∧ $codeOf$ = a) ∨ (~($codeOf!0$ = c) ∧ $codeOf$ = b)
Universals:  
  codeOf(red) -> b
  codeOf(red) = b
Consequences:
  codeOf(blue) -> a
  c -> blue
  ~red = c
  ~codeOf(red) = a
  codeOf(blue) = a
  ~codeOf(blue) = b
  ~c = red
  c = blue
Simplified:  
  b = b
  false ∨ true
  false ∨ true
Irrelevant:  
  codeOf(blue) -> a
  codeOf(blue) = a
  ~codeOf(blue) = b
Co-constraints:
  (false) ∨ (true)


-- meta -------------------------------------
{'symbols': [{'idpname': 'codeOf', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'},
             {'idpname': 'c', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'c': {'__rank': 1,
       'c': {'environmental': False,
             'normal': True,
             'reading': 'c',
             'relevant': True,
             'status': 'CONSEQUENCE',
             'typ': 'color',
             'value': 'blue',
             'values': ['red', 'blue']},
       'c = blue': {'environmental': False,
                    'normal': False,
                    'reading': 'c = blue',
                    'relevant': True,
                    'status': 'CONSEQUENCE',
                    'typ': 'Bool',
                    'value': True},
       'c = red': {'environmental': False,
                   'normal': False,
                   'reading': 'c = red',
                   'relevant': True,
                   'status': 'CONSEQUENCE',
                   'typ': 'Bool',
                   'value': False},
       'red = c': {'environmental': False,
                   'normal': False,
                   'reading': 'red = c',
                   'relevant': True,
                   'status': 'CONSEQUENCE',
                   'typ': 'Bool',
                   'value': False}},
 'codeOf': {'__rank': 1,
            'codeOf(blue)': {'environmental': False,
                             'normal': True,
                             'reading': 'codeOf(blue)',
                             'relevant': False,
                             'status': 'CONSEQUENCE',
                             'typ': 'code',
                             'value': 'a',
                             'values': ['a', 'b']},
            'codeOf(blue) = a': {'environmental': False,
                                 'normal': False,
                                 'reading': 'codeOf(blue) = a',
                                 'relevant': False,
                                 'status': 'CONSEQUENCE',
                                 'typ': 'Bool',
                                 'value': True},
            'codeOf(blue) = b': {'environmental': False,
                                 'normal': False,
                                 'reading': 'codeOf(blue) = b',
                                 'relevant': False,
                                 'status': 'CONSEQUENCE',
                                 'typ': 'Bool',
                                 'value': False},
            'codeOf(red)': {'environmental': False,
                            'normal': True,
                            'reading': 'codeOf(red)',
                            'relevant': True,
                            'status': 'UNIVERSAL',
                            'typ': 'code',
                            'value': 'b',
                            'values': ['a', 'b']},
            'codeOf(red) = a': {'environmental': False,
                                'normal': False,
                                'reading': 'codeOf(red) = a',
                                'relevant': True,
                                'status': 'CONSEQUENCE',
                                'typ': 'Bool',
                                'value': False},
            'codeOf(red) = b': {'environmental': False,
                                'normal': False,
                                'reading': 'codeOf(red) = b',
                                'relevant': True,
                                'status': 'UNIVERSAL',
                                'typ': 'Bool',
                                'value': True}}}
