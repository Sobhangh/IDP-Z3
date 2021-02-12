
-- original ---------------------------------
vocabulary {
    x, y:()→Int
}
theory {
    x()=0.
    ~(x()=0)|(x()=0).
}
display {
    view() = expanded.
}
-- meta -------------------------------------
{'optionalPropagation': False,
 'symbols': [{'environmental': False,
              'idpname': 'x',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'expanded'},
             {'environmental': False,
              'idpname': 'y',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'x': {'__rank': 1,
       'x': {'environmental': False,
             'is_assignment': True,
             'normal': True,
             'reading': 'x',
             'relevant': True,
             'status': 'UNIVERSAL',
             'typ': 'Int',
             'value': '0'},
       'x = 0': {'environmental': False,
                 'is_assignment': True,
                 'normal': False,
                 'reading': 'x = 0',
                 'relevant': True,
                 'status': 'UNIVERSAL',
                 'typ': 'Bool',
                 'value': True}},
 'y': {'__rank': 9999,
       'y': {'environmental': False,
             'is_assignment': True,
             'normal': True,
             'reading': 'y',
             'relevant': False,
             'status': 'UNKNOWN',
             'typ': 'Int',
             'value': ''}}}
