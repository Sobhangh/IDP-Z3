
-- original ---------------------------------


vocabulary {
	Bonus: ()→Int
	Years_of_Work: ()→Int
}
theory {
	//Salary Bonus
	Bonus() = sum{ : Years_of_Work() > 1: 100 }+sum{ : Years_of_Work() > 2: 200 }+sum{ : Years_of_Work() > 3: 300 }+sum{ : Years_of_Work() > 5: 500 }.
}


structure {
}

-- meta -------------------------------------
{'optionalPropagation': False,
 'symbols': [{'environmental': False,
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
 'Bonus': {'Bonus()': {'environmental': False,
                       'is_assignment': True,
                       'normal': True,
                       'reading': 'Bonus',
                       'relevant': True,
                       'status': 'UNKNOWN',
                       'typ': 'Int',
                       'value': ''},
           'Bonus() = sum{ : Years_of_Work() > 1 : 100} + sum{ : Years_of_Work() > 2 : 200} + sum{ : Years_of_Work() > 3 : 300} + sum{ : Years_of_Work() > 5 : 500}': {'environmental': False,
                                                                                                                                                                       'is_assignment': False,
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
           '__rank': 9999},
 'Years_of_Work': {'Years_of_Work()': {'environmental': False,
                                       'is_assignment': True,
                                       'normal': True,
                                       'reading': 'Years_of_Work',
                                       'relevant': True,
                                       'status': 'UNKNOWN',
                                       'typ': 'Int',
                                       'value': ''},
                   'Years_of_Work() > 1': {'environmental': False,
                                           'is_assignment': False,
                                           'normal': False,
                                           'reading': 'Years_of_Work > 1',
                                           'relevant': True,
                                           'status': 'UNKNOWN',
                                           'typ': 'Bool'},
                   'Years_of_Work() > 2': {'environmental': False,
                                           'is_assignment': False,
                                           'normal': False,
                                           'reading': 'Years_of_Work > 2',
                                           'relevant': True,
                                           'status': 'UNKNOWN',
                                           'typ': 'Bool'},
                   'Years_of_Work() > 3': {'environmental': False,
                                           'is_assignment': False,
                                           'normal': False,
                                           'reading': 'Years_of_Work > 3',
                                           'relevant': True,
                                           'status': 'UNKNOWN',
                                           'typ': 'Bool'},
                   'Years_of_Work() > 5': {'environmental': False,
                                           'is_assignment': False,
                                           'normal': False,
                                           'reading': 'Years_of_Work > 5',
                                           'relevant': True,
                                           'status': 'UNKNOWN',
                                           'typ': 'Bool'},
                   '__rank': 9999}}
