ForAll(c!226,
       Implies(Prime(c!226),
               And(And(c!226 >= 1, c!226 <= 4))))
-- theory
ForAll(c!227,
       Prime(c!227) ==
       Or(c!227 == 1, c!227 == 2, c!227 == 3, False))

-- atoms
Prime(1)
Prime(2)
Prime(3)
Prime(4)

-- case
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
