
-- original ---------------------------------
vocabulary  {
    type date = {2015; 2016}
    Start_Dt_Dwelling_For_Social_Rent : date
}
theory {
}

-- meta -------------------------------------
{'optionalPropagation': False,
 'symbols': [{'environmental': False,
              'idpname': 'Start_Dt_Dwelling_For_Social_Rent',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'Start_Dt_Dwelling_For_Social_Rent': {'Start_Dt_Dwelling_For_Social_Rent': {'environmental': False,
                                                                             'is_assignment': True,
                                                                             'normal': True,
                                                                             'reading': 'Start_Dt_Dwelling_For_Social_Rent',
                                                                             'relevant': False,
                                                                             'status': 'UNKNOWN',
                                                                             'typ': 'Int',
                                                                             'value': '',
                                                                             'values': ['2015', '2016']},
                                       'Start_Dt_Dwelling_For_Social_Rent = 2015': {'environmental': False,
                                                                                    'is_assignment': True,
                                                                                    'normal': False,
                                                                                    'reading': 'Start_Dt_Dwelling_For_Social_Rent '
                                                                                               '= 2015',
                                                                                    'relevant': False,
                                                                                    'status': 'UNKNOWN',
                                                                                    'typ': 'Bool'},
                                       'Start_Dt_Dwelling_For_Social_Rent = 2016': {'environmental': False,
                                                                                    'is_assignment': True,
                                                                                    'normal': False,
                                                                                    'reading': 'Start_Dt_Dwelling_For_Social_Rent '
                                                                                               '= 2016',
                                                                                    'relevant': False,
                                                                                    'status': 'UNKNOWN',
                                                                                    'typ': 'Bool'},
                                       '__rank': 9999}}
