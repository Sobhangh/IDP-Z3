
-- original ---------------------------------


vocabulary {
	type Animalt_t constructed from { Dog } 
	Total: real
	Age: int
	Animal: Animalt_t
	ViciousDog
	Sterilized
}
theory {
	//Animal License Price
	Total() = sum{ : Age() < 6 & ~(Sterilized()): 20.0 }+sum{ : Age() >= 6 & Sterilized(): 20.0 }+sum{ : Age() >= 6 & ~(Sterilized()): 40.0 }+sum{ : Animal() = Dog & ViciousDog(): 100.0 }.
}


structure {
}

-- meta -------------------------------------
{'optionalPropagation': False,
 'symbols': [{'environmental': False,
              'idpname': 'Total',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Age',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Animal',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'ViciousDog',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Sterilized',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'Age': {'Age': {'environmental': False,
                 'is_assignment': True,
                 'normal': True,
                 'reading': 'Age',
                 'relevant': True,
                 'status': 'UNKNOWN',
                 'typ': 'Int',
                 'value': ''},
         'Age < 6': {'environmental': False,
                     'is_assignment': False,
                     'normal': False,
                     'reading': 'Age < 6',
                     'relevant': True,
                     'status': 'UNKNOWN',
                     'typ': 'Bool'},
         'Age ≥ 6': {'environmental': False,
                     'is_assignment': False,
                     'normal': False,
                     'reading': 'Age ≥ 6',
                     'relevant': True,
                     'status': 'UNKNOWN',
                     'typ': 'Bool'},
         '__rank': 1},
 'Animal': {'Animal': {'environmental': False,
                       'is_assignment': True,
                       'normal': True,
                       'reading': 'Animal',
                       'relevant': True,
                       'status': 'UNIVERSAL',
                       'typ': 'Animalt_t',
                       'value': 'Dog',
                       'values': ['Dog']},
            'Animal = Dog': {'environmental': False,
                             'is_assignment': True,
                             'normal': False,
                             'reading': 'Animal = Dog',
                             'relevant': True,
                             'status': 'UNIVERSAL',
                             'typ': 'Bool',
                             'value': True},
            '__rank': 1},
 'Sterilized': {'Sterilized': {'environmental': False,
                               'is_assignment': False,
                               'normal': True,
                               'reading': 'Sterilized',
                               'relevant': True,
                               'status': 'UNKNOWN',
                               'typ': 'Bool'},
                '__rank': 1},
 'Total': {'Total': {'environmental': False,
                     'is_assignment': True,
                     'normal': True,
                     'reading': 'Total',
                     'relevant': True,
                     'status': 'UNKNOWN',
                     'typ': 'Real',
                     'value': ''},
           'Total = sum{ : Age < 6 ∧ ¬((Sterilized)) : 20.0} + sum{ : Age ≥ 6 ∧ Sterilized : 20.0} + sum{ : Age ≥ 6 ∧ ¬((Sterilized)) : 40.0} + sum{ : Animal = Dog ∧ ViciousDog : 100.0}': {'environmental': False,
                                                                                                                                                                                             'is_assignment': False,
                                                                                                                                                                                             'normal': False,
                                                                                                                                                                                             'reading': 'Total '
                                                                                                                                                                                                        '= '
                                                                                                                                                                                                        'sum{ '
                                                                                                                                                                                                        ': '
                                                                                                                                                                                                        'Age '
                                                                                                                                                                                                        '< '
                                                                                                                                                                                                        '6 '
                                                                                                                                                                                                        '∧ '
                                                                                                                                                                                                        '¬((Sterilized)) '
                                                                                                                                                                                                        ': '
                                                                                                                                                                                                        '20.0} '
                                                                                                                                                                                                        '+ '
                                                                                                                                                                                                        'sum{ '
                                                                                                                                                                                                        ': '
                                                                                                                                                                                                        'Age '
                                                                                                                                                                                                        '≥ '
                                                                                                                                                                                                        '6 '
                                                                                                                                                                                                        '∧ '
                                                                                                                                                                                                        'Sterilized '
                                                                                                                                                                                                        ': '
                                                                                                                                                                                                        '20.0} '
                                                                                                                                                                                                        '+ '
                                                                                                                                                                                                        'sum{ '
                                                                                                                                                                                                        ': '
                                                                                                                                                                                                        'Age '
                                                                                                                                                                                                        '≥ '
                                                                                                                                                                                                        '6 '
                                                                                                                                                                                                        '∧ '
                                                                                                                                                                                                        '¬((Sterilized)) '
                                                                                                                                                                                                        ': '
                                                                                                                                                                                                        '40.0} '
                                                                                                                                                                                                        '+ '
                                                                                                                                                                                                        'sum{ '
                                                                                                                                                                                                        ': '
                                                                                                                                                                                                        'Animal '
                                                                                                                                                                                                        '= '
                                                                                                                                                                                                        'Dog '
                                                                                                                                                                                                        '∧ '
                                                                                                                                                                                                        'ViciousDog '
                                                                                                                                                                                                        ': '
                                                                                                                                                                                                        '100.0}',
                                                                                                                                                                                             'relevant': True,
                                                                                                                                                                                             'status': 'UNIVERSAL',
                                                                                                                                                                                             'typ': 'Bool',
                                                                                                                                                                                             'value': True},
           '__rank': 1},
 'ViciousDog': {'ViciousDog': {'environmental': False,
                               'is_assignment': False,
                               'normal': True,
                               'reading': 'ViciousDog',
                               'relevant': True,
                               'status': 'UNKNOWN',
                               'typ': 'Bool'},
                '__rank': 1}}
