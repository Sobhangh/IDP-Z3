
-- original ---------------------------------


vocabulary {
	Bonus: ()→Int
	Years_of_Work: ()→Int
}
theory {
	//Salary Bonus
	Bonus() = sum(lambda : if Years_of_Work() > 1 then 100 else 0)+sum(lambda : if Years_of_Work() > 2 then 200 else 0)+sum(lambda : if Years_of_Work() > 3 then 300 else 0 )+sum(lambda : if Years_of_Work() > 5 then 500 else 0 ).
}


structure {
}

-- meta -------------------------------------
{'manualPropagation': False,
 'manualRelevance': False,
 'optionalPropagation': False,
 'optionalRelevance': False,
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
{' Global': {'active': '{}', 'env_dec': False},
 'Bonus': {'Bonus()': {'environmental': False,
                       'is_assignment': True,
                       'normal': True,
                       'reading': 'Bonus',
                       'relevant': True,
                       'status': 'UNKNOWN',
                       'typ': 'Int',
                       'value': ''},
           'Bonus() = sum(lambda  :  if   Years_of_Work() > 1 then 100 else 0) + sum(lambda  :  if   Years_of_Work() > 2 then 200 else 0) + sum(lambda  :  if   Years_of_Work() > 3 then 300 else 0) + sum(lambda  :  if   Years_of_Work() > 5 then 500 else 0)': {'environmental': False,
                                                                                                                                                                                                                                                                   'is_assignment': False,
                                                                                                                                                                                                                                                                   'normal': False,
                                                                                                                                                                                                                                                                   'reading': 'Bonus '
                                                                                                                                                                                                                                                                              '= '
                                                                                                                                                                                                                                                                              'sum(lambda  '
                                                                                                                                                                                                                                                                              ':  '
                                                                                                                                                                                                                                                                              'if   '
                                                                                                                                                                                                                                                                              'Years_of_Work '
                                                                                                                                                                                                                                                                              '> '
                                                                                                                                                                                                                                                                              '1 '
                                                                                                                                                                                                                                                                              'then '
                                                                                                                                                                                                                                                                              '100 '
                                                                                                                                                                                                                                                                              'else '
                                                                                                                                                                                                                                                                              '0) '
                                                                                                                                                                                                                                                                              '+ '
                                                                                                                                                                                                                                                                              'sum(lambda  '
                                                                                                                                                                                                                                                                              ':  '
                                                                                                                                                                                                                                                                              'if   '
                                                                                                                                                                                                                                                                              'Years_of_Work '
                                                                                                                                                                                                                                                                              '> '
                                                                                                                                                                                                                                                                              '2 '
                                                                                                                                                                                                                                                                              'then '
                                                                                                                                                                                                                                                                              '200 '
                                                                                                                                                                                                                                                                              'else '
                                                                                                                                                                                                                                                                              '0) '
                                                                                                                                                                                                                                                                              '+ '
                                                                                                                                                                                                                                                                              'sum(lambda  '
                                                                                                                                                                                                                                                                              ':  '
                                                                                                                                                                                                                                                                              'if   '
                                                                                                                                                                                                                                                                              'Years_of_Work '
                                                                                                                                                                                                                                                                              '> '
                                                                                                                                                                                                                                                                              '3 '
                                                                                                                                                                                                                                                                              'then '
                                                                                                                                                                                                                                                                              '300 '
                                                                                                                                                                                                                                                                              'else '
                                                                                                                                                                                                                                                                              '0) '
                                                                                                                                                                                                                                                                              '+ '
                                                                                                                                                                                                                                                                              'sum(lambda  '
                                                                                                                                                                                                                                                                              ':  '
                                                                                                                                                                                                                                                                              'if   '
                                                                                                                                                                                                                                                                              'Years_of_Work '
                                                                                                                                                                                                                                                                              '> '
                                                                                                                                                                                                                                                                              '5 '
                                                                                                                                                                                                                                                                              'then '
                                                                                                                                                                                                                                                                              '500 '
                                                                                                                                                                                                                                                                              'else '
                                                                                                                                                                                                                                                                              '0)',
                                                                                                                                                                                                                                                                   'relevant': True,
                                                                                                                                                                                                                                                                   'status': 'CONSEQUENCE',
                                                                                                                                                                                                                                                                   'typ': 'Bool',
                                                                                                                                                                                                                                                                   'value': True}},
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
                                           'typ': 'Bool'}}}
