
-- original ---------------------------------
vocabulary {
	type node := {a,b,c}
	edge: (node ⨯ node) → Bool
	symmetric: (Symbol) → Bool
    Start: ()→node
}
theory {
    edge(a,b).
    !`p in Symbol: arity(`p)=2 & input_domain(`p,1)=input_domain(`p,1)
				=> (!x: !y in $(input_domain(`p,2)): $(`p)(x,y) => $(`p)(y,x)).
    !`p in Symbol: symmetric(`p)
				=> (!x: !y in $(input_domain(`p,2)): $(`p)(x,y) => $(`p)(y,x)).
    !`p in symmetric: !x: !y in $(input_domain(`p,2)): $(`p)(x,y) => $(`p)(y,x).
	symmetric := {`edge}
}
display {
	expand(`edge).
}
-- meta -------------------------------------
{'manualPropagation': False,
 'optionalPropagation': False,
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
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Start',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'active': '{}', 'env_dec': False},
 'Start': {'Start()': {'environmental': False,
                       'is_assignment': True,
                       'normal': True,
                       'reading': 'Start',
                       'relevant': False,
                       'status': 'UNKNOWN',
                       'typ': 'node',
                       'value': '',
                       'values': []},
           '__rank': 9999},
 'edge': {'__rank': 9999,
          'edge(a, a)': {'environmental': False,
                         'is_assignment': False,
                         'normal': True,
                         'reading': 'edge(a, a)',
                         'relevant': True,
                         'status': 'UNKNOWN',
                         'typ': 'Bool'},
          'edge(a, b)': {'environmental': False,
                         'is_assignment': False,
                         'normal': True,
                         'reading': 'edge(a, b)',
                         'relevant': True,
                         'status': 'UNIVERSAL',
                         'typ': 'Bool',
                         'value': True},
          'edge(a, c)': {'environmental': False,
                         'is_assignment': False,
                         'normal': True,
                         'reading': 'edge(a, c)',
                         'relevant': True,
                         'status': 'UNKNOWN',
                         'typ': 'Bool'},
          'edge(b, a)': {'environmental': False,
                         'is_assignment': False,
                         'normal': True,
                         'reading': 'edge(b, a)',
                         'relevant': True,
                         'status': 'CONSEQUENCE',
                         'typ': 'Bool',
                         'value': True},
          'edge(b, b)': {'environmental': False,
                         'is_assignment': False,
                         'normal': True,
                         'reading': 'edge(b, b)',
                         'relevant': True,
                         'status': 'UNKNOWN',
                         'typ': 'Bool'},
          'edge(b, c)': {'environmental': False,
                         'is_assignment': False,
                         'normal': True,
                         'reading': 'edge(b, c)',
                         'relevant': True,
                         'status': 'UNKNOWN',
                         'typ': 'Bool'},
          'edge(c, a)': {'environmental': False,
                         'is_assignment': False,
                         'normal': True,
                         'reading': 'edge(c, a)',
                         'relevant': True,
                         'status': 'UNKNOWN',
                         'typ': 'Bool'},
          'edge(c, b)': {'environmental': False,
                         'is_assignment': False,
                         'normal': True,
                         'reading': 'edge(c, b)',
                         'relevant': True,
                         'status': 'UNKNOWN',
                         'typ': 'Bool'},
          'edge(c, c)': {'environmental': False,
                         'is_assignment': False,
                         'normal': True,
                         'reading': 'edge(c, c)',
                         'relevant': True,
                         'status': 'UNKNOWN',
                         'typ': 'Bool'},
          '∀`p ∈ Symbol : arity(`p) = 2 ∧ input_domain(`p, 1) = input_domain(`p, 1) ⇒ (∀x ∈ None : ∀y ∈ $(input_domain(`p, 2)) : $(`p)(x, y) ⇒ $(`p)(y, x))': {'environmental': False,
                                                                                                                                                               'is_assignment': False,
                                                                                                                                                               'normal': False,
                                                                                                                                                               'reading': '∀`p '
                                                                                                                                                                          '∈ '
                                                                                                                                                                          'Symbol '
                                                                                                                                                                          ': '
                                                                                                                                                                          'arity(`p) '
                                                                                                                                                                          '= '
                                                                                                                                                                          '2 '
                                                                                                                                                                          '∧ '
                                                                                                                                                                          'input_domain(`p, '
                                                                                                                                                                          '1) '
                                                                                                                                                                          '= '
                                                                                                                                                                          'input_domain(`p, '
                                                                                                                                                                          '1) '
                                                                                                                                                                          '⇒ '
                                                                                                                                                                          '(∀x '
                                                                                                                                                                          '∈ '
                                                                                                                                                                          'None '
                                                                                                                                                                          ': '
                                                                                                                                                                          '∀y '
                                                                                                                                                                          '∈ '
                                                                                                                                                                          '$(input_domain(`p, '
                                                                                                                                                                          '2)) '
                                                                                                                                                                          ': '
                                                                                                                                                                          '$(`p)(x, '
                                                                                                                                                                          'y) '
                                                                                                                                                                          '⇒ '
                                                                                                                                                                          '$(`p)(y, '
                                                                                                                                                                          'x))',
                                                                                                                                                               'relevant': False,
                                                                                                                                                               'status': 'UNIVERSAL',
                                                                                                                                                               'typ': 'Bool',
                                                                                                                                                               'value': True},
          '∀`p ∈ Symbol : symmetric(`p) ⇒ (∀x ∈ None : ∀y ∈ $(input_domain(`p, 2)) : $(`p)(x, y) ⇒ $(`p)(y, x))': {'environmental': False,
                                                                                                                   'is_assignment': False,
                                                                                                                   'normal': False,
                                                                                                                   'reading': '∀`p '
                                                                                                                              '∈ '
                                                                                                                              'Symbol '
                                                                                                                              ': '
                                                                                                                              'symmetric(`p) '
                                                                                                                              '⇒ '
                                                                                                                              '(∀x '
                                                                                                                              '∈ '
                                                                                                                              'None '
                                                                                                                              ': '
                                                                                                                              '∀y '
                                                                                                                              '∈ '
                                                                                                                              '$(input_domain(`p, '
                                                                                                                              '2)) '
                                                                                                                              ': '
                                                                                                                              '$(`p)(x, '
                                                                                                                              'y) '
                                                                                                                              '⇒ '
                                                                                                                              '$(`p)(y, '
                                                                                                                              'x))',
                                                                                                                   'relevant': False,
                                                                                                                   'status': 'UNIVERSAL',
                                                                                                                   'typ': 'Bool',
                                                                                                                   'value': True},
          '∀`p ∈ symmetric : ∀x ∈ None : ∀y ∈ $(input_domain(`p, 2)) : $(`p)(x, y) ⇒ $(`p)(y, x)': {'environmental': False,
                                                                                                    'is_assignment': False,
                                                                                                    'normal': False,
                                                                                                    'reading': '∀`p ∈ '
                                                                                                               'symmetric '
                                                                                                               ': ∀x ∈ '
                                                                                                               'None : '
                                                                                                               '∀y ∈ '
                                                                                                               '$(input_domain(`p, '
                                                                                                               '2)) : '
                                                                                                               '$(`p)(x, '
                                                                                                               'y) ⇒ '
                                                                                                               '$(`p)(y, '
                                                                                                               'x)',
                                                                                                    'relevant': False,
                                                                                                    'status': 'UNIVERSAL',
                                                                                                    'typ': 'Bool',
                                                                                                    'value': True}},
 'symmetric': {}}
