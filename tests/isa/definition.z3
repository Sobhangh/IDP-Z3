
-- theory
ForAll([c!473, c!474],
       (codeOf(c!473) == c!474) ==
       Or(And(c!473 == red, c!474 == a),
          And(c!473 == blue, c!474 == b)))

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
