
-- theory
ForAll([c!484, c!485],
       (codeOf(c!484) == c!485) ==
       Or(And(c!484 == red, c!485 == a),
          And(c!484 == blue, c!485 == b)))

-- atoms
codeOf(red)
codeOf(blue)

-- case
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
  


-- propagation
{' Global': {'env_dec': False, 'env_done': True},
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
