ForAll(c!462,
       Implies(Prime(c!462),
               And(And(c!462 >= 1, c!462 <= 4))))
-- theory
ForAll(c!463,
       Prime(c!463) ==
       Or(c!463 == 1, c!463 == 2, c!463 == 3))

-- atoms
Prime(1)
Prime(2)
Prime(3)
Prime(4)

-- case
Type:        
  ForAll(c!462,
       Implies(Prime(c!462),
               And(And(c!462 >= 1, c!462 <= 4))))
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
