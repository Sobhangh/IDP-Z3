
-- original ---------------------------------
vocabulary {
    f:(Int)→Date
}

theory {
    f(1)>=2.
    f(0) = #TODAY.
    #2000-01-01 < f(0).
}
display { view() = expanded. }
-- meta -------------------------------------
{'optionalPropagation': False,
 'symbols': [{'environmental': False,
              'idpname': 'f',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'f': {'#2000-01-01 < f(0)': {'environmental': False,
                              'is_assignment': False,
                              'normal': False,
                              'reading': '#2000-01-01 < f(0)',
                              'relevant': True,
                              'status': 'UNIVERSAL',
                              'typ': 'Bool',
                              'value': True},
       '__rank': 1,
       'f(0)': {'environmental': False,
                'is_assignment': True,
                'normal': True,
                'reading': 'f(0)',
                'relevant': True,
                'status': 'UNIVERSAL',
                'typ': 'Date',
                'value': '#2021-03-04'},
       'f(0) = #2021-03-04': {'environmental': False,
                              'is_assignment': True,
                              'normal': False,
                              'reading': 'f(0) = #2021-03-04',
                              'relevant': True,
                              'status': 'UNIVERSAL',
                              'typ': 'Bool',
                              'value': True},
       'f(1) ≥ 2': {'environmental': False,
                    'is_assignment': False,
                    'normal': False,
                    'reading': 'f(1) ≥ 2',
                    'relevant': True,
                    'status': 'UNIVERSAL',
                    'typ': 'Bool',
                    'value': True}}}
