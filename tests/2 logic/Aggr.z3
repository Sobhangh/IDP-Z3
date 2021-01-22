
-- original ---------------------------------
vocabulary {
    type color constructed from {red, blue, green}
    p: ()
}
theory {
    p <=> sum{c[color] : true : 1} = 3.
}
display {
    view = expanded.
    moveSymbols.
}
-- meta -------------------------------------
{'optionalPropagation': False,
 'symbols': [{'environmental': False,
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
             'is_assignment': False,
             'normal': True,
             'reading': 'p',
             'relevant': True,
             'status': 'UNIVERSAL',
             'typ': 'Bool',
             'value': True}}}
