
-- original ---------------------------------
vocabulary V {
    p, _q, δ: () -> Bool
}

theory T:V {
    p() => _q().
    _q() => δ().

}


display {
    goal(`δ).
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
              'idpname': 'δ',
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
 'δ': {'__rank': 9999,
       'δ()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'δ',
               'relevant': True,
               'status': 'UNKNOWN',
               'typ': 'Bool'}}}
