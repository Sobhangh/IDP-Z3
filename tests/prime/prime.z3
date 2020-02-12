ForAll(c!523,
       Implies(Prime(c!523),
               And(And(c!523 >= 1, c!523 <= 4))))
-- theory
ForAll(c!524,
       Prime(c!524) ==
       Or(c!524 == 1, c!524 == 2, c!524 == 3))

-- atoms
Prime(1)
Prime(2)
Prime(3)
Prime(4)

-- case
Type:        
  ForAll(c!523,
       Implies(Prime(c!523),
               And(And(c!523 >= 1, c!523 <= 4))))
Definitions: 
  Rule:∀[][[]]: Prime(1) ⇔($Prime$0 = 1)
Rule:∀[][[]]: Prime(2) ⇔($Prime$0 = 2)
Rule:∀[][[]]: Prime(3) ⇔($Prime$0 = 3)
Rule:∀[][[]]: Prime(4) ⇔(false)
Universals:  
  
Consequences:
  Prime(1)
  Prime(2)
  Prime(3)
  ~Prime(4)
Simplified:  
  
Irrelevant:  
  


-- propagation
{' Global': {'env_dec': False, 'env_done': True},
 'Prime': {'Prime(1)': {'cf': False,
                        'ct': True,
                        'environmental': False,
                        'normal': True,
                        'reading': 'Prime(1)',
                        'relevant': True,
                        'status': 'CONSEQUENCE',
                        'typ': 'Bool',
                        'value': True},
           'Prime(2)': {'cf': False,
                        'ct': True,
                        'environmental': False,
                        'normal': True,
                        'reading': 'Prime(2)',
                        'relevant': True,
                        'status': 'CONSEQUENCE',
                        'typ': 'Bool',
                        'value': True},
           'Prime(3)': {'cf': False,
                        'ct': True,
                        'environmental': False,
                        'normal': True,
                        'reading': 'Prime(3)',
                        'relevant': True,
                        'status': 'CONSEQUENCE',
                        'typ': 'Bool',
                        'value': True},
           'Prime(4)': {'cf': True,
                        'ct': False,
                        'environmental': False,
                        'normal': True,
                        'reading': 'Prime(4)',
                        'relevant': True,
                        'status': 'CONSEQUENCE',
                        'typ': 'Bool',
                        'value': False}}}
