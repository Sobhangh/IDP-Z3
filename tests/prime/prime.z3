ForAll(c!334,
       Implies(Prime(c!334),
               And(And(c!334 >= 1, c!334 <= 4))))
-- theory
ForAll(c!335,
       Prime(c!335) ==
       Or(c!335 == 1, c!335 == 2, c!335 == 3))

-- atoms
Prime(1)
Prime(2)
Prime(3)
Prime(4)

-- case
Type:        
  ForAll(c!334,
       Implies(Prime(c!334),
               And(And(c!334 >= 1, c!334 <= 4))))
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
{'Prime': {'Prime(1)': {'cf': False,
                        'ct': True,
                        'environmental': False,
                        'irrelevant': False,
                        'normal': True,
                        'reading': 'Prime(1)',
                        'status': 'CONSEQUENCE',
                        'typ': 'Bool',
                        'value': True},
           'Prime(2)': {'cf': False,
                        'ct': True,
                        'environmental': False,
                        'irrelevant': False,
                        'normal': True,
                        'reading': 'Prime(2)',
                        'status': 'CONSEQUENCE',
                        'typ': 'Bool',
                        'value': True},
           'Prime(3)': {'cf': False,
                        'ct': True,
                        'environmental': False,
                        'irrelevant': False,
                        'normal': True,
                        'reading': 'Prime(3)',
                        'status': 'CONSEQUENCE',
                        'typ': 'Bool',
                        'value': True},
           'Prime(4)': {'cf': True,
                        'ct': False,
                        'environmental': False,
                        'irrelevant': False,
                        'normal': True,
                        'reading': 'Prime(4)',
                        'status': 'CONSEQUENCE',
                        'typ': 'Bool',
                        'value': False}}}
