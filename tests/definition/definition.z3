
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
And(codeOf(red) == a,
    Not(codeOf(red) == b),
    Not(codeOf(blue) == a),
    codeOf(blue) == b)

-- subtences ------------------------------------


-- GUILines ------------------------------------
codeOf(red)
codeOf(blue)

-- case -------------------------------------
Type:        
  
Definitions: 
  Rule:∀['$codeOf!0$', '$codeOf$'][]: codeOf($codeOf!0$,$codeOf$) ⇔(($codeOf!0$ = red) ∧ ($codeOf$ = a)) ∨ (($codeOf!0$ = blue) ∧ ($codeOf$ = b))
Universals:  
  
Consequences:
  codeOf(red) = a <= Z3 proof
  codeOf(blue) = b <= Z3 proof
Simplified:  
  
Irrelevant:  
  


-- meta -------------------------------------
{'symbols': [{'idpname': 'codeOf', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'codeOf': {'codeOf(blue)': {'environmental': False,
                             'normal': True,
                             'reading': 'codeOf(blue)',
                             'relevant': True,
                             'status': 'CONSEQUENCE',
                             'typ': 'code',
                             'value': 'b',
                             'values': ['a', 'b']},
            'codeOf(red)': {'environmental': False,
                            'normal': True,
                            'reading': 'codeOf(red)',
                            'relevant': True,
                            'status': 'CONSEQUENCE',
                            'typ': 'code',
                            'value': 'a',
                            'values': ['a', 'b']}}}
