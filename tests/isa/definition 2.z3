
-- theory
codeOf(red) == b

ForAll([c!511, c!512],
       (codeOf(c!511) == c!512) ==
       Or(And(c!511 == red, c!512 == a, red == c),
          And(c!511 == blue, c!512 == a, blue == c),
          And(c!511 == red, c!512 == b, Not(red == c)),
          And(c!511 == blue, c!512 == b, Not(blue == c))))

-- atoms
codeOf(red)
codeOf(blue)
c
codeOf(red) = b

-- case
Type:        
  
Definitions: 
  Rule:∀[][[]]: codeOf(red,a) ⇔($codeOf$0 = red) ∧ ($codeOf$ = a) ∧ (((red = c)))
Rule:∀[][[]]: codeOf(blue,a) ⇔($codeOf$0 = blue) ∧ ($codeOf$ = a) ∧ (((blue = c)))
Rule:∀[][[]]: codeOf(red,b) ⇔($codeOf$0 = red) ∧ ($codeOf$ = b) ∧ (((~(red = c))))
Rule:∀[][[]]: codeOf(blue,b) ⇔($codeOf$0 = blue) ∧ ($codeOf$ = b) ∧ (((~(blue = c))))
Universals:  
  codeOf(red) = b
Consequences:
  codeOf(red) = b
  codeOf(blue) = a
  c = blue
Simplified:  
  
Irrelevant:  
  


-- propagation
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
