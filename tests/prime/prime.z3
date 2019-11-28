ForAll(c!47,
       Implies(Prime(c!47), And(And(c!47 >= 1, c!47 <= 4))))
-- theory
ForAll(c!48,
       Prime(c!48) ==
       Or(c!48 == 1, c!48 == 2, c!48 == 3, False))

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
