
-- original ---------------------------------

theory {
  ~p|q.
}
vocabulary {
    p q
}
structure {
  p = true.
}
display {
  expand(`q).
  view = normal.
}

-- meta -------------------------------------
{'optionalPropagation': False,
 'symbols': [{'environmental': False,
              'idpname': 'q',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'q': {'__rank': 1,
       'q': {'environmental': False,
             'is_assignment': False,
             'normal': True,
             'reading': 'q',
             'relevant': True,
             'status': 'UNIVERSAL',
             'typ': 'Bool',
             'value': True}}}
