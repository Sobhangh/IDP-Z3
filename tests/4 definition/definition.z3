
-- original ---------------------------------
vocabulary {
    type color constructed from {red, blue}
    type code constructed from {a,b}
    codeOf(color): code
} 

theory {
    { !cl[color]: ! cd[code]: codeOf(cl)=cd <- (cl=red & cd=a) | (cl=blue & cd=b). }
}
 
view expanded

-- vocabulary -------------------------------

-- theory -----------------------------------
Or(codeOf(red) == a, codeOf(red) == b)

Or(codeOf(blue) == a, codeOf(blue) == b)

And(codeOf(red) == a,
    Not(codeOf(red) == b),
    Not(codeOf(blue) == a),
    codeOf(blue) == b)

-- subtences ------------------------------------
codeOf(red) = a
codeOf(red) = b
codeOf(blue) = a
codeOf(blue) = b

-- GUILines ------------------------------------
codeOf(red)
codeOf(blue)
codeOf(red) = a
codeOf(red) = b
codeOf(blue) = a
codeOf(blue) = b

-- case -------------------------------------
Type:        
  
Definitions: 
  Rule:∀$codeOf!0$[color],$codeOf$[code]: codeOf($codeOf!0$,$codeOf$) ⇔($codeOf!0$ = red ∧ $codeOf$ = a) ∨ ($codeOf!0$ = blue ∧ $codeOf$ = b)
Universals:  
  
Consequences:
  codeOf(red) -> a
  codeOf(blue) -> b
  codeOf(red) = a
  ~codeOf(red) = b
  ~codeOf(blue) = a
  codeOf(blue) = b
Simplified:  
  
Irrelevant:  
  codeOf(red) -> a
  codeOf(blue) -> b
  codeOf(red) = a
  ~codeOf(red) = b
  ~codeOf(blue) = a
  codeOf(blue) = b
Co-constraints:
  


-- meta -------------------------------------
{'symbols': [{'idpname': 'codeOf', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'codeOf': {'__rank': 9999,
            'codeOf(blue)': {'environmental': False,
                             'normal': True,
                             'reading': 'codeOf(blue)',
                             'relevant': False,
                             'status': 'CONSEQUENCE',
                             'typ': 'code',
                             'value': 'b',
                             'values': ['a', 'b']},
            'codeOf(blue) = a': {'environmental': False,
                                 'normal': False,
                                 'reading': 'codeOf(blue) = a',
                                 'relevant': False,
                                 'status': 'CONSEQUENCE',
                                 'typ': 'Bool',
                                 'value': False},
            'codeOf(blue) = b': {'environmental': False,
                                 'normal': False,
                                 'reading': 'codeOf(blue) = b',
                                 'relevant': False,
                                 'status': 'CONSEQUENCE',
                                 'typ': 'Bool',
                                 'value': True},
            'codeOf(red)': {'environmental': False,
                            'normal': True,
                            'reading': 'codeOf(red)',
                            'relevant': False,
                            'status': 'CONSEQUENCE',
                            'typ': 'code',
                            'value': 'a',
                            'values': ['a', 'b']},
            'codeOf(red) = a': {'environmental': False,
                                'normal': False,
                                'reading': 'codeOf(red) = a',
                                'relevant': False,
                                'status': 'CONSEQUENCE',
                                'typ': 'Bool',
                                'value': True},
            'codeOf(red) = b': {'environmental': False,
                                'normal': False,
                                'reading': 'codeOf(red) = b',
                                'relevant': False,
                                'status': 'CONSEQUENCE',
                                'typ': 'Bool',
                                'value': False}}}
