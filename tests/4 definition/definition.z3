
-- original ---------------------------------
vocabulary {
    type color constructed from {red, blue}
    type code constructed from {a,b}
    codeOf: (color)→ code
}

theory {
    { !cl[color]: ! cd[code]: codeOf(cl)=cd <- (cl=red & cd=a) | (cl=blue & cd=b). }
}

display {
    view() = expanded.
}

-- meta -------------------------------------
{'optionalPropagation': False,
 'symbols': [{'environmental': False,
              'idpname': 'codeOf',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'codeOf': {'__rank': 9999,
            'codeOf(blue)': {'environmental': False,
                             'is_assignment': True,
                             'normal': True,
                             'reading': 'codeOf(blue)',
                             'relevant': False,
                             'status': 'CONSEQUENCE',
                             'typ': 'code',
                             'value': 'b',
                             'values': ['a', 'b']},
            'codeOf(blue) = a': {'environmental': False,
                                 'is_assignment': True,
                                 'normal': False,
                                 'reading': 'codeOf(blue) = a',
                                 'relevant': False,
                                 'status': 'CONSEQUENCE',
                                 'typ': 'Bool',
                                 'value': False},
            'codeOf(blue) = b': {'environmental': False,
                                 'is_assignment': True,
                                 'normal': False,
                                 'reading': 'codeOf(blue) = b',
                                 'relevant': False,
                                 'status': 'CONSEQUENCE',
                                 'typ': 'Bool',
                                 'value': True},
            'codeOf(red)': {'environmental': False,
                            'is_assignment': True,
                            'normal': True,
                            'reading': 'codeOf(red)',
                            'relevant': False,
                            'status': 'CONSEQUENCE',
                            'typ': 'code',
                            'value': 'a',
                            'values': ['a', 'b']},
            'codeOf(red) = a': {'environmental': False,
                                'is_assignment': True,
                                'normal': False,
                                'reading': 'codeOf(red) = a',
                                'relevant': False,
                                'status': 'CONSEQUENCE',
                                'typ': 'Bool',
                                'value': True},
            'codeOf(red) = b': {'environmental': False,
                                'is_assignment': True,
                                'normal': False,
                                'reading': 'codeOf(red) = b',
                                'relevant': False,
                                'status': 'CONSEQUENCE',
                                'typ': 'Bool',
                                'value': False}}}
