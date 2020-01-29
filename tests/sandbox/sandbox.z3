
-- theory
ForAll(c!316,
       (LipLen == c!316) ==
       Or(And(c!316 == Short, JacketDesign == Design_230)))

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
  LipLen = Short
  JacketDesign = Design_230
Simplified:  
  
Irrelevant:  
  


-- propagation
{'JacketDesign': {'JacketDesign': {'environmental': False,
                                   'irrelevant': False,
                                   'normal': True,
                                   'reading': 'JacketDesign',
                                   'status': 'CONSEQUENCE',
                                   'typ': 'jaDes',
                                   'value': 'Design_230',
                                   'values': ['Design_230', 'Design_400HP']},
                  'JacketDesign = Design_230': {'cf': False,
                                                'ct': True,
                                                'environmental': False,
                                                'irrelevant': False,
                                                'normal': False,
                                                'reading': 'JacketDesign = Design_230',
                                                'status': 'CONSEQUENCE',
                                                'typ': 'Bool',
                                                'value': True}},
 'LipLen': {'LipLen': {'environmental': False,
                       'irrelevant': False,
                       'normal': True,
                       'reading': 'LipLen',
                       'status': 'CONSEQUENCE',
                       'typ': 'lipLen',
                       'value': 'Short',
                       'values': ['Short', 'Standard']}}}
