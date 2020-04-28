
-- original ---------------------------------
vocabulary environment {
    type material constructed from {e1, e2, e3}
    _MinT(material): int
    _MaxT(material): int

}

vocabulary decision {
    type material constructed from {e1, e2, e3}
    _O(material)
    OMinT(material): int
    OMaxT(material): int
    T: int
    M: material
    Guaranteed
}

theory {
    [Observations of MinT are accurate]
    (! m[material]: _O(m) => OMinT(m)=_MinT(m)).
    [Observations of MaxT are accurate]
    (! m[material]: _O(m) => OMaxT(m)=_MaxT(m)).

    [T must be within acceptable range]
    (_MinT(M) =< T =< _MaxT(M)).

    [A guarantee requires an observation for M]
    (Guaranteed <=> _O(M)).

    [Observation for e1]
    (_O(e1) &  OMinT(e1)= 0 &   OMaxT(e1) = 20).

    [Observation for e2]
    (_O(e2) &  OMinT(e2)= 0 &   OMaxT(e2) = 100).

    [No observation for e3]
    (~_O(e3)).
    
    M=e1 | M=e2 | M=e3.
}

goal M
view normal
-- vocabulary -------------------------------

-- theory -----------------------------------
And(Or(Not(_O(e1)), OMinT(e1) == _MinT(e1)),
    Or(Not(_O(e2)), OMinT(e2) == _MinT(e2)),
    Or(Not(_O(e3)), OMinT(e3) == _MinT(e3)))

And(Or(Not(_O(e1)), OMaxT(e1) == _MaxT(e1)),
    Or(Not(_O(e2)), OMaxT(e2) == _MaxT(e2)),
    Or(Not(_O(e3)), OMaxT(e3) == _MaxT(e3)))

And(_MinT(M) <= T, T <= _MaxT(M))

Guaranteed == _O(M)

And(_O(e1), OMinT(e1) == 0, OMaxT(e1) == 20)

And(_O(e2), OMinT(e2) == 0, OMaxT(e2) == 100)

Not(_O(e3))

Or(M == e1, M == e2, M == e3)

Or(M == e1, M == e2, M == e3)

Or(M == e1, M == e2, M == e3)

-- subtences ------------------------------------
∀m[material] : _O(m) ⇒ (OMinT(m) = _MinT(m))
∀m[material] : _O(m) ⇒ (OMaxT(m) = _MaxT(m))
_MinT(M) ≤ T ≤ _MaxT(M)
Guaranteed
_O(M)
_O(e1)
OMinT(e1) = 0
OMaxT(e1) = 20
_O(e2)
OMinT(e2) = 0
OMaxT(e2) = 100
_O(e3)
M = e1
M = e2
M = e3

-- GUILines ------------------------------------
OMinT(e1)
OMinT(e2)
OMinT(e3)
OMaxT(e1)
OMaxT(e2)
OMaxT(e3)
T
M
Guaranteed
∀m[material] : _O(m) ⇒ (OMinT(m) = _MinT(m))
∀m[material] : _O(m) ⇒ (OMaxT(m) = _MaxT(m))
_MinT(M) ≤ T ≤ _MaxT(M)
_O(M)
_O(e1)
OMinT(e1) = 0
OMaxT(e1) = 20
_O(e2)
OMinT(e2) = 0
OMaxT(e2) = 100
_O(e3)
M = e1
M = e2
M = e3

-- case -------------------------------------
Type:        
  
Definitions: 
  
Universals:  
  ∀m[material] : _O(m) ⇒ (OMinT(m) = _MinT(m))
  ∀m[material] : _O(m) ⇒ (OMaxT(m) = _MaxT(m))
  _MinT(M) ≤ T ≤ _MaxT(M)
  _O(e1)
  OMinT(e1) = 0
  OMaxT(e1) = 20
  _O(e2)
  OMinT(e2) = 0
  OMaxT(e2) = 100
  ~_O(e3)
  OMinT(e1) -> 0
  OMaxT(e1) -> 20
  OMinT(e2) -> 0
  OMaxT(e2) -> 100
Consequences:
  
Simplified:  
  (true)
  (true)
  (true)
  (Guaranteed ⇔ _O(M))
  (true)
  (true)
  (true)
  (M = e1) ∨ (M = e2) ∨ (M = e3)
  (M = e1) ∨ (M = e2) ∨ (M = e3)
  (M = e1) ∨ (M = e2) ∨ (M = e3)
Irrelevant:  
  


