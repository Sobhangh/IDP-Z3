
-- original ---------------------------------
vocabulary {
    double(real): real
    x: real
    y: real
}
theory {
    {!x[real]: double(x)= x+x. }
    x=3.
    y=double(x).
}
-- meta -------------------------------------
{'optionalPropagation': False,
 'symbols': [{'environmental': False,
              'idpname': 'double',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'x',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'y',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'double': {},
 'x': {'__rank': 1,
       'x': {'environmental': False,
             'is_assignment': True,
             'normal': True,
             'reading': 'x',
             'relevant': True,
             'status': 'UNIVERSAL',
             'typ': 'Real',
             'value': '3'},
       'x = 3': {'environmental': False,
                 'is_assignment': True,
                 'normal': False,
                 'reading': 'x = 3',
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
       'y = double(x)': {'environmental': False,
                         'is_assignment': False,
                         'normal': False,
                         'reading': 'y = double(x)',
                         'relevant': True,
                         'status': 'UNIVERSAL',
                         'typ': 'Bool',
                         'value': True}}}
