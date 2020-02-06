
-- theory
ForAll([c!330, c!331],
       (codeOf(c!330) == c!331) ==
       Or(And(c!330 == red, c!331 == a),
          And(c!330 == blue, c!331 == b)))

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
