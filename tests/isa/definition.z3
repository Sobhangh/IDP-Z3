
-- theory
ForAll([c!332, c!333],
       (codeOf(c!332) == c!333) ==
       Or(And(c!332 == red, c!333 == a),
          And(c!332 == blue, c!333 == b)))

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
{'codeOf': {'codeOf(blue)': {'environmental': False,
                             'irrelevant': False,
                             'normal': True,
                             'reading': 'codeOf(blue)',
                             'status': 'CONSEQUENCE',
                             'typ': 'code',
                             'value': 'b',
                             'values': ['a', 'b']},
            'codeOf(red)': {'environmental': False,
                            'irrelevant': False,
                            'normal': True,
                            'reading': 'codeOf(red)',
                            'status': 'CONSEQUENCE',
                            'typ': 'code',
                            'value': 'a',
                            'values': ['a', 'b']}}}
