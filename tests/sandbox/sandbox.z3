
-- theory
ForAll(c!460,
       (LipLen == c!460) ==
       Or(And(c!460 == Short, JacketDesign == Design_230)))

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
{' Global': {'env_dec': False},
 'JacketDesign': {'JacketDesign': {'environmental': False,
                                   'normal': True,
                                   'reading': 'JacketDesign',
                                   'relevant': True,
                                   'status': 'CONSEQUENCE',
                                   'typ': 'jaDes',
                                   'value': 'Design_230',
                                   'values': ['Design_230', 'Design_400HP']},
                  'JacketDesign = Design_230': {'environmental': False,
                                                'normal': False,
                                                'reading': 'JacketDesign = Design_230',
                                                'relevant': True,
                                                'status': 'CONSEQUENCE',
                                                'typ': 'Bool',
                                                'value': True}},
 'LipLen': {'LipLen': {'environmental': False,
                       'normal': True,
                       'reading': 'LipLen',
                       'relevant': True,
                       'status': 'CONSEQUENCE',
                       'typ': 'lipLen',
                       'value': 'Short',
                       'values': ['Short', 'Standard']}}}
