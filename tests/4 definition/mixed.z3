
-- original ---------------------------------
vocabulary {
p, q, r, s: () → Bool
x:()→Int
}

theory {
    {p() <- ~q().}
    p() => s().
   x()=1.

}

-- meta -------------------------------------
{'optionalPropagation': False,
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
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'x',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'p': {'__rank': 9999,
       'p()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'p',
               'relevant': True,
               'status': 'UNKNOWN',
               'typ': 'Bool'}},
 'q': {'__rank': 9999,
       'q()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'q',
               'relevant': True,
               'status': 'UNKNOWN',
               'typ': 'Bool'}},
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
               'relevant': True,
               'status': 'UNKNOWN',
               'typ': 'Bool'}},
 'x': {'__rank': 9999,
       'x()': {'environmental': False,
               'is_assignment': True,
               'normal': True,
               'reading': 'x',
               'relevant': True,
               'status': 'UNIVERSAL',
               'typ': 'Int',
               'value': '1'},
       'x() = 1': {'environmental': False,
                   'is_assignment': True,
                   'normal': False,
                   'reading': 'x = 1',
                   'relevant': True,
                   'status': 'UNIVERSAL',
                   'typ': 'Bool',
                   'value': True}}}
