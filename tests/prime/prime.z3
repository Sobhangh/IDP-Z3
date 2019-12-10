ForAll(c!589,
       Implies(Prime(c!589),
               And(And(c!589 >= 1, c!589 <= 4))))
-- theory
ForAll(c!590,
       Prime(c!590) ==
       Or(c!590 == 1, c!590 == 2, c!590 == 3))

-- atoms
Prime(1)
Prime(2)
Prime(3)
Prime(4)

-- case
Type:        
  ForAll(c!589,
       Implies(Prime(c!589),
               And(And(c!589 >= 1, c!589 <= 4))))
Definitions: 
  Rule:∀[][[]]: Prime(1) ⇔($Prime$0 = 1)
Rule:∀[][[]]: Prime(2) ⇔($Prime$0 = 2)
Rule:∀[][[]]: Prime(3) ⇔($Prime$0 = 3)
Rule:∀[][[]]: Prime(4) ⇔(false)
Universals:  
  
Consequences:
  
Simplified:  
  
Irrelevant:  
  


-- propagation
{'Prime': {'Prime(1)': {'cf': False,
                        'ct': True,
                        'irrelevant': False,
                        'normal': True,
                        'reading': 'Prime(1)',
                        'typ': 'Bool'},
           'Prime(2)': {'cf': False,
                        'ct': True,
                        'irrelevant': False,
                        'normal': True,
                        'reading': 'Prime(2)',
                        'typ': 'Bool'},
           'Prime(3)': {'cf': False,
                        'ct': True,
                        'irrelevant': False,
                        'normal': True,
                        'reading': 'Prime(3)',
                        'typ': 'Bool'},
           'Prime(4)': {'cf': True,
                        'ct': False,
                        'irrelevant': False,
                        'normal': True,
                        'reading': 'Prime(4)',
                        'typ': 'Bool'}}}
