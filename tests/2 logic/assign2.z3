
-- original ---------------------------------
vocabulary {
    x, y:()→Int
}
theory {
    x()=0.
    ~(x()+1=1)|(x()+1=1).
}
display {
    view() = expanded.
}
-- meta -------------------------------------
{'manualPropagation': False,
 'optionalPropagation': False,
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
 'x': {'__rank': 9999,
       'x()': {'environmental': False,
               'is_assignment': True,
               'normal': True,
               'reading': 'x',
               'relevant': True,
               'status': 'UNIVERSAL',
               'typ': 'Int',
               'value': '0'},
       'x() + 1 = 1': {'environmental': False,
                       'is_assignment': False,
                       'normal': False,
                       'reading': 'x + 1 = 1',
                       'relevant': True,
                       'status': 'CONSEQUENCE',
                       'typ': 'Bool',
                       'value': True},
       'x() = 0': {'environmental': False,
                   'is_assignment': True,
                   'normal': False,
                   'reading': 'x = 0',
                   'relevant': True,
                   'status': 'UNIVERSAL',
                   'typ': 'Bool',
                   'value': True}},
 'y': {'__rank': 9999,
       'y()': {'environmental': False,
               'is_assignment': True,
               'normal': True,
               'reading': 'y',
               'relevant': False,
               'status': 'UNKNOWN',
               'typ': 'Int',
               'value': ''}}}
