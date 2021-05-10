
-- original ---------------------------------


vocabulary {
	price: ()→Real
	age: ()→Real
	priority:() → Bool
}
theory {
	//Calculate Price Decision
	price() = sum{ : age() < 2: 0 }+sum{ : 3 =< age() & age() =< 16: 20 }+sum{ : age() >= 16: 40 }+sum{ : priority(): 10 }.
}


structure {
}

-- meta -------------------------------------
{'manualPropagation': False,
 'optionalPropagation': False,
 'symbols': [{'environmental': False,
              'idpname': 'price',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'age',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'priority',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'age': {'3 ≤ age()': {'environmental': False,
                       'is_assignment': False,
                       'normal': False,
                       'reading': '3 ≤ age',
                       'relevant': True,
                       'status': 'UNKNOWN',
                       'typ': 'Bool'},
         '__rank': 9999,
         'age()': {'environmental': False,
                   'is_assignment': True,
                   'normal': True,
                   'reading': 'age',
                   'relevant': True,
                   'status': 'UNKNOWN',
                   'typ': 'Real',
                   'value': ''},
         'age() < 2': {'environmental': False,
                       'is_assignment': False,
                       'normal': False,
                       'reading': 'age < 2',
                       'relevant': True,
                       'status': 'UNKNOWN',
                       'typ': 'Bool'},
         'age() ≤ 16': {'environmental': False,
                        'is_assignment': False,
                        'normal': False,
                        'reading': 'age ≤ 16',
                        'relevant': True,
                        'status': 'UNKNOWN',
                        'typ': 'Bool'},
         'age() ≥ 16': {'environmental': False,
                        'is_assignment': False,
                        'normal': False,
                        'reading': 'age ≥ 16',
                        'relevant': True,
                        'status': 'UNKNOWN',
                        'typ': 'Bool'}},
 'price': {'__rank': 9999,
           'price()': {'environmental': False,
                       'is_assignment': True,
                       'normal': True,
                       'reading': 'price',
                       'relevant': True,
                       'status': 'UNKNOWN',
                       'typ': 'Real',
                       'value': ''},
           'price() = sum{ : age() < 2 : 0} + sum{ : 3 ≤ age() ∧ age() ≤ 16 : 20} + sum{ : age() ≥ 16 : 40} + sum{ : priority() : 10}': {'environmental': False,
                                                                                                                                         'is_assignment': False,
                                                                                                                                         'normal': False,
                                                                                                                                         'reading': 'price '
                                                                                                                                                    '= '
                                                                                                                                                    'sum{ '
                                                                                                                                                    ': '
                                                                                                                                                    'age '
                                                                                                                                                    '< '
                                                                                                                                                    '2 '
                                                                                                                                                    ': '
                                                                                                                                                    '0} '
                                                                                                                                                    '+ '
                                                                                                                                                    'sum{ '
                                                                                                                                                    ': '
                                                                                                                                                    '3 '
                                                                                                                                                    '≤ '
                                                                                                                                                    'age '
                                                                                                                                                    '∧ '
                                                                                                                                                    'age '
                                                                                                                                                    '≤ '
                                                                                                                                                    '16 '
                                                                                                                                                    ': '
                                                                                                                                                    '20} '
                                                                                                                                                    '+ '
                                                                                                                                                    'sum{ '
                                                                                                                                                    ': '
                                                                                                                                                    'age '
                                                                                                                                                    '≥ '
                                                                                                                                                    '16 '
                                                                                                                                                    ': '
                                                                                                                                                    '40} '
                                                                                                                                                    '+ '
                                                                                                                                                    'sum{ '
                                                                                                                                                    ': '
                                                                                                                                                    'priority '
                                                                                                                                                    ': '
                                                                                                                                                    '10}',
                                                                                                                                         'relevant': True,
                                                                                                                                         'status': 'UNIVERSAL',
                                                                                                                                         'typ': 'Bool',
                                                                                                                                         'value': True}},
 'priority': {'__rank': 9999,
              'priority()': {'environmental': False,
                             'is_assignment': False,
                             'normal': True,
                             'reading': 'priority',
                             'relevant': True,
                             'status': 'UNKNOWN',
                             'typ': 'Bool'}}}
