ForAll(c!132,
       Implies(Prime(c!132),
               And(And(c!132 >= 1, c!132 <= 4))))
-- theory
ForAll(c!133,
       Prime(c!133) ==
       Or(c!133 == 1, c!133 == 2, c!133 == 3, False))

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
  


-- propagation
{'Prime': {'Prime(1)': {'cf': False, 'ct': True, 'normal': True, 'reading': 'Prime(1)', 'typ': 'Bool'},
           'Prime(2)': {'cf': False, 'ct': True, 'normal': True, 'reading': 'Prime(2)', 'typ': 'Bool'},
           'Prime(3)': {'cf': False, 'ct': True, 'normal': True, 'reading': 'Prime(3)', 'typ': 'Bool'},
           'Prime(4)': {'cf': True, 'ct': False, 'normal': True, 'reading': 'Prime(4)', 'typ': 'Bool'}}}
