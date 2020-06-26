
-- original ---------------------------------


vocabulary {
	Bonus: int
	Years_of_Work: int
}
theory {
	//Salary Bonus
	Bonus() = sum{ : Years_of_Work() > 1: 100 }+sum{ : Years_of_Work() > 2: 200 }+sum{ : Years_of_Work() > 3: 300 }+sum{ : Years_of_Work() > 5: 500 }.
}


structure {
}

-- meta -------------------------------------
{'symbols': [{'environmental': False,
              'idpname': 'Bonus',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Years_of_Work',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'Bonus': {'Bonus': {'environmental': False,
                     'normal': True,
                     'reading': 'Bonus',
                     'relevant': True,
                     'status': 'UNKNOWN',
                     'typ': 'Int',
                     'value': ''},
           'Bonus = sum{ : Years_of_Work > 1 : 100} + sum{ : Years_of_Work > 2 : 200} + sum{ : Years_of_Work > 3 : 300} + sum{ : Years_of_Work > 5 : 500}': {'environmental': False,
                                                                                                                                                             'normal': False,
                                                                                                                                                             'reading': 'Bonus '
                                                                                                                                                                        '= '
                                                                                                                                                                        'sum{ '
                                                                                                                                                                        ': '
                                                                                                                                                                        'Years_of_Work '
                                                                                                                                                                        '> '
                                                                                                                                                                        '1 '
                                                                                                                                                                        ': '
                                                                                                                                                                        '100} '
                                                                                                                                                                        '+ '
                                                                                                                                                                        'sum{ '
                                                                                                                                                                        ': '
                                                                                                                                                                        'Years_of_Work '
                                                                                                                                                                        '> '
                                                                                                                                                                        '2 '
                                                                                                                                                                        ': '
                                                                                                                                                                        '200} '
                                                                                                                                                                        '+ '
                                                                                                                                                                        'sum{ '
                                                                                                                                                                        ': '
                                                                                                                                                                        'Years_of_Work '
                                                                                                                                                                        '> '
                                                                                                                                                                        '3 '
                                                                                                                                                                        ': '
                                                                                                                                                                        '300} '
                                                                                                                                                                        '+ '
                                                                                                                                                                        'sum{ '
                                                                                                                                                                        ': '
                                                                                                                                                                        'Years_of_Work '
                                                                                                                                                                        '> '
                                                                                                                                                                        '5 '
                                                                                                                                                                        ': '
                                                                                                                                                                        '500}',
                                                                                                                                                             'relevant': True,
                                                                                                                                                             'status': 'UNIVERSAL',
                                                                                                                                                             'typ': 'Bool',
                                                                                                                                                             'value': True},
           '__rank': 1},
 'Years_of_Work': {'Years_of_Work': {'environmental': False,
                                     'normal': True,
                                     'reading': 'Years_of_Work',
                                     'relevant': True,
                                     'status': 'UNKNOWN',
                                     'typ': 'Int',
                                     'value': ''},
                   'Years_of_Work > 1': {'environmental': False,
                                         'normal': False,
                                         'reading': 'Years_of_Work > 1',
                                         'relevant': True,
                                         'status': 'UNKNOWN',
                                         'typ': 'Bool'},
                   'Years_of_Work > 2': {'environmental': False,
                                         'normal': False,
                                         'reading': 'Years_of_Work > 2',
                                         'relevant': True,
                                         'status': 'UNKNOWN',
                                         'typ': 'Bool'},
                   'Years_of_Work > 3': {'environmental': False,
                                         'normal': False,
                                         'reading': 'Years_of_Work > 3',
                                         'relevant': True,
                                         'status': 'UNKNOWN',
                                         'typ': 'Bool'},
                   'Years_of_Work > 5': {'environmental': False,
                                         'normal': False,
                                         'reading': 'Years_of_Work > 5',
                                         'relevant': True,
                                         'status': 'UNKNOWN',
                                         'typ': 'Bool'},
                   '__rank': 1}}
