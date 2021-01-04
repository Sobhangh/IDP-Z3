
-- original ---------------------------------
vocabulary {
    double(Real): Real
    X: Real
    y: Real
}
theory {
    {!x[Real]: double(x)= x+x. }
    X()=3.
    y=double(X()).
}
-- meta -------------------------------------
{'optionalPropagation': False,
 'symbols': [{'environmental': False,
              'idpname': 'X',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'y',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'double',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'X': {'X': {'environmental': False,
             'is_assignment': True,
             'normal': True,
             'reading': 'X',
             'relevant': True,
             'status': 'UNIVERSAL',
             'typ': 'Real',
             'value': '3'},
       'X = 3': {'environmental': False,
                 'is_assignment': True,
                 'normal': False,
                 'reading': 'X = 3',
                 'relevant': True,
                 'status': 'UNIVERSAL',
                 'typ': 'Bool',
                 'value': True},
       '__rank': 1},
 'double': {'__rank': 1,
            'double(X) = X + X': {'environmental': False,
                                  'is_assignment': False,
                                  'normal': False,
                                  'reading': 'double(X) = X + X',
                                  'relevant': True,
                                  'status': 'UNIVERSAL',
                                  'typ': 'Bool',
                                  'value': True}},
 'y': {'__rank': 1,
       'y': {'environmental': False,
             'is_assignment': True,
             'normal': True,
             'reading': 'y',
             'relevant': True,
             'status': 'CONSEQUENCE',
             'typ': 'Real',
             'value': '6'},
       'y = double(X)': {'environmental': False,
                         'is_assignment': False,
                         'normal': False,
                         'reading': 'y = double(X)',
                         'relevant': True,
                         'status': 'UNIVERSAL',
                         'typ': 'Bool',
                         'value': True}}}
