
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

ForAll([c!239, c!240],
       (codeOf(c!239) == c!240) ==
       Or(Or(And(c!239 == red, c!240 == a, red == c),
             And(c!239 == blue, c!240 == a, blue == c),
             And(c!239 == red, c!240 == b, Not(red == c)),
             And(c!239 == blue, c!240 == b, Not(blue == c)))))

-- atoms ------------------------------------
codeOf(red)
codeOf(blue)
c
codeOf(red) = b

-- case -------------------------------------
Type:        
  
Definitions: 
  Rule:∀['$codeOf$0', '$codeOf$'][]: codeOf($codeOf$0,$codeOf$) ⇔((($codeOf$0 = red) ∧ ($codeOf$ = a) ∧ (((red = c)))) ∨ (($codeOf$0 = blue) ∧ ($codeOf$ = a) ∧ (((blue = c)))) ∨ (($codeOf$0 = red) ∧ ($codeOf$ = b) ∧ (((~(red = c))))) ∨ (($codeOf$0 = blue) ∧ ($codeOf$ = b) ∧ (((~(blue = c))))))
Universals:  
  codeOf(red) = b
Consequences:
  codeOf(red) = b
  codeOf(blue) = a
  c = blue
Simplified:  
  
Irrelevant:  
  


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
