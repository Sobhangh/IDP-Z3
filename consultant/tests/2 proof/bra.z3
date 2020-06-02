
-- original ---------------------------------
vocabulary {
    p
    q
    r
    s
    t
} 
theory {
    p.
    (~(p)|(p)).
}
display {
    view = expanded.
}
-- meta -------------------------------------
{'symbols': [{'environmental': False,
              'idpname': 'p',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'p': {'__rank': 1,
       'p': {'environmental': False,
             'normal': True,
             'reading': 'p',
             'relevant': True,
             'status': 'UNIVERSAL',
             'typ': 'Bool',
             'value': True}},
 'q': {'__rank': 9999,
       'q': {'environmental': False,
             'normal': True,
             'reading': 'q',
             'relevant': False,
             'status': 'UNKNOWN',
             'typ': 'Bool'}},
 'r': {'__rank': 9999,
       'r': {'environmental': False,
             'normal': True,
             'reading': 'r',
             'relevant': False,
             'status': 'UNKNOWN',
             'typ': 'Bool'}},
 's': {'__rank': 9999,
       's': {'environmental': False,
             'normal': True,
             'reading': 's',
             'relevant': False,
             'status': 'UNKNOWN',
             'typ': 'Bool'}},
 't': {'__rank': 9999,
       't': {'environmental': False,
             'normal': True,
             'reading': 't',
             'relevant': False,
             'status': 'UNKNOWN',
             'typ': 'Bool'}}}
