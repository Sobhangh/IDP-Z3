
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

And((codeOf(red) == a) == (red == c),
    (codeOf(red) == b) == Not(red == c),
    (codeOf(blue) == a) == (blue == c),
    (codeOf(blue) == b) == Not(blue == c))

-- subtences ------------------------------------
codeOf(red) = b
red = c
codeOf(red) = a

-- GUILines ------------------------------------
codeOf(red)
codeOf(blue)
c
codeOf(red) = b
red = c
codeOf(red) = a

-- case -------------------------------------
Type:        
  
Definitions: 
  Rule:∀['$codeOf!0$', '$codeOf$'][]: codeOf($codeOf!0$,$codeOf$) ⇔(($codeOf!0$ = c) ∧ ($codeOf$ = a)) ∨ ((~($codeOf!0$ = c)) ∧ ($codeOf$ = b))
Universals:  
  codeOf(red) = b
  codeOf(red) = b
Consequences:
  ~red = c <= Z3 proof
  ~codeOf(red) = a <= {'codeOf(red)'}
  codeOf(blue) = a <= Z3 proof
  c = blue <= Z3 proof
Simplified:  
  
Irrelevant:  
  ~codeOf(red) = a <= {'codeOf(red)'}


-- meta -------------------------------------
{'symbols': [{'idpname': 'codeOf', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'},
             {'idpname': 'c', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'c': {'c': {'environmental': False,
             'normal': True,
             'reading': 'c',
             'relevant': True,
             'status': 'CONSEQUENCE',
             'typ': 'color',
             'value': 'blue',
             'values': ['red', 'blue']},
       'red = c': {'environmental': False,
                   'normal': False,
                   'reading': 'cl = c',
                   'relevant': True,
                   'status': 'CONSEQUENCE',
                   'typ': 'Bool',
                   'value': False}},
 'codeOf': {'codeOf(blue)': {'environmental': False,
                             'normal': True,
                             'reading': 'codeOf(blue)',
                             'relevant': True,
                             'status': 'CONSEQUENCE',
                             'typ': 'code',
                             'value': 'a',
                             'values': ['a', 'b']},
            'codeOf(red)': {'environmental': False,
                            'normal': True,
                            'reading': 'codeOf(red)',
                            'relevant': True,
                            'status': 'UNIVERSAL',
                            'typ': 'code',
                            'value': '',
                            'values': ['a', 'b']},
            'codeOf(red) = a': {'environmental': False,
                                'normal': False,
                                'reading': 'cd = a',
                                'relevant': False,
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
