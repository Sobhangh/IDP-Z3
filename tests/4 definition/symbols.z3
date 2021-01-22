
-- original ---------------------------------
vocabulary {
    p, q: ()
    important: (`Symbols)
}
theory {
  ~p()|q.
  { important(`p). }

  { !`x[`Symbols]: important(`x) <- `x(). }
}
display {
  relevant(`p).
  expand(`q).
  hide(`important).
  goal(`p).
  view = normal.
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
              'idpname': 'important',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'hidden'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'important': {'__rank': 9999,
               'important(`important)': {'environmental': False,
                                         'is_assignment': False,
                                         'normal': True,
                                         'reading': 'important(`important)',
                                         'relevant': False,
                                         'status': 'UNKNOWN',
                                         'typ': 'Bool'},
               'important(`p)': {'environmental': False,
                                 'is_assignment': False,
                                 'normal': True,
                                 'reading': 'important(`p)',
                                 'relevant': False,
                                 'status': 'UNKNOWN',
                                 'typ': 'Bool'},
               'important(`q)': {'environmental': False,
                                 'is_assignment': False,
                                 'normal': True,
                                 'reading': 'important(`q)',
                                 'relevant': False,
                                 'status': 'UNKNOWN',
                                 'typ': 'Bool'}},
 'p': {'__rank': 1,
       'p': {'environmental': False,
             'is_assignment': False,
             'normal': True,
             'reading': 'p',
             'relevant': True,
             'status': 'UNKNOWN',
             'typ': 'Bool'}},
 'q': {'__rank': 2,
       'q': {'environmental': False,
             'is_assignment': False,
             'normal': True,
             'reading': 'q',
             'relevant': True,
             'status': 'UNKNOWN',
             'typ': 'Bool'}}}
