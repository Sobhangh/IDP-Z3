
-- original ---------------------------------
vocabulary  {
    type date := {2015, 2016}
    Start_Dt_Dwelling_For_Social_Rent : ()→date
}
theory {
}

-- meta -------------------------------------
{'manualPropagation': False,
 'manualRelevance': False,
 'optionalPropagation': False,
 'optionalRelevance': False,
 'symbols': [{'environmental': False,
              'idpname': 'Start_Dt_Dwelling_For_Social_Rent',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'Start_Dt_Dwelling_For_Social_Rent': {'Start_Dt_Dwelling_For_Social_Rent()': {'environmental': False,
                                                                               'is_assignment': True,
                                                                               'normal': True,
                                                                               'reading': 'Start_Dt_Dwelling_For_Social_Rent',
                                                                               'relevant': False,
                                                                               'status': 'UNKNOWN',
                                                                               'typ': 'Int',
                                                                               'value': '',
                                                                               'values': ['2015', '2016']}}}
