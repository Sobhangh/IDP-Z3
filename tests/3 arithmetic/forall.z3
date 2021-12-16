
-- original ---------------------------------
vocabulary {
    Works: (ℝ) → Bool
    type temp := {0, 1, 2}
    p, q:() → Bool
}
theory {
   p() <=> (!t ∈ temp: 1 < t < 3 => 0 < t < 3).
   q() <=> (!tintin in ℝ: 1 < tintin < 3 => 0 < tintin < 3).
   ?x in Real: Works(x).
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
              'idpname': 'Works',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'Works': {'∃x ∈ ℝ : Works(x)': {'environmental': False,
                                 'is_assignment': False,
                                 'normal': False,
                                 'reading': '∃x ∈ ℝ : Works(x)',
                                 'relevant': True,
                                 'status': 'UNIVERSAL',
                                 'typ': 'Bool',
                                 'value': True}},
 'p': {'p()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'p',
               'relevant': True,
               'status': 'UNIVERSAL',
               'typ': 'Bool',
               'value': True}},
 'q': {'q()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'q',
               'relevant': True,
               'status': 'UNIVERSAL',
               'typ': 'Bool',
               'value': True}}}
