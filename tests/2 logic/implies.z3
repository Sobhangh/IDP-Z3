
-- original ---------------------------------
vocabulary {
    p, q, r,s,t:() → Bool
}
theory {
    p().
    p()=>q().
    q()=>(~r()).
}
display {
    view() = expanded.
}
-- meta -------------------------------------
{'manualPropagation': False,
 'manualRelevance': False,
 'optionalPropagation': False,
 'optionalRelevance': False,
 'symbols': [{'environmental': False,
              'idpname': 'p',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'expanded'},
             {'environmental': False,
              'idpname': 'q',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'expanded'},
             {'environmental': False,
              'idpname': 'r',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'expanded'},
             {'environmental': False,
              'idpname': 's',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'expanded'},
             {'environmental': False,
              'idpname': 't',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'active': '{}', 'env_dec': False},
 'p': {'p()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'p',
               'relevant': True,
               'status': 'CONSEQUENCE',
               'typ': 'Bool',
               'value': True}},
 'q': {'q()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'q',
               'relevant': True,
               'status': 'CONSEQUENCE',
               'typ': 'Bool',
               'value': True}},
 'r': {'r()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'r',
               'relevant': True,
               'status': 'CONSEQUENCE',
               'typ': 'Bool',
               'value': False}},
 's': {'s()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 's',
               'relevant': False,
               'status': 'UNKNOWN',
               'typ': 'Bool'}},
 't': {'t()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 't',
               'relevant': False,
               'status': 'UNKNOWN',
               'typ': 'Bool'}}}
