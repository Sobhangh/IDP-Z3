
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
    (codeOf(blue) == a) == (blue == c),
    (codeOf(red) == b) == Not(red == c),
    (codeOf(blue) == b) == Not(blue == c))

-- subtences ------------------------------------
codeOf(red) = b

-- GUILines ------------------------------------
codeOf(red)
codeOf(blue)
c
codeOf(red) = b

-- case -------------------------------------
Type:        
  
Definitions: 
  Rule:∀['$codeOf!0$', '$codeOf$'][]: codeOf($codeOf!0$,$codeOf$) ⇔(($codeOf!0$ = c) ∧ ($codeOf$ = a)) ∨ ((~($codeOf!0$ = c)) ∧ ($codeOf$ = b))
Universals:  
  codeOf(red) = b
Consequences:
  codeOf(red) = b
  codeOf(blue) = a
  c = blue
Simplified:  
  
Irrelevant:  
  


-- meta -------------------------------------
{'title': 'Interactive Consultant', 'symbols': [{'idpname': 'codeOf', 'type': 'function', 'priority': 'core', 'showOptimize': True, 'view': 'expanded'}, {'idpname': 'c', 'type': 'function', 'priority': 'core', 'showOptimize': True, 'view': 'expanded'}]}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'c': {'c': {'environmental': False,
             'normal': True,
             'reading': 'c',
             'relevant': True,
             'status': 'CONSEQUENCE',
             'typ': 'color',
             'value': 'blue',
             'values': ['red', 'blue']}},
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
                            'status': 'CONSEQUENCE',
                            'typ': 'code',
                            'value': 'b',
                            'values': ['a', 'b']},
            'codeOf(red) = b': {'environmental': False,
                                'normal': False,
                                'reading': 'codeOf(red) = b',
                                'relevant': True,
                                'status': 'UNIVERSAL',
                                'typ': 'Bool',
                                'value': True}}}
