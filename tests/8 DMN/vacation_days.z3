
-- original ---------------------------------


vocabulary {
	Years_of_Service: ()→Int
	Age: ()→Int
	vacationdays: ()→Int
	extra5:() → Bool
	extra3:() → Bool
	extra2:() → Bool
}
theory {
	//Extra 5 Days
	{
		extra5() <- Age() < 18.
		extra5() <- Age() >= 60.
		extra5() <- Years_of_Service() >= 30.
	}

	//Extra 3 Days
	{
		extra3() <- Age() >= 60.
		extra3() <- Years_of_Service() >= 30.
	}

	//Extra 2 Days
	{
		extra2() <- Age() >= 45.
		extra2() <- 15 =< Years_of_Service() & Years_of_Service() =< 30.
	}

	//Total Days
	vacationdays() = sum(lambda : 20 )+sum(lambda : if extra2() then 2 else 0)+sum(lambda : if extra3() then 3 else 0)+sum(lambda : if extra5() then 5 else 0).
}


structure {
}

-- meta -------------------------------------
{'manualPropagation': False,
 'manualRelevance': False,
 'optionalPropagation': False,
 'optionalRelevance': False,
 'symbols': [{'environmental': False,
              'idpname': 'Years_of_Service',
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
              'idpname': 'vacationdays',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'extra5',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'extra3',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'extra2',
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
         'Age() < 18': {'environmental': False,
                        'is_assignment': False,
                        'normal': False,
                        'reading': 'Age < 18',
                        'relevant': True,
                        'status': 'UNKNOWN',
                        'typ': 'Bool'},
         'Age() ≥ 45': {'environmental': False,
                        'is_assignment': False,
                        'normal': False,
                        'reading': 'Age ≥ 45',
                        'relevant': True,
                        'status': 'UNKNOWN',
                        'typ': 'Bool'},
         'Age() ≥ 60': {'environmental': False,
                        'is_assignment': False,
                        'normal': False,
                        'reading': 'Age ≥ 60',
                        'relevant': True,
                        'status': 'UNKNOWN',
                        'typ': 'Bool'}},
 'Years_of_Service': {'15 ≤ Years_of_Service()': {'environmental': False,
                                                  'is_assignment': False,
                                                  'normal': False,
                                                  'reading': '15 ≤ Years_of_Service',
                                                  'relevant': True,
                                                  'status': 'UNKNOWN',
                                                  'typ': 'Bool'},
                      'Years_of_Service()': {'environmental': False,
                                             'is_assignment': True,
                                             'normal': True,
                                             'reading': 'Years_of_Service',
                                             'relevant': True,
                                             'status': 'UNKNOWN',
                                             'typ': 'Int',
                                             'value': ''},
                      'Years_of_Service() ≤ 30': {'environmental': False,
                                                  'is_assignment': False,
                                                  'normal': False,
                                                  'reading': 'Years_of_Service ≤ 30',
                                                  'relevant': True,
                                                  'status': 'UNKNOWN',
                                                  'typ': 'Bool'},
                      'Years_of_Service() ≥ 30': {'environmental': False,
                                                  'is_assignment': False,
                                                  'normal': False,
                                                  'reading': 'Years_of_Service ≥ 30',
                                                  'relevant': True,
                                                  'status': 'UNKNOWN',
                                                  'typ': 'Bool'}},
 'extra2': {'extra2()': {'environmental': False,
                         'is_assignment': False,
                         'normal': True,
                         'reading': 'extra2',
                         'relevant': True,
                         'status': 'UNKNOWN',
                         'typ': 'Bool'}},
 'extra3': {'extra3()': {'environmental': False,
                         'is_assignment': False,
                         'normal': True,
                         'reading': 'extra3',
                         'relevant': True,
                         'status': 'UNKNOWN',
                         'typ': 'Bool'}},
 'extra5': {'extra5()': {'environmental': False,
                         'is_assignment': False,
                         'normal': True,
                         'reading': 'extra5',
                         'relevant': True,
                         'status': 'UNKNOWN',
                         'typ': 'Bool'}},
 'vacationdays': {'vacationdays()': {'environmental': False,
                                     'is_assignment': True,
                                     'normal': True,
                                     'reading': 'vacationdays',
                                     'relevant': True,
                                     'status': 'UNKNOWN',
                                     'typ': 'Int',
                                     'value': ''},
                  'vacationdays() = sum(lambda  : 20) + sum(lambda  :  if   extra2() then 2 else 0) + sum(lambda  :  if   extra3() then 3 else 0) + sum(lambda  :  if   extra5() then 5 else 0)': {'environmental': False,
                                                                                                                                                                                                   'is_assignment': False,
                                                                                                                                                                                                   'normal': False,
                                                                                                                                                                                                   'reading': 'vacationdays '
                                                                                                                                                                                                              '= '
                                                                                                                                                                                                              'sum(lambda  '
                                                                                                                                                                                                              ': '
                                                                                                                                                                                                              '20) '
                                                                                                                                                                                                              '+ '
                                                                                                                                                                                                              'sum(lambda  '
                                                                                                                                                                                                              ':  '
                                                                                                                                                                                                              'if   '
                                                                                                                                                                                                              'extra2 '
                                                                                                                                                                                                              'then '
                                                                                                                                                                                                              '2 '
                                                                                                                                                                                                              'else '
                                                                                                                                                                                                              '0) '
                                                                                                                                                                                                              '+ '
                                                                                                                                                                                                              'sum(lambda  '
                                                                                                                                                                                                              ':  '
                                                                                                                                                                                                              'if   '
                                                                                                                                                                                                              'extra3 '
                                                                                                                                                                                                              'then '
                                                                                                                                                                                                              '3 '
                                                                                                                                                                                                              'else '
                                                                                                                                                                                                              '0) '
                                                                                                                                                                                                              '+ '
                                                                                                                                                                                                              'sum(lambda  '
                                                                                                                                                                                                              ':  '
                                                                                                                                                                                                              'if   '
                                                                                                                                                                                                              'extra5 '
                                                                                                                                                                                                              'then '
                                                                                                                                                                                                              '5 '
                                                                                                                                                                                                              'else '
                                                                                                                                                                                                              '0)',
                                                                                                                                                                                                   'relevant': True,
                                                                                                                                                                                                   'status': 'UNIVERSAL',
                                                                                                                                                                                                   'typ': 'Bool',
                                                                                                                                                                                                   'value': True}}}
