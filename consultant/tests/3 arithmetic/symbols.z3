
-- original ---------------------------------
vocabulary {
    p q
    important(`Symbols)
}
theory {
  { p.}
  ~p()|q.
  { important(`p). }
  ?`x[`Symbols]: important(`x).
  ~(!`x[`Symbols]: important(`x)).

  // TODO 
  // !`x[`Symbols]: important(`x) => `x().
}
display {
  relevant(`p).
  expanded(`q).
  goal(`p).
  view = normal.
}
-- meta -------------------------------------
{'symbols': [{'environmental': False,
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
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'important': {'__rank': 9999,
               'important(`important)': {'environmental': False,
                                         'normal': True,
                                         'reading': 'important(`important)',
                                         'relevant': False,
                                         'status': 'UNIVERSAL',
                                         'typ': 'Bool',
                                         'value': False},
               'important(`p)': {'environmental': False,
                                 'normal': True,
                                 'reading': 'important(`p)',
                                 'relevant': False,
                                 'status': 'UNIVERSAL',
                                 'typ': 'Bool',
                                 'value': True},
               'important(`q)': {'environmental': False,
                                 'normal': True,
                                 'reading': 'important(`q)',
                                 'relevant': False,
                                 'status': 'UNIVERSAL',
                                 'typ': 'Bool',
                                 'value': False},
               '∀`x[`Symbols] : important(`x)': {'environmental': False,
                                                 'normal': False,
                                                 'reading': '∀`x[`Symbols] : important(`x)',
                                                 'relevant': False,
                                                 'status': 'UNIVERSAL',
                                                 'typ': 'Bool',
                                                 'value': False},
               '∃`x[`Symbols] : important(`x)': {'environmental': False,
                                                 'normal': False,
                                                 'reading': '∃`x[`Symbols] : important(`x)',
                                                 'relevant': False,
                                                 'status': 'UNIVERSAL',
                                                 'typ': 'Bool',
                                                 'value': True}},
 'p': {'__rank': 1,
       'p': {'environmental': False,
             'normal': True,
             'reading': 'p',
             'relevant': True,
             'status': 'UNIVERSAL',
             'typ': 'Bool',
             'value': True}},
 'q': {'__rank': 2,
       'q': {'environmental': False,
             'normal': True,
             'reading': 'q',
             'relevant': True,
             'status': 'CONSEQUENCE',
             'typ': 'Bool',
             'value': True}}}
