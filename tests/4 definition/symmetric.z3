
-- original ---------------------------------
vocabulary {
	type node constructed from {a,b,c}
	edge(node, node)
	symmetric(`Symbols)
}
theory {
    edge(a,b).
    !`p[`Symbols]: symmetric(`p) => (!x y : `p(x,y) => `p(y,x)).
}
structure {
	symmetric = {`edge}
}
display {
	expand(`edge).
}
-- meta -------------------------------------
{'optionalPropagation': False,
 'symbols': [{'environmental': False,
              'idpname': 'edge',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'expanded'},
             {'environmental': False,
              'idpname': 'symmetric',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'edge': {'__rank': 1,
          'edge(a,a)': {'environmental': False,
                        'is_assignment': False,
                        'normal': True,
                        'reading': 'edge(a,a)',
                        'relevant': True,
                        'status': 'UNKNOWN',
                        'typ': 'Bool'},
          'edge(a,b)': {'environmental': False,
                        'is_assignment': False,
                        'normal': True,
                        'reading': 'edge(a,b)',
                        'relevant': True,
                        'status': 'UNIVERSAL',
                        'typ': 'Bool',
                        'value': True},
          'edge(a,c)': {'environmental': False,
                        'is_assignment': False,
                        'normal': True,
                        'reading': 'edge(a,c)',
                        'relevant': True,
                        'status': 'UNKNOWN',
                        'typ': 'Bool'},
          'edge(b,a)': {'environmental': False,
                        'is_assignment': False,
                        'normal': True,
                        'reading': 'edge(b,a)',
                        'relevant': True,
                        'status': 'CONSEQUENCE',
                        'typ': 'Bool',
                        'value': True},
          'edge(b,b)': {'environmental': False,
                        'is_assignment': False,
                        'normal': True,
                        'reading': 'edge(b,b)',
                        'relevant': True,
                        'status': 'UNKNOWN',
                        'typ': 'Bool'},
          'edge(b,c)': {'environmental': False,
                        'is_assignment': False,
                        'normal': True,
                        'reading': 'edge(b,c)',
                        'relevant': True,
                        'status': 'UNKNOWN',
                        'typ': 'Bool'},
          'edge(c,a)': {'environmental': False,
                        'is_assignment': False,
                        'normal': True,
                        'reading': 'edge(c,a)',
                        'relevant': True,
                        'status': 'UNKNOWN',
                        'typ': 'Bool'},
          'edge(c,b)': {'environmental': False,
                        'is_assignment': False,
                        'normal': True,
                        'reading': 'edge(c,b)',
                        'relevant': True,
                        'status': 'UNKNOWN',
                        'typ': 'Bool'},
          'edge(c,c)': {'environmental': False,
                        'is_assignment': False,
                        'normal': True,
                        'reading': 'edge(c,c)',
                        'relevant': True,
                        'status': 'UNKNOWN',
                        'typ': 'Bool'},
          '∀`p[`Symbols] : symmetric(`p) ⇒ (∀x[None]y[None] : `p(x,y) ⇒ `p(y,x))': {'environmental': False,
                                                                                    'is_assignment': False,
                                                                                    'normal': False,
                                                                                    'reading': '∀`p[`Symbols] : '
                                                                                               'symmetric(`p) ⇒ '
                                                                                               '(∀x[None]y[None] : '
                                                                                               '`p(x,y) ⇒ `p(y,x))',
                                                                                    'relevant': True,
                                                                                    'status': 'UNIVERSAL',
                                                                                    'typ': 'Bool',
                                                                                    'value': True}},
 'symmetric': {}}
