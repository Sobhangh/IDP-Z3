
-- original ---------------------------------
vocabulary {
    p, q, r, s, b: () → Bool
}

theory {
    { p() <- q() | r(). }
    p()|s().
    q().
}
display {
    goal(`b).
    view() = expanded.
}
-- meta -------------------------------------
{'optionalPropagation': False,
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
              'idpname': 'b',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'b': {'__rank': 1,
       'b()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'b',
               'relevant': True,
               'status': 'UNKNOWN',
               'typ': 'Bool'}},
 'p': {'__rank': 9999,
       'p()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'p',
               'relevant': False,
               'status': 'CONSEQUENCE',
               'typ': 'Bool',
               'value': True}},
 'q': {'__rank': 9999,
       'q()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'q',
               'relevant': False,
               'status': 'UNIVERSAL',
               'typ': 'Bool',
               'value': True}},
 'r': {'__rank': 9999,
       'r()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'r',
               'relevant': False,
               'status': 'UNKNOWN',
               'typ': 'Bool'}},
 's': {'__rank': 9999,
       's()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 's',
               'relevant': False,
               'status': 'UNKNOWN',
               'typ': 'Bool'}}}
