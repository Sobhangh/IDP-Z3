
-- original ---------------------------------
vocabulary {
    Wages_Salaries_Tips: int
    Unemployment_Comp: int
    Taxable_Interest: int
    Adjusted_Gross_Income: int
    Eligible
}
theory {
    //Calculate Gross Income
    {
        Adjusted_Gross_Income() = 0 <- ~(Eligible()).
        Adjusted_Gross_Income() = Wages_Salaries_Tips + Taxable_Interest + Unemployment_Comp <- Eligible().
    }

}


structure {
}


-- meta -------------------------------------
{'symbols': [{'environmental': False,
              'idpname': 'Wages_Salaries_Tips',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Unemployment_Comp',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Taxable_Interest',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Adjusted_Gross_Income',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Eligible',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'Adjusted_Gross_Income': {'Adjusted_Gross_Income': {'environmental': False,
                                                     'is_assignment': True,
                                                     'normal': True,
                                                     'reading': 'Adjusted_Gross_Income',
                                                     'relevant': False,
                                                     'status': 'UNKNOWN',
                                                     'typ': 'Int',
                                                     'value': ''},
                           '__rank': 9999},
 'Eligible': {'Eligible': {'environmental': False,
                           'is_assignment': False,
                           'normal': True,
                           'reading': 'Eligible',
                           'relevant': False,
                           'status': 'UNKNOWN',
                           'typ': 'Bool'},
              '__rank': 9999},
 'Taxable_Interest': {'Taxable_Interest': {'environmental': False,
                                           'is_assignment': True,
                                           'normal': True,
                                           'reading': 'Taxable_Interest',
                                           'relevant': False,
                                           'status': 'UNKNOWN',
                                           'typ': 'Int',
                                           'value': ''},
                      '__rank': 9999},
 'Unemployment_Comp': {'Unemployment_Comp': {'environmental': False,
                                             'is_assignment': True,
                                             'normal': True,
                                             'reading': 'Unemployment_Comp',
                                             'relevant': False,
                                             'status': 'UNKNOWN',
                                             'typ': 'Int',
                                             'value': ''},
                       '__rank': 9999},
 'Wages_Salaries_Tips': {'Wages_Salaries_Tips': {'environmental': False,
                                                 'is_assignment': True,
                                                 'normal': True,
                                                 'reading': 'Wages_Salaries_Tips',
                                                 'relevant': False,
                                                 'status': 'UNKNOWN',
                                                 'typ': 'Int',
                                                 'value': ''},
                         '__rank': 9999}}
