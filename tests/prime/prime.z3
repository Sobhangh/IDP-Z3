ForAll(c!371,
       Implies(Prime(c!371),
               And(And(c!371 >= 1, c!371 <= 4))))
-- theory
ForAll(c!372,
       Prime(c!372) ==
       Or(c!372 == 1, c!372 == 2, c!372 == 3))

-- atoms
Prime(1)
Prime(2)
Prime(3)
Prime(4)

-- case
Type:        
  ForAll(c!371,
       Implies(Prime(c!371),
               And(And(c!371 >= 1, c!371 <= 4))))
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
