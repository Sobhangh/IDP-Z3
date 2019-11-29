
-- theory
ForAll(c!117,
       (LipLen == c!117) ==
       Or(And(c!117 == Short, JacketDesign == Design_230)))

-- atoms
LipLen
JacketDesign
JacketDesign = Design_230

-- case
Definitions:
  Rule:∀[][[]]: LipLen(Short) ⇔$LipLen$ = Short ∧ JacketDesign = Design_230
Universals:
  
Consequences:
  
Simplified:
  


-- propagation
{'JacketDesign': {'JacketDesign': {'normal': True,
                                   'reading': 'JacketDesign',
                                   'typ': 'jaDes',
                                   'value': 'Design_230',
                                   'values': ['Design_230', 'Design_400HP']},
                  'JacketDesign = Design_230': {'cf': False,
                                                'ct': True,
                                                'normal': False,
                                                'reading': 'JacketDesign = Design_230',
                                                'typ': 'Bool'}},
 'LipLen': {'LipLen': {'normal': True,
                       'reading': 'LipLen',
                       'typ': 'lipLen',
                       'value': 'Short',
                       'values': ['Short', 'Standard']}}}
