
-- original ---------------------------------


vocabulary {
	price: ()→Real
	age: ()→Real
	priority:() → Bool
}
theory {
	//Calculate Price Decision
	price() = sum(lambda : if age() < 2 then 0 else 0)+sum(lambda : if 3 =< age() & age() =< 16 then 20 else 0)+sum(lambda : if age() >= 16 then 40 else 0)+sum(lambda : if priority() then 10 else 0).
}


structure {
}

-- meta -------------------------------------
{'manualPropagation': False,
 'manualRelevance': False,
 'optionalPropagation': False,
 'optionalRelevance': False,
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
 'price': {'price()': {'environmental': False,
                       'is_assignment': True,
                       'normal': True,
                       'reading': 'price',
                       'relevant': True,
                       'status': 'UNKNOWN',
                       'typ': 'Real',
                       'value': ''},
           'price() = sum(lambda  : if age() < 2 then 0 else 0) + sum(lambda  : if 3 ≤ age() ∧ age() ≤ 16 then 20 else 0) + sum(lambda  : if age() ≥ 16 then 40 else 0) + sum(lambda  : if priority() then 10 else 0)': {'environmental': False,
                                                                                                                                                                                                                         'is_assignment': False,
                                                                                                                                                                                                                         'normal': False,
                                                                                                                                                                                                                         'reading': 'price '
                                                                                                                                                                                                                                    '= '
                                                                                                                                                                                                                                    'sum(lambda  '
                                                                                                                                                                                                                                    ': '
                                                                                                                                                                                                                                    'if '
                                                                                                                                                                                                                                    'age '
                                                                                                                                                                                                                                    '< '
                                                                                                                                                                                                                                    '2 '
                                                                                                                                                                                                                                    'then '
                                                                                                                                                                                                                                    '0 '
                                                                                                                                                                                                                                    'else '
                                                                                                                                                                                                                                    '0) '
                                                                                                                                                                                                                                    '+ '
                                                                                                                                                                                                                                    'sum(lambda  '
                                                                                                                                                                                                                                    ': '
                                                                                                                                                                                                                                    'if '
                                                                                                                                                                                                                                    '3 '
                                                                                                                                                                                                                                    '≤ '
                                                                                                                                                                                                                                    'age '
                                                                                                                                                                                                                                    '∧ '
                                                                                                                                                                                                                                    'age '
                                                                                                                                                                                                                                    '≤ '
                                                                                                                                                                                                                                    '16 '
                                                                                                                                                                                                                                    'then '
                                                                                                                                                                                                                                    '20 '
                                                                                                                                                                                                                                    'else '
                                                                                                                                                                                                                                    '0) '
                                                                                                                                                                                                                                    '+ '
                                                                                                                                                                                                                                    'sum(lambda  '
                                                                                                                                                                                                                                    ': '
                                                                                                                                                                                                                                    'if '
                                                                                                                                                                                                                                    'age '
                                                                                                                                                                                                                                    '≥ '
                                                                                                                                                                                                                                    '16 '
                                                                                                                                                                                                                                    'then '
                                                                                                                                                                                                                                    '40 '
                                                                                                                                                                                                                                    'else '
                                                                                                                                                                                                                                    '0) '
                                                                                                                                                                                                                                    '+ '
                                                                                                                                                                                                                                    'sum(lambda  '
                                                                                                                                                                                                                                    ': '
                                                                                                                                                                                                                                    'if '
                                                                                                                                                                                                                                    'priority '
                                                                                                                                                                                                                                    'then '
                                                                                                                                                                                                                                    '10 '
                                                                                                                                                                                                                                    'else '
                                                                                                                                                                                                                                    '0)',
                                                                                                                                                                                                                         'relevant': True,
                                                                                                                                                                                                                         'status': 'UNIVERSAL',
                                                                                                                                                                                                                         'typ': 'Bool',
                                                                                                                                                                                                                         'value': True}},
 'priority': {'priority()': {'environmental': False,
                             'is_assignment': False,
                             'normal': True,
                             'reading': 'priority',
                             'relevant': True,
                             'status': 'UNKNOWN',
                             'typ': 'Bool'}}}
