
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
    goal_symbol := {`b}.
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
              'idpname': 'b',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'b': {'b()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'b',
               'relevant': True,
               'status': 'UNKNOWN',
               'typ': 'Bool'}},
 'p': {'p()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'p',
               'relevant': False,
               'status': 'UNIVERSAL',
               'typ': 'Bool',
               'value': True}},
 'q': {'q()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'q',
               'relevant': False,
               'status': 'UNIVERSAL',
               'typ': 'Bool',
               'value': True}},
 'r': {'r()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'r',
               'relevant': False,
               'status': 'UNKNOWN',
               'typ': 'Bool'}},
 's': {'s()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 's',
               'relevant': False,
               'status': 'UNKNOWN',
               'typ': 'Bool'}}}
