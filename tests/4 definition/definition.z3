
-- original ---------------------------------
vocabulary {
    type color := {red, blue}
    type code := {a,b}
    codeOf: (color)→ code
}

theory {
    { !cl ∈ color: ! cd ∈ code: codeOf(cl)=cd <- (cl=red & cd=a) | (cl=blue & cd=b). }
}

display {
    view() = expanded.
}

-- meta -------------------------------------
{'manualPropagation': False,
 'optionalPropagation': False,
 'symbols': [{'environmental': False,
              'idpname': 'codeOf',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'active': '{}', 'env_dec': False},
 'codeOf': {'__rank': 9999,
            'codeOf(blue)': {'environmental': False,
                             'is_assignment': True,
                             'normal': True,
                             'reading': 'codeOf(blue)',
                             'relevant': True,
                             'status': 'CONSEQUENCE',
                             'typ': 'code',
                             'value': 'b',
                             'values': ['a', 'b']},
            'codeOf(blue) = a': {'environmental': False,
                                 'is_assignment': True,
                                 'normal': False,
                                 'reading': 'codeOf(blue) = a',
                                 'relevant': True,
                                 'status': 'CONSEQUENCE',
                                 'typ': 'Bool',
                                 'value': False},
            'codeOf(blue) = b': {'environmental': False,
                                 'is_assignment': True,
                                 'normal': False,
                                 'reading': 'codeOf(blue) = b',
                                 'relevant': True,
                                 'status': 'CONSEQUENCE',
                                 'typ': 'Bool',
                                 'value': True},
            'codeOf(red)': {'environmental': False,
                            'is_assignment': True,
                            'normal': True,
                            'reading': 'codeOf(red)',
                            'relevant': True,
                            'status': 'CONSEQUENCE',
                            'typ': 'code',
                            'value': 'a',
                            'values': ['a', 'b']},
            'codeOf(red) = a': {'environmental': False,
                                'is_assignment': True,
                                'normal': False,
                                'reading': 'codeOf(red) = a',
                                'relevant': True,
                                'status': 'CONSEQUENCE',
                                'typ': 'Bool',
                                'value': True},
            'codeOf(red) = b': {'environmental': False,
                                'is_assignment': True,
                                'normal': False,
                                'reading': 'codeOf(red) = b',
                                'relevant': True,
                                'status': 'CONSEQUENCE',
                                'typ': 'Bool',
                                'value': False}}}
