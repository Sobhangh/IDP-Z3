
-- original ---------------------------------
vocabulary environment {
    type material := {e1, e2, e3}
    _MinT:(material)→ Int // physical
    _MaxT:(material)→ Int
    _O:(material) → Bool         // observed
    OMinT:(material)→ Int // observations
    OMaxT:(material)→ Int

}

vocabulary decision {
    extern vocabulary environment

    T: ()→Int
    M: ()→material
    Guaranteed:() → Bool
}

theory environment:environment {
    [Observations are accurate]
    ( (! m in material: _O(m) => OMinT(m)=_MinT(m))
    & (! m in material: _O(m) => OMaxT(m)=_MaxT(m))
    ).

    [Observation for e1]
    (_O(e1) &  OMinT(e1)= 0 &   OMaxT(e1) = 20).

    [Observation for e2]
    (_O(e2) &  OMinT(e2)= 0 &   OMaxT(e2) = 100).

    [No observation for e3]
    (~_O(e3)).
}

theory decision:decision {
    [T must be within acceptable range]
    (_MinT(M()) =< T() =< _MaxT(M())).

    [A guarantee requires an observation for M]
    (Guaranteed() <=> _O(M())).

    M()=e1 | M()=e2 | M()=e3.
}

display {
    goal(`M).
    view() = expanded.
}
-- meta -------------------------------------
{'manualPropagation': False,
 'optionalPropagation': False,
 'symbols': [{'environmental': True,
              'idpname': 'OMinT',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'expanded'},
             {'environmental': True,
              'idpname': 'OMaxT',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'expanded'},
             {'environmental': False,
              'idpname': 'T',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'expanded'},
             {'environmental': False,
              'idpname': 'M',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'expanded'},
             {'environmental': False,
              'idpname': 'Guaranteed',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'active': '{}', 'env_dec': True},
 'Guaranteed': {'Guaranteed()': {'environmental': False,
                                 'is_assignment': False,
                                 'normal': True,
                                 'reading': 'Guaranteed',
                                 'relevant': True,
                                 'status': 'UNKNOWN',
                                 'typ': 'Bool'},
                '__rank': 9999},
 'M': {'M()': {'environmental': False,
               'is_assignment': True,
               'normal': True,
               'reading': 'M',
               'relevant': True,
               'status': 'UNKNOWN',
               'typ': 'material',
               'value': '',
               'values': []},
       'M() = e1': {'environmental': False,
                    'is_assignment': True,
                    'normal': False,
                    'reading': 'M = e1',
                    'relevant': True,
                    'status': 'UNKNOWN',
                    'typ': 'Bool'},
       'M() = e2': {'environmental': False,
                    'is_assignment': True,
                    'normal': False,
                    'reading': 'M = e2',
                    'relevant': True,
                    'status': 'UNKNOWN',
                    'typ': 'Bool'},
       'M() = e3': {'environmental': False,
                    'is_assignment': True,
                    'normal': False,
                    'reading': 'M = e3',
                    'relevant': True,
                    'status': 'UNKNOWN',
                    'typ': 'Bool'},
       '_MaxT(M())': {'environmental': False,
                      'is_assignment': True,
                      'normal': False,
                      'reading': '_MaxT(M)',
                      'relevant': True,
                      'status': 'UNKNOWN',
                      'typ': 'material',
                      'value': '',
                      'values': []},
       '_MinT(M())': {'environmental': False,
                      'is_assignment': True,
                      'normal': False,
                      'reading': '_MinT(M)',
                      'relevant': True,
                      'status': 'UNKNOWN',
                      'typ': 'material',
                      'value': '',
                      'values': []},
       '_MinT(M()) ≤ T() ≤ _MaxT(M())': {'environmental': False,
                                         'is_assignment': False,
                                         'normal': False,
                                         'reading': 'T must be within acceptable range',
                                         'relevant': True,
                                         'status': 'UNIVERSAL',
                                         'typ': 'Bool',
                                         'value': True},
       '_O(M())': {'environmental': False,
                   'is_assignment': False,
                   'normal': False,
                   'reading': '_O(M)',
                   'relevant': True,
                   'status': 'UNKNOWN',
                   'typ': 'Bool'},
       '__rank': 9999},
 'OMaxT': {'OMaxT(e1)': {'environmental': True,
                         'is_assignment': True,
                         'normal': True,
                         'reading': 'OMaxT(e1)',
                         'relevant': False,
                         'status': 'ENV_UNIV',
                         'typ': 'Int',
                         'value': '20'},
           'OMaxT(e1) = 20': {'environmental': True,
                              'is_assignment': True,
                              'normal': False,
                              'reading': 'OMaxT(e1) = 20',
                              'relevant': False,
                              'status': 'ENV_UNIV',
                              'typ': 'Bool',
                              'value': True},
           'OMaxT(e2)': {'environmental': True,
                         'is_assignment': True,
                         'normal': True,
                         'reading': 'OMaxT(e2)',
                         'relevant': False,
                         'status': 'ENV_UNIV',
                         'typ': 'Int',
                         'value': '100'},
           'OMaxT(e2) = 100': {'environmental': True,
                               'is_assignment': True,
                               'normal': False,
                               'reading': 'OMaxT(e2) = 100',
                               'relevant': False,
                               'status': 'ENV_UNIV',
                               'typ': 'Bool',
                               'value': True},
           'OMaxT(e3)': {'environmental': True,
                         'is_assignment': True,
                         'normal': True,
                         'reading': 'OMaxT(e3)',
                         'relevant': False,
                         'status': 'UNKNOWN',
                         'typ': 'Int',
                         'value': ''},
           '__rank': 9999,
           '∀m ∈ material : _O(m) ⇒ OMaxT(m) = _MaxT(m)': {'environmental': True,
                                                           'is_assignment': False,
                                                           'normal': False,
                                                           'reading': '∀m ∈ material : _O(m) ⇒ OMaxT(m) = _MaxT(m)',
                                                           'relevant': False,
                                                           'status': 'ENV_UNIV',
                                                           'typ': 'Bool',
                                                           'value': True}},
 'OMinT': {'OMinT(e1)': {'environmental': True,
                         'is_assignment': True,
                         'normal': True,
                         'reading': 'OMinT(e1)',
                         'relevant': False,
                         'status': 'ENV_UNIV',
                         'typ': 'Int',
                         'value': '0'},
           'OMinT(e1) = 0': {'environmental': True,
                             'is_assignment': True,
                             'normal': False,
                             'reading': 'OMinT(e1) = 0',
                             'relevant': False,
                             'status': 'ENV_UNIV',
                             'typ': 'Bool',
                             'value': True},
           'OMinT(e2)': {'environmental': True,
                         'is_assignment': True,
                         'normal': True,
                         'reading': 'OMinT(e2)',
                         'relevant': False,
                         'status': 'ENV_UNIV',
                         'typ': 'Int',
                         'value': '0'},
           'OMinT(e2) = 0': {'environmental': True,
                             'is_assignment': True,
                             'normal': False,
                             'reading': 'OMinT(e2) = 0',
                             'relevant': False,
                             'status': 'ENV_UNIV',
                             'typ': 'Bool',
                             'value': True},
           'OMinT(e3)': {'environmental': True,
                         'is_assignment': True,
                         'normal': True,
                         'reading': 'OMinT(e3)',
                         'relevant': False,
                         'status': 'UNKNOWN',
                         'typ': 'Int',
                         'value': ''},
           '__rank': 9999,
           '∀m ∈ material : _O(m) ⇒ OMinT(m) = _MinT(m)': {'environmental': True,
                                                           'is_assignment': False,
                                                           'normal': False,
                                                           'reading': '∀m ∈ material : _O(m) ⇒ OMinT(m) = _MinT(m)',
                                                           'relevant': False,
                                                           'status': 'ENV_UNIV',
                                                           'typ': 'Bool',
                                                           'value': True}},
 'T': {'T()': {'environmental': False,
               'is_assignment': True,
               'normal': True,
               'reading': 'T',
               'relevant': True,
               'status': 'UNKNOWN',
               'typ': 'Int',
               'value': ''},
       '__rank': 9999}}
