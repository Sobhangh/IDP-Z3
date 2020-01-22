
-- theory
ForAll(c!584,
       (LipLen == c!584) ==
       Or(And(c!584 == Short, JacketDesign == Design_230)))

-- atoms
LipLen
JacketDesign
JacketDesign = Design_230

-- case
Type:        
  
Definitions: 
  Rule:∀[][[]]: LipLen(Short) ⇔($LipLen$ = Short) ∧ (JacketDesign = Design_230)
Universals:  
  
Consequences:
  JacketDesign = Design_230
Simplified:  
  
Irrelevant:  
  


-- propagation
{'JacketDesign': {'JacketDesign': {'normal': True,
                                   'reading': 'JacketDesign',
                                   'typ': 'jaDes',
                                   'value': 'Design_230',
                                   'values': ['Design_230', 'Design_400HP']},
                  'JacketDesign = Design_230': {'cf': False,
                                                'ct': True,
                                                'irrelevant': False,
                                                'normal': False,
                                                'reading': 'JacketDesign = Design_230',
                                                'typ': 'Bool'}},
 'LipLen': {'LipLen': {'normal': True,
                       'reading': 'LipLen',
                       'typ': 'lipLen',
                       'value': 'Short',
                       'values': ['Short', 'Standard']}}}
