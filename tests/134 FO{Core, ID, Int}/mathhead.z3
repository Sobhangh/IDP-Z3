
-- original ---------------------------------
vocabulary {
    Wages_Salaries_Tips: () → Int
    Unemployment_Comp: ()→Int
    Taxable_Interest: ()→Int
    Adjusted_Gross_Income: ()→Int
    Eligible: () → Bool
}
theory {
    //Calculate Gross Income
    {
        Adjusted_Gross_Income() = 0 <- ~(Eligible()).
        Adjusted_Gross_Income() = Wages_Salaries_Tips() + Taxable_Interest() + Unemployment_Comp() <- Eligible().
    }

}


structure {
}


-- meta -------------------------------------
{'manualPropagation': False,
 'manualRelevance': False,
 'optionalPropagation': False,
 'optionalRelevance': False,
 'symbols': [{'environmental': False,
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
              'idpname': 'Eligible',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Adjusted_Gross_Income',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'Adjusted_Gross_Income': {'Adjusted_Gross_Income()': {'environmental': False,
                                                       'is_assignment': True,
                                                       'normal': True,
                                                       'reading': 'Adjusted_Gross_Income',
                                                       'relevant': True,
                                                       'status': 'UNKNOWN',
                                                       'typ': 'Int'}},
 'Eligible': {'Eligible()': {'environmental': False,
                             'is_assignment': False,
                             'normal': True,
                             'reading': 'Eligible',
                             'relevant': True,
                             'status': 'UNKNOWN',
                             'typ': 'Bool'}},
 'Taxable_Interest': {'Taxable_Interest()': {'environmental': False,
                                             'is_assignment': True,
                                             'normal': True,
                                             'reading': 'Taxable_Interest',
                                             'relevant': True,
                                             'status': 'UNKNOWN',
                                             'typ': 'Int'}},
 'Unemployment_Comp': {'Unemployment_Comp()': {'environmental': False,
                                               'is_assignment': True,
                                               'normal': True,
                                               'reading': 'Unemployment_Comp',
                                               'relevant': True,
                                               'status': 'UNKNOWN',
                                               'typ': 'Int'}},
 'Wages_Salaries_Tips': {'Wages_Salaries_Tips()': {'environmental': False,
                                                   'is_assignment': True,
                                                   'normal': True,
                                                   'reading': 'Wages_Salaries_Tips',
                                                   'relevant': True,
                                                   'status': 'UNKNOWN',
                                                   'typ': 'Int'}}}
