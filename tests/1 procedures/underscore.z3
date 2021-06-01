
-- original ---------------------------------
vocabulary V {
    p, _q, r: () -> Bool
}

theory T:V {
    p() => _q().
    _q() => r().

}


display {
    goal(`r).
  view() = expanded.
}
-- meta -------------------------------------
{'manualPropagation': False,
 'optionalPropagation': False,
 'symbols': [{'environmental': False,
              'idpname': 'p',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'expanded'},
             {'environmental': False,
              'idpname': 'r',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'active': '{}', 'env_dec': False},
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
               'status': 'UNKNOWN',
               'typ': 'Bool'}}}
