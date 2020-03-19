
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
ForAll([c!0, c!1],
       (codeOf(c!0) == c!1) ==
       Or(And(c!0 == red, c!1 == a),
          And(c!0 == blue, c!1 == b)))

-- atoms ------------------------------------
codeOf(red)
codeOf(blue)

-- case -------------------------------------
Type:        
  
Definitions: 
  Rule:∀[][[]]: codeOf(red,a) ⇔($codeOf$0 = red) ∧ ($codeOf$ = a)
Rule:∀[][[]]: codeOf(blue,a) ⇔(false)
Rule:∀[][[]]: codeOf(red,b) ⇔(false)
Rule:∀[][[]]: codeOf(blue,b) ⇔($codeOf$0 = blue) ∧ ($codeOf$ = b)
Universals:  
  
Consequences:
  codeOf(red) = a
  codeOf(blue) = b
Simplified:  
  
Irrelevant:  
  


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
