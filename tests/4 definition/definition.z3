
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
 'manualRelevance': False,
 'optionalPropagation': False,
 'optionalRelevance': False,
 'symbols': [{'environmental': False,
              'idpname': 'codeOf',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'active': '{}', 'env_dec': False},
 'codeOf': {'codeOf(blue)': {'environmental': False,
                             'is_assignment': True,
                             'normal': True,
                             'reading': 'codeOf(blue)',
                             'relevant': True,
                             'status': 'CONSEQUENCE',
                             'typ': 'code',
                             'value': 'b',
                             'values': ['b']},
            'codeOf(red)': {'environmental': False,
                            'is_assignment': True,
                            'normal': True,
                            'reading': 'codeOf(red)',
                            'relevant': True,
                            'status': 'CONSEQUENCE',
                            'typ': 'code',
                            'value': 'a',
                            'values': ['a']}}}
