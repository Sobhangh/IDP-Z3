
-- original ---------------------------------
vocabulary {
    p, l, r, rd, i: () → Bool
}
theory {
  { i() <- rd().}
  { p() <- l() | r().}
  { r() <- rd().}
  r().
}
display {
  goal(`p).
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
              'idpname': 'l',
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
              'idpname': 'rd',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'i',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'active': '{}', 'env_dec': False},
 'i': {'__rank': 9999,
       'i()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'i',
               'relevant': False,
               'status': 'UNKNOWN',
               'typ': 'Bool'}},
 'l': {'__rank': 9999,
       'l()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'l',
               'relevant': False,
               'status': 'UNKNOWN',
               'typ': 'Bool'}},
 'p': {'__rank': 9999,
       'p()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'p',
               'relevant': True,
               'status': 'UNKNOWN',
               'typ': 'Bool'}},
 'r': {'__rank': 9999,
       'r()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'r',
               'relevant': True,
               'status': 'UNIVERSAL',
               'typ': 'Bool',
               'value': True}},
 'rd': {'__rank': 9999,
        'rd()': {'environmental': False,
                 'is_assignment': False,
                 'normal': True,
                 'reading': 'rd',
                 'relevant': True,
                 'status': 'UNKNOWN',
                 'typ': 'Bool'}}}
