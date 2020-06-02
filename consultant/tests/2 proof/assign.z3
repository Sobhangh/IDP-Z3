
-- original ---------------------------------
vocabulary {
    x:int
    y:int
} 
theory {
    x=0.
    ~(x=0)|(x=0).
}
display {
    view = expanded.
}
-- meta -------------------------------------
{'symbols': [{'environmental': False,
              'idpname': 'x',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'x': {'__rank': 1,
       'x': {'environmental': False,
             'normal': True,
             'reading': 'x',
             'relevant': True,
             'status': 'UNIVERSAL',
             'typ': 'Int',
             'value': '0'},
       'x = 0': {'environmental': False,
                 'normal': False,
                 'reading': 'x = 0',
                 'relevant': True,
                 'status': 'UNIVERSAL',
                 'typ': 'Bool',
                 'value': True}},
 'y': {'__rank': 9999,
       'y': {'environmental': False,
             'normal': True,
             'reading': 'y',
             'relevant': False,
             'status': 'UNKNOWN',
             'typ': 'Int',
             'value': ''}}}
