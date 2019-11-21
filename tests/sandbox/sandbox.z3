
-- theory
ForAll(c!15,
       (LipLen == c!15) ==
       Or(And(c!15 == Short, JacketDesign == Design_230)))

-- atoms
LipLen
JacketDesign
JacketDesign = Design_230

-- propagation
{'JacketDesign': {'JacketDesign': {'normal': True,
                                   'typ': 'jaDes',
                                   'value': 'Design_230',
                                   'values': ['Design_230', 'Design_400HP']},
                  'JacketDesign = Design_230': {'cf': False, 'ct': True, 'normal': False, 'typ': 'Bool'}},
 'LipLen': {'LipLen': {'normal': True, 'typ': 'lipLen', 'value': 'Short', 'values': ['Short', 'Standard']}}}
