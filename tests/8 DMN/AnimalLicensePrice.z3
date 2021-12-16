
-- original ---------------------------------


vocabulary {
	type Animalt_t := { Dog }
	Total: ()→Real
	Age: ()→Int
	Animal: ()→Animalt_t
	ViciousDog:() → Bool
	Sterilized:() → Bool
}
theory {
	//Animal License Price
	Total() = sum(lambda : if Age() < 6 & ~(Sterilized()) then 20.0 else 0.0)+sum(lambda : if Age() >= 6 & Sterilized() then 20.0 else 0)+sum(lambda : if Age() >= 6 & ~(Sterilized()) then 40.0 else 0.0)+sum(lambda : if Animal() = Dog & ViciousDog() then 100.0 else 0.0 ).
}


structure {
}

-- meta -------------------------------------
{'manualPropagation': False,
 'manualRelevance': False,
 'optionalPropagation': False,
 'optionalRelevance': False,
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
 'Age': {'Age()': {'environmental': False,
                   'is_assignment': True,
                   'normal': True,
                   'reading': 'Age',
                   'relevant': True,
                   'status': 'UNKNOWN',
                   'typ': 'Int',
                   'value': ''},
         'Age() < 6': {'environmental': False,
                       'is_assignment': False,
                       'normal': False,
                       'reading': 'Age < 6',
                       'relevant': True,
                       'status': 'UNKNOWN',
                       'typ': 'Bool'},
         'Age() ≥ 6': {'environmental': False,
                       'is_assignment': False,
                       'normal': False,
                       'reading': 'Age ≥ 6',
                       'relevant': True,
                       'status': 'UNKNOWN',
                       'typ': 'Bool'}},
 'Animal': {'Animal()': {'environmental': False,
                         'is_assignment': True,
                         'normal': True,
                         'reading': 'Animal',
                         'relevant': True,
                         'status': 'UNIVERSAL',
                         'typ': 'Animalt_t',
                         'value': 'Dog',
                         'values': ['Dog']},
            'Animal() = Dog': {'environmental': False,
                               'is_assignment': True,
                               'normal': False,
                               'reading': 'Animal = Dog',
                               'relevant': True,
                               'status': 'UNIVERSAL',
                               'typ': 'Bool',
                               'value': True}},
 'Sterilized': {'Sterilized()': {'environmental': False,
                                 'is_assignment': False,
                                 'normal': True,
                                 'reading': 'Sterilized',
                                 'relevant': True,
                                 'status': 'UNKNOWN',
                                 'typ': 'Bool'}},
 'Total': {'Total()': {'environmental': False,
                       'is_assignment': True,
                       'normal': True,
                       'reading': 'Total',
                       'relevant': True,
                       'status': 'UNKNOWN',
                       'typ': 'Real',
                       'value': ''},
           'Total() = sum(lambda  :  if   Age() < 6 ∧ ¬((Sterilized())) then 20.0 else 0.0) + sum(lambda  :  if   Age() ≥ 6 ∧ Sterilized() then 20.0 else 0) + sum(lambda  :  if   Age() ≥ 6 ∧ ¬((Sterilized())) then 40.0 else 0.0) + sum(lambda  :  if   Animal() = Dog ∧ ViciousDog() then 100.0 else 0.0)': {'environmental': False,
                                                                                                                                                                                                                                                                                                                 'is_assignment': False,
                                                                                                                                                                                                                                                                                                                 'normal': False,
                                                                                                                                                                                                                                                                                                                 'reading': 'Total '
                                                                                                                                                                                                                                                                                                                            '= '
                                                                                                                                                                                                                                                                                                                            'sum(lambda  '
                                                                                                                                                                                                                                                                                                                            ':  '
                                                                                                                                                                                                                                                                                                                            'if   '
                                                                                                                                                                                                                                                                                                                            'Age '
                                                                                                                                                                                                                                                                                                                            '< '
                                                                                                                                                                                                                                                                                                                            '6 '
                                                                                                                                                                                                                                                                                                                            '∧ '
                                                                                                                                                                                                                                                                                                                            '¬((Sterilized)) '
                                                                                                                                                                                                                                                                                                                            'then '
                                                                                                                                                                                                                                                                                                                            '20.0 '
                                                                                                                                                                                                                                                                                                                            'else '
                                                                                                                                                                                                                                                                                                                            '0.0) '
                                                                                                                                                                                                                                                                                                                            '+ '
                                                                                                                                                                                                                                                                                                                            'sum(lambda  '
                                                                                                                                                                                                                                                                                                                            ':  '
                                                                                                                                                                                                                                                                                                                            'if   '
                                                                                                                                                                                                                                                                                                                            'Age '
                                                                                                                                                                                                                                                                                                                            '≥ '
                                                                                                                                                                                                                                                                                                                            '6 '
                                                                                                                                                                                                                                                                                                                            '∧ '
                                                                                                                                                                                                                                                                                                                            'Sterilized '
                                                                                                                                                                                                                                                                                                                            'then '
                                                                                                                                                                                                                                                                                                                            '20.0 '
                                                                                                                                                                                                                                                                                                                            'else '
                                                                                                                                                                                                                                                                                                                            '0) '
                                                                                                                                                                                                                                                                                                                            '+ '
                                                                                                                                                                                                                                                                                                                            'sum(lambda  '
                                                                                                                                                                                                                                                                                                                            ':  '
                                                                                                                                                                                                                                                                                                                            'if   '
                                                                                                                                                                                                                                                                                                                            'Age '
                                                                                                                                                                                                                                                                                                                            '≥ '
                                                                                                                                                                                                                                                                                                                            '6 '
                                                                                                                                                                                                                                                                                                                            '∧ '
                                                                                                                                                                                                                                                                                                                            '¬((Sterilized)) '
                                                                                                                                                                                                                                                                                                                            'then '
                                                                                                                                                                                                                                                                                                                            '40.0 '
                                                                                                                                                                                                                                                                                                                            'else '
                                                                                                                                                                                                                                                                                                                            '0.0) '
                                                                                                                                                                                                                                                                                                                            '+ '
                                                                                                                                                                                                                                                                                                                            'sum(lambda  '
                                                                                                                                                                                                                                                                                                                            ':  '
                                                                                                                                                                                                                                                                                                                            'if   '
                                                                                                                                                                                                                                                                                                                            'Animal '
                                                                                                                                                                                                                                                                                                                            '= '
                                                                                                                                                                                                                                                                                                                            'Dog '
                                                                                                                                                                                                                                                                                                                            '∧ '
                                                                                                                                                                                                                                                                                                                            'ViciousDog '
                                                                                                                                                                                                                                                                                                                            'then '
                                                                                                                                                                                                                                                                                                                            '100.0 '
                                                                                                                                                                                                                                                                                                                            'else '
                                                                                                                                                                                                                                                                                                                            '0.0)',
                                                                                                                                                                                                                                                                                                                 'relevant': True,
                                                                                                                                                                                                                                                                                                                 'status': 'UNIVERSAL',
                                                                                                                                                                                                                                                                                                                 'typ': 'Bool',
                                                                                                                                                                                                                                                                                                                 'value': True}},
 'ViciousDog': {'ViciousDog()': {'environmental': False,
                                 'is_assignment': False,
                                 'normal': True,
                                 'reading': 'ViciousDog',
                                 'relevant': True,
                                 'status': 'UNKNOWN',
                                 'typ': 'Bool'}}}