-- meta -------------------------------------
{'symbols': [{'idpname': '_MinT', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'normal'},
             {'idpname': '_MaxT', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'normal'},
             {'idpname': '_O', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'normal'},
             {'idpname': 'OMinT', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'normal'},
             {'idpname': 'OMaxT', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'normal'},
             {'idpname': 'T', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'normal'},
             {'idpname': 'M', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'},
             {'idpname': 'Guaranteed',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': True},
 'Guaranteed': {'Guaranteed': {'environmental': False,
                               'normal': True,
                               'reading': 'Guaranteed',
                               'relevant': True,
                               'status': 'UNKNOWN',
                               'typ': 'Bool'}},
 'M': {'M': {'environmental': False,
             'normal': True,
             'reading': 'M',
             'relevant': True,
             'status': 'UNKNOWN',
             'typ': 'material',
             'value': '',
             'values': ['e1', 'e2', 'e3']},
       'M = e1': {'environmental': False,
                  'normal': False,
                  'reading': 'M = e1',
                  'relevant': True,
                  'status': 'UNKNOWN',
                  'typ': 'Bool'},
       'M = e2': {'environmental': False,
                  'normal': False,
                  'reading': 'M = e2',
                  'relevant': True,
                  'status': 'UNKNOWN',
                  'typ': 'Bool'},
       'M = e3': {'environmental': False,
                  'normal': False,
                  'reading': 'M = e3',
                  'relevant': True,
                  'status': 'UNKNOWN',
                  'typ': 'Bool'},
       '_MinT(M) ≤ T ≤ _MaxT(M)': {'environmental': True,
                                   'normal': False,
                                   'reading': 'T must be within acceptable range',
                                   'relevant': True,
                                   'status': 'UNIVERSAL',
                                   'typ': 'Bool',
                                   'value': True},
       '_O(M)': {'environmental': False,
                 'normal': True,
                 'reading': '_O(M)',
                 'relevant': True,
                 'status': 'UNKNOWN',
                 'typ': 'Bool'}},
 'OMaxT': {'OMaxT(e1)': {'environmental': False,
                         'normal': True,
                         'reading': 'OMaxT(e1)',
                         'relevant': True,
                         'status': 'UNIVERSAL',
                         'typ': 'Int',
                         'value': '20'},
           'OMaxT(e1) = 20': {'environmental': False,
                              'normal': False,
                              'reading': 'OMaxT(e1) = 20',
                              'relevant': True,
                              'status': 'UNIVERSAL',
                              'typ': 'Bool',
                              'value': True},
           'OMaxT(e2)': {'environmental': False,
                         'normal': True,
                         'reading': 'OMaxT(e2)',
                         'relevant': True,
                         'status': 'UNIVERSAL',
                         'typ': 'Int',
                         'value': '100'},
           'OMaxT(e2) = 100': {'environmental': False,
                               'normal': False,
                               'reading': 'OMaxT(e2) = 100',
                               'relevant': True,
                               'status': 'UNIVERSAL',
                               'typ': 'Bool',
                               'value': True},
           'OMaxT(e3)': {'environmental': False,
                         'normal': True,
                         'reading': 'OMaxT(e3)',
                         'relevant': True,
                         'status': 'UNKNOWN',
                         'typ': 'Int',
                         'value': ''},
           '∀m[material] : _O(m) ⇒ (OMaxT(m) = _MaxT(m))': {'environmental': True,
                                                            'normal': False,
                                                            'reading': 'Observations of MaxT are accurate',
                                                            'relevant': True,
                                                            'status': 'UNIVERSAL',
                                                            'typ': 'Bool',
                                                            'value': True}},
 'OMinT': {'OMinT(e1)': {'environmental': False,
                         'normal': True,
                         'reading': 'OMinT(e1)',
                         'relevant': True,
                         'status': 'UNIVERSAL',
                         'typ': 'Int',
                         'value': '0'},
           'OMinT(e1) = 0': {'environmental': False,
                             'normal': False,
                             'reading': 'OMinT(e1) = 0',
                             'relevant': True,
                             'status': 'UNIVERSAL',
                             'typ': 'Bool',
                             'value': True},
           'OMinT(e2)': {'environmental': False,
                         'normal': True,
                         'reading': 'OMinT(e2)',
                         'relevant': True,
                         'status': 'UNIVERSAL',
                         'typ': 'Int',
                         'value': '0'},
           'OMinT(e2) = 0': {'environmental': False,
                             'normal': False,
                             'reading': 'OMinT(e2) = 0',
                             'relevant': True,
                             'status': 'UNIVERSAL',
                             'typ': 'Bool',
                             'value': True},
           'OMinT(e3)': {'environmental': False,
                         'normal': True,
                         'reading': 'OMinT(e3)',
                         'relevant': True,
                         'status': 'UNKNOWN',
                         'typ': 'Int',
                         'value': ''},
           '∀m[material] : _O(m) ⇒ (OMinT(m) = _MinT(m))': {'environmental': True,
                                                            'normal': False,
                                                            'reading': 'Observations of MinT are accurate',
                                                            'relevant': True,
                                                            'status': 'UNIVERSAL',
                                                            'typ': 'Bool',
                                                            'value': True}},
 'T': {'T': {'environmental': False,
             'normal': True,
             'reading': 'T',
             'relevant': True,
             'status': 'UNKNOWN',
             'typ': 'Int',
             'value': ''}},
 '_MaxT': {},
 '_MinT': {},
 '_O': {}}
