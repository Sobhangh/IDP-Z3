
-- original ---------------------------------
vocabulary V {
    p, q : () → 𝔹
    c: () -> Int
}

theory T:V {
    c()>3 => p() or q().
    c()<2.
}

structure S:V {

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
              'idpname': 'c',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'c': {'c()': {'environmental': False,
               'is_assignment': True,
               'normal': True,
               'reading': 'c',
               'relevant': True,
               'status': 'UNKNOWN',
               'typ': 'Int'},
       'c() < 2': {'environmental': False,
                   'is_assignment': False,
                   'normal': False,
                   'reading': 'c < 2',
                   'relevant': False,
                   'status': 'UNIVERSAL',
                   'typ': 'Bool',
                   'value': True},
       'c() > 3': {'environmental': False,
                   'is_assignment': False,
                   'normal': False,
                   'reading': 'c > 3',
                   'relevant': False,
                   'status': 'UNIVERSAL',
                   'typ': 'Bool',
                   'value': False}},
 'p': {'p()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'p',
               'relevant': False,
               'status': 'UNKNOWN',
               'typ': 'Bool'}},
 'q': {'q()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'q',
               'relevant': False,
               'status': 'UNKNOWN',
               'typ': 'Bool'}}}
