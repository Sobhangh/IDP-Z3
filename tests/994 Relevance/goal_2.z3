
-- original ---------------------------------
vocabulary V {
    p, q, r, s: () -> Bool
}

theory T:V {
    { p() <- q(). }
    { r() <- s(). }
}

structure default:V {
}

display {
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
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'q',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'r',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 's',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'p': {'p()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'p',
               'relevant': True,
               'status': 'UNKNOWN',
               'typ': 'Bool'}},
 'q': {'q()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'q',
               'relevant': True,
               'status': 'UNKNOWN',
               'typ': 'Bool'}},
 'r': {'r()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'r',
               'relevant': True,
               'status': 'UNKNOWN',
               'typ': 'Bool'}},
 's': {'s()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 's',
               'relevant': True,
               'status': 'UNKNOWN',
               'typ': 'Bool'}}}
