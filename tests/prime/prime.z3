ForAll(c!200,
       Implies(Prime(c!200),
               And(And(c!200 >= 1, c!200 <= 4))))
-- theory
ForAll(c!201,
       Prime(c!201) ==
       Or(c!201 == 1, c!201 == 2, c!201 == 3, False))

-- atoms
Prime(1)
Prime(2)
Prime(3)
Prime(4)

-- case
Type:        
  ForAll(c!200,
       Implies(Prime(c!200),
               And(And(c!200 >= 1, c!200 <= 4))))
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
