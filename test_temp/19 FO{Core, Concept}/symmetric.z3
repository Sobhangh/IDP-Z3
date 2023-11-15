
-- original ---------------------------------
vocabulary {
	type node := {a,b,c}
	edge: (node ⨯ node) → Bool
	symmetric: (Concept[node*node -> Bool]) → Bool
    Start: ()→node
	var x in node
	var `q in symmetric
}
theory {
    edge(a,b).
    !`p in Concept[node*node -> Bool]: !x: !y in node: $(`p)(x,y) => $(`p)(y,x).
    !`p in Concept[node*node -> Bool]: symmetric(`p)
				=> (!x: !y in node: $(`p)(x,y) => $(`p)(y,x)).
    !`q, x: !y in node: $(`q)(x,y) => $(`q)(y,x).
	symmetric := {`edge}.
}
display {
	expand := {`edge}.
}
-- meta -------------------------------------
{'manualPropagation': False,
 'manualRelevance': False,
 'optionalPropagation': False,
 'optionalRelevance': False,
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
{' Global': {'env_dec': False},
 'Start': {'Start()': {'environmental': False,
                       'is_assignment': True,
                       'normal': True,
                       'reading': 'Start',
                       'relevant': False,
                       'status': 'UNKNOWN',
                       'typ': 'node',
                       'values': ['a', 'b', 'c']}},
 'edge': {'edge(a, a)': {'environmental': False,
                         'is_assignment': False,
                         'normal': True,
                         'reading': 'edge(a, a)',
                         'relevant': False,
                         'status': 'UNKNOWN',
                         'typ': 'Bool'},
          'edge(a, b)': {'environmental': False,
                         'is_assignment': False,
                         'normal': True,
                         'reading': 'edge(a, b)',
                         'relevant': False,
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
                         'relevant': False,
                         'status': 'UNIVERSAL',
                         'typ': 'Bool',
                         'value': True},
          'edge(b, b)': {'environmental': False,
                         'is_assignment': False,
                         'normal': True,
                         'reading': 'edge(b, b)',
                         'relevant': False,
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
                         'relevant': False,
                         'status': 'UNKNOWN',
                         'typ': 'Bool'},
          '∀ `p ∈ Concept[node*node->𝔹]: symmetric(`p) ⇒ (∀ x: ∀ y ∈ node: $(`p)(x, y) ⇒ $(`p)(y, x))': {'environmental': False,
                                                                                                         'is_assignment': False,
                                                                                                         'normal': False,
                                                                                                         'reading': '∀ '
                                                                                                                    '`p '
                                                                                                                    '∈ '
                                                                                                                    'Concept[node*node->𝔹]: '
                                                                                                                    'symmetric(`p) '
                                                                                                                    '⇒ '
                                                                                                                    '(∀ '
                                                                                                                    'x: '
                                                                                                                    '∀ '
                                                                                                                    'y '
                                                                                                                    '∈ '
                                                                                                                    'node: '
                                                                                                                    '$(`p)(x, '
                                                                                                                    'y) '
                                                                                                                    '⇒ '
                                                                                                                    '$(`p)(y, '
                                                                                                                    'x))',
                                                                                                         'relevant': False,
                                                                                                         'status': 'UNIVERSAL',
                                                                                                         'typ': 'Bool',
                                                                                                         'value': True},
          '∀ `p ∈ Concept[node*node->𝔹]: ∀ x: ∀ y ∈ node: $(`p)(x, y) ⇒ $(`p)(y, x)': {'environmental': False,
                                                                                       'is_assignment': False,
                                                                                       'normal': False,
                                                                                       'reading': '∀ `p ∈ '
                                                                                                  'Concept[node*node->𝔹]: '
                                                                                                  '∀ x: ∀ y ∈ node: '
                                                                                                  '$(`p)(x, y) ⇒ '
                                                                                                  '$(`p)(y, x)',
                                                                                       'relevant': False,
                                                                                       'status': 'UNIVERSAL',
                                                                                       'typ': 'Bool',
                                                                                       'value': True},
          '∀ `q,x: ∀ y ∈ node: $(`q)(x, y) ⇒ $(`q)(y, x)': {'environmental': False,
                                                            'is_assignment': False,
                                                            'normal': False,
                                                            'reading': '∀ `q,x: ∀ y ∈ node: $(`q)(x, y) ⇒ $(`q)(y, x)',
                                                            'relevant': False,
                                                            'status': 'UNIVERSAL',
                                                            'typ': 'Bool',
                                                            'value': True}},
 'symmetric': {}}
