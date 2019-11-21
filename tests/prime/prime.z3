ForAll(c!30,
       Implies(Prime(c!30), And(And(c!30 >= 1, c!30 <= 4))))
-- theory
ForAll(c!31,
       Prime(c!31) ==
       Or(c!31 == 1, c!31 == 2, c!31 == 3, False))

-- atoms
Prime(1)
Prime(2)
Prime(3)
Prime(4)

-- propagation
{'Prime': {'Prime(1)': {'cf': False, 'ct': True, 'normal': True, 'typ': 'Bool'},
           'Prime(2)': {'cf': False, 'ct': True, 'normal': True, 'typ': 'Bool'},
           'Prime(3)': {'cf': False, 'ct': True, 'normal': True, 'typ': 'Bool'},
           'Prime(4)': {'cf': True, 'ct': False, 'normal': True, 'typ': 'Bool'}}}
