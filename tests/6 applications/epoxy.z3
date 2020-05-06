
-- original ---------------------------------
vocabulary {
    type t_epoxy constructed from {e1, e2, e3}
    type t_cost = {0.539; -1}
    type t_safe_low_storage_t = {0; 15; 16}
    type t_safe_high_storage_t = {10; 25; 38}
    

    KnownCost
    KnownHighStorageT
    KnownLowStorageT
    
    Epoxy: t_epoxy
    
    
    ECost(t_epoxy): t_cost
    _Min_Cost: real
    _Max_Cost: real
    [Slider: (_Min_Cost, _Max_Cost): (0.2, 1)]
    Cost: t_cost

    _Min_Storage_T: real
    _Max_Storage_T: real

    ELowest_Storage_T(t_epoxy): t_safe_low_storage_t
    EHighest_Storage_T(t_epoxy): t_safe_high_storage_t 
    [Slider: (_Min_Storage_T, ): (-25, 25)]
    Safe_Low_Storage_T: t_safe_low_storage_t
    [Slider: ( , _Max_Storage_T): (-25, 25)]
    Safe_High_Storage_T: t_safe_high_storage_t 
    


}


theory {
    KnownCost <=> ECost(Epoxy) ~= -1. // Default t_cost is -1.
    KnownCost => _Min_Cost =< ECost(Epoxy) =< _Max_Cost.
    Cost = ECost(Epoxy).  

    KnownLowStorageT <=> ELowest_Storage_T(Epoxy) ~= -900. 
    KnownHighStorageT <=> EHighest_Storage_T(Epoxy) ~= -900.

    ELowest_Storage_T(Epoxy) =< _Min_Storage_T =< EHighest_Storage_T(Epoxy).
    EHighest_Storage_T(Epoxy) >= _Max_Storage_T >= ELowest_Storage_T(Epoxy).
    Safe_Low_Storage_T = ELowest_Storage_T(Epoxy).
    Safe_High_Storage_T = EHighest_Storage_T(Epoxy).
}

structure {
    ECost = {e1, 0.539} else -1
    ELowest_Storage_T = {e1, 16; e2, 0; e3, 15} else -900
    EHighest_Storage_T = {e1, 38; e2, 10; e3, 25} else -900

}
 

-- vocabulary -------------------------------

-- theory -----------------------------------
KnownCost ==
Not(If(Epoxy == e1, 539/1000, ToReal(-1)) == -1)

Or(Not(KnownCost),
   And(_Min_Cost <= If(Epoxy == e1, 539/1000, ToReal(-1)),
       If(Epoxy == e1, 539/1000, ToReal(-1)) <= _Max_Cost))

Cost == If(Epoxy == e1, 539/1000, ToReal(-1))

KnownLowStorageT ==
Not(If(Epoxy == e3,
       15,
       If(Epoxy == e2, 0, If(Epoxy == e1, 16, -900))) ==
    -900)

KnownHighStorageT ==
Not(If(Epoxy == e3,
       25,
       If(Epoxy == e2, 10, If(Epoxy == e1, 38, -900))) ==
    -900)

And(ToReal(If(Epoxy == e3,
              15,
              If(Epoxy == e2, 0, If(Epoxy == e1, 16, -900)))) <=
    _Min_Storage_T,
    _Min_Storage_T <=
    ToReal(If(Epoxy == e3,
              25,
              If(Epoxy == e2, 10, If(Epoxy == e1, 38, -900)))))

And(ToReal(If(Epoxy == e3,
              25,
              If(Epoxy == e2, 10, If(Epoxy == e1, 38, -900)))) >=
    _Max_Storage_T,
    _Max_Storage_T >=
    ToReal(If(Epoxy == e3,
              15,
              If(Epoxy == e2, 0, If(Epoxy == e1, 16, -900)))))

Safe_Low_Storage_T ==
If(Epoxy == e3,
   15,
   If(Epoxy == e2, 0, If(Epoxy == e1, 16, -900)))

Safe_High_Storage_T ==
If(Epoxy == e3,
   25,
   If(Epoxy == e2, 10, If(Epoxy == e1, 38, -900)))

Or(Epoxy == e1, Epoxy == e2, Epoxy == e3)

Or(ECost(e1) == 539/1000, ECost(e1) == -1)

Or(ECost(e2) == 539/1000, ECost(e2) == -1)

Or(ECost(e3) == 539/1000, ECost(e3) == -1)

Or(Cost == 539/1000, Cost == -1)

Or(ELowest_Storage_T(e1) == 0,
   ELowest_Storage_T(e1) == 15,
   ELowest_Storage_T(e1) == 16)

Or(ELowest_Storage_T(e2) == 0,
   ELowest_Storage_T(e2) == 15,
   ELowest_Storage_T(e2) == 16)

Or(ELowest_Storage_T(e3) == 0,
   ELowest_Storage_T(e3) == 15,
   ELowest_Storage_T(e3) == 16)

Or(EHighest_Storage_T(e1) == 10,
   EHighest_Storage_T(e1) == 25,
   EHighest_Storage_T(e1) == 38)

Or(EHighest_Storage_T(e2) == 10,
   EHighest_Storage_T(e2) == 25,
   EHighest_Storage_T(e2) == 38)

Or(EHighest_Storage_T(e3) == 10,
   EHighest_Storage_T(e3) == 25,
   EHighest_Storage_T(e3) == 38)

Or(Safe_Low_Storage_T == 0,
   Safe_Low_Storage_T == 15,
   Safe_Low_Storage_T == 16)

Or(Safe_High_Storage_T == 10,
   Safe_High_Storage_T == 25,
   Safe_High_Storage_T == 38)

-- subtences ------------------------------------
KnownCost
ECost(Epoxy) = -1
_Min_Cost ≤ ECost(Epoxy) ≤ _Max_Cost
Cost = ECost(Epoxy)
KnownLowStorageT
ELowest_Storage_T(Epoxy) = -900
KnownHighStorageT
EHighest_Storage_T(Epoxy) = -900
ELowest_Storage_T(Epoxy) ≤ _Min_Storage_T ≤ EHighest_Storage_T(Epoxy)
EHighest_Storage_T(Epoxy) ≥ _Max_Storage_T ≥ ELowest_Storage_T(Epoxy)
Safe_Low_Storage_T = ELowest_Storage_T(Epoxy)
Safe_High_Storage_T = EHighest_Storage_T(Epoxy)
Epoxy = e1
Epoxy = e2
Epoxy = e3
ECost(e1) = 0.539
ECost(e1) = -1
ECost(e2) = 0.539
ECost(e2) = -1
ECost(e3) = 0.539
ECost(e3) = -1
Cost = 0.539
Cost = -1
ELowest_Storage_T(e1) = 0
ELowest_Storage_T(e1) = 15
ELowest_Storage_T(e1) = 16
ELowest_Storage_T(e2) = 0
ELowest_Storage_T(e2) = 15
ELowest_Storage_T(e2) = 16
ELowest_Storage_T(e3) = 0
ELowest_Storage_T(e3) = 15
ELowest_Storage_T(e3) = 16
EHighest_Storage_T(e1) = 10
EHighest_Storage_T(e1) = 25
EHighest_Storage_T(e1) = 38
EHighest_Storage_T(e2) = 10
EHighest_Storage_T(e2) = 25
EHighest_Storage_T(e2) = 38
EHighest_Storage_T(e3) = 10
EHighest_Storage_T(e3) = 25
EHighest_Storage_T(e3) = 38
Safe_Low_Storage_T = 0
Safe_Low_Storage_T = 15
Safe_Low_Storage_T = 16
Safe_High_Storage_T = 10
Safe_High_Storage_T = 25
Safe_High_Storage_T = 38

-- GUILines ------------------------------------
KnownCost
KnownHighStorageT
KnownLowStorageT
Epoxy
Cost
Safe_Low_Storage_T
Safe_High_Storage_T
ECost(Epoxy) = -1
_Min_Cost ≤ ECost(Epoxy) ≤ _Max_Cost
Cost = ECost(Epoxy)
ELowest_Storage_T(Epoxy) = -900
EHighest_Storage_T(Epoxy) = -900
ELowest_Storage_T(Epoxy) ≤ _Min_Storage_T ≤ EHighest_Storage_T(Epoxy)
EHighest_Storage_T(Epoxy) ≥ _Max_Storage_T ≥ ELowest_Storage_T(Epoxy)
Safe_Low_Storage_T = ELowest_Storage_T(Epoxy)
Safe_High_Storage_T = EHighest_Storage_T(Epoxy)
Epoxy = e1
Epoxy = e2
Epoxy = e3
ECost(e1) = 0.539
ECost(e1) = -1
ECost(e2) = 0.539
ECost(e2) = -1
ECost(e3) = 0.539
ECost(e3) = -1
Cost = 0.539
Cost = -1
ELowest_Storage_T(e1) = 0
ELowest_Storage_T(e1) = 15
ELowest_Storage_T(e1) = 16
ELowest_Storage_T(e2) = 0
ELowest_Storage_T(e2) = 15
ELowest_Storage_T(e2) = 16
ELowest_Storage_T(e3) = 0
ELowest_Storage_T(e3) = 15
ELowest_Storage_T(e3) = 16
EHighest_Storage_T(e1) = 10
EHighest_Storage_T(e1) = 25
EHighest_Storage_T(e1) = 38
EHighest_Storage_T(e2) = 10
EHighest_Storage_T(e2) = 25
EHighest_Storage_T(e2) = 38
EHighest_Storage_T(e3) = 10
EHighest_Storage_T(e3) = 25
EHighest_Storage_T(e3) = 38
Safe_Low_Storage_T = 0
Safe_Low_Storage_T = 15
Safe_Low_Storage_T = 16
Safe_High_Storage_T = 10
Safe_High_Storage_T = 25
Safe_High_Storage_T = 38

-- case -------------------------------------
Type:        
  
Definitions: 
  
Universals:  
  Cost = ECost(Epoxy)
  ELowest_Storage_T(Epoxy) ≤ _Min_Storage_T ≤ EHighest_Storage_T(Epoxy)
  EHighest_Storage_T(Epoxy) ≥ _Max_Storage_T ≥ ELowest_Storage_T(Epoxy)
  Safe_Low_Storage_T = ELowest_Storage_T(Epoxy)
  Safe_High_Storage_T = EHighest_Storage_T(Epoxy)
Consequences:
  KnownLowStorageT
  ~ELowest_Storage_T(Epoxy) = -900
  KnownHighStorageT
  ~EHighest_Storage_T(Epoxy) = -900
Simplified:  
  KnownCost ⇔ ~( if   Epoxy = e1 then 0.539 else -1 = -1)
  KnownCost ⇒ _Min_Cost ≤  if   Epoxy = e1 then 0.539 else -1 ≤ _Max_Cost
  true
  true
  true
  true
  true
  true
  true
  Epoxy = e1 ∨ Epoxy = e2 ∨ Epoxy = e3
  Cost = 0.539 ∨ Cost = -1
  Safe_Low_Storage_T = 0 ∨ Safe_Low_Storage_T = 15 ∨ Safe_Low_Storage_T = 16
  Safe_High_Storage_T = 10 ∨ Safe_High_Storage_T = 25 ∨ Safe_High_Storage_T = 38
Irrelevant:  
  ? ECost(e1) = 0.539
  ? ECost(e1) = -1
  ? ECost(e2) = 0.539
  ? ECost(e2) = -1
  ? ECost(e3) = 0.539
  ? ECost(e3) = -1
  ? ELowest_Storage_T(e1) = 0
  ? ELowest_Storage_T(e1) = 15
  ? ELowest_Storage_T(e1) = 16
  ? ELowest_Storage_T(e2) = 0
  ? ELowest_Storage_T(e2) = 15
  ? ELowest_Storage_T(e2) = 16
  ? ELowest_Storage_T(e3) = 0
  ? ELowest_Storage_T(e3) = 15
  ? ELowest_Storage_T(e3) = 16
  ? EHighest_Storage_T(e1) = 10
  ? EHighest_Storage_T(e1) = 25
  ? EHighest_Storage_T(e1) = 38
  ? EHighest_Storage_T(e2) = 10
  ? EHighest_Storage_T(e2) = 25
  ? EHighest_Storage_T(e2) = 38
  ? EHighest_Storage_T(e3) = 10
  ? EHighest_Storage_T(e3) = 25
  ? EHighest_Storage_T(e3) = 38


-- meta -------------------------------------
{'symbols': [{'idpname': 'KnownCost',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'idpname': 'KnownHighStorageT',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'idpname': 'KnownLowStorageT',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'idpname': 'Epoxy', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'normal'},
             {'idpname': '_Min_Cost', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'normal'},
             {'idpname': '_Max_Cost', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'normal'},
             {'idpname': 'Cost', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'normal'},
             {'idpname': '_Min_Storage_T',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'idpname': '_Max_Storage_T',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'idpname': 'Safe_Low_Storage_T',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'idpname': 'Safe_High_Storage_T',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'Cost': {'Cost': {'environmental': False,
                   'normal': True,
                   'reading': 'Cost',
                   'relevant': True,
                   'status': 'UNKNOWN',
                   'typ': 'Real',
                   'value': '',
                   'values': ['0.539', '-1']},
          'Cost = -1': {'environmental': False,
                        'normal': False,
                        'reading': 'Cost = -1',
                        'relevant': True,
                        'status': 'UNKNOWN',
                        'typ': 'Bool'},
          'Cost = 0.539': {'environmental': False,
                           'normal': False,
                           'reading': 'Cost = 0.539',
                           'relevant': True,
                           'status': 'UNKNOWN',
                           'typ': 'Bool'},
          'Cost = ECost(Epoxy)': {'environmental': False,
                                  'normal': False,
                                  'reading': 'Cost = ECost(Epoxy)',
                                  'relevant': True,
                                  'status': 'UNIVERSAL',
                                  'typ': 'Bool',
                                  'value': True}},
 'Epoxy': {'ECost(Epoxy) = -1': {'environmental': False,
                                 'normal': False,
                                 'reading': 'ECost(Epoxy) = -1',
                                 'relevant': True,
                                 'status': 'UNKNOWN',
                                 'typ': 'Bool'},
           'EHighest_Storage_T(Epoxy) = -900': {'environmental': False,
                                                'normal': False,
                                                'reading': 'EHighest_Storage_T(Epoxy) = -900',
                                                'relevant': True,
                                                'status': 'CONSEQUENCE',
                                                'typ': 'Bool',
                                                'value': False},
           'EHighest_Storage_T(Epoxy) ≥ _Max_Storage_T ≥ ELowest_Storage_T(Epoxy)': {'environmental': False,
                                                                                     'normal': False,
                                                                                     'reading': 'EHighest_Storage_T(Epoxy) '
                                                                                                '≥ _Max_Storage_T ≥ '
                                                                                                'ELowest_Storage_T(Epoxy)',
                                                                                     'relevant': True,
                                                                                     'status': 'UNIVERSAL',
                                                                                     'typ': 'Bool',
                                                                                     'value': True},
           'ELowest_Storage_T(Epoxy) = -900': {'environmental': False,
                                               'normal': False,
                                               'reading': 'ELowest_Storage_T(Epoxy) = -900',
                                               'relevant': True,
                                               'status': 'CONSEQUENCE',
                                               'typ': 'Bool',
                                               'value': False},
           'ELowest_Storage_T(Epoxy) ≤ _Min_Storage_T ≤ EHighest_Storage_T(Epoxy)': {'environmental': False,
                                                                                     'normal': False,
                                                                                     'reading': 'ELowest_Storage_T(Epoxy) '
                                                                                                '≤ _Min_Storage_T ≤ '
                                                                                                'EHighest_Storage_T(Epoxy)',
                                                                                     'relevant': True,
                                                                                     'status': 'UNIVERSAL',
                                                                                     'typ': 'Bool',
                                                                                     'value': True},
           'Epoxy': {'environmental': False,
                     'normal': True,
                     'reading': 'Epoxy',
                     'relevant': True,
                     'status': 'UNKNOWN',
                     'typ': 't_epoxy',
                     'value': '',
                     'values': ['e1', 'e2', 'e3']},
           'Epoxy = e1': {'environmental': False,
                          'normal': False,
                          'reading': 'Epoxy = e1',
                          'relevant': True,
                          'status': 'UNKNOWN',
                          'typ': 'Bool'},
           'Epoxy = e2': {'environmental': False,
                          'normal': False,
                          'reading': 'Epoxy = e2',
                          'relevant': True,
                          'status': 'UNKNOWN',
                          'typ': 'Bool'},
           'Epoxy = e3': {'environmental': False,
                          'normal': False,
                          'reading': 'Epoxy = e3',
                          'relevant': True,
                          'status': 'UNKNOWN',
                          'typ': 'Bool'},
           '_Min_Cost ≤ ECost(Epoxy) ≤ _Max_Cost': {'environmental': False,
                                                    'normal': False,
                                                    'reading': '_Min_Cost ≤ ECost(Epoxy) ≤ _Max_Cost',
                                                    'relevant': True,
                                                    'status': 'UNKNOWN',
                                                    'typ': 'Bool'}},
 'KnownCost': {'KnownCost': {'environmental': False,
                             'normal': True,
                             'reading': 'KnownCost',
                             'relevant': True,
                             'status': 'UNKNOWN',
                             'typ': 'Bool'}},
 'KnownHighStorageT': {'KnownHighStorageT': {'environmental': False,
                                             'normal': True,
                                             'reading': 'KnownHighStorageT',
                                             'relevant': True,
                                             'status': 'CONSEQUENCE',
                                             'typ': 'Bool',
                                             'value': True}},
 'KnownLowStorageT': {'KnownLowStorageT': {'environmental': False,
                                           'normal': True,
                                           'reading': 'KnownLowStorageT',
                                           'relevant': True,
                                           'status': 'CONSEQUENCE',
                                           'typ': 'Bool',
                                           'value': True}},
 'Safe_High_Storage_T': {'Safe_High_Storage_T': {'environmental': False,
                                                 'normal': True,
                                                 'reading': 'Safe_High_Storage_T',
                                                 'relevant': True,
                                                 'status': 'UNKNOWN',
                                                 'typ': 'Int',
                                                 'value': '',
                                                 'values': ['10', '25', '38']},
                         'Safe_High_Storage_T = 10': {'environmental': False,
                                                      'normal': False,
                                                      'reading': 'Safe_High_Storage_T = 10',
                                                      'relevant': True,
                                                      'status': 'UNKNOWN',
                                                      'typ': 'Bool'},
                         'Safe_High_Storage_T = 25': {'environmental': False,
                                                      'normal': False,
                                                      'reading': 'Safe_High_Storage_T = 25',
                                                      'relevant': True,
                                                      'status': 'UNKNOWN',
                                                      'typ': 'Bool'},
                         'Safe_High_Storage_T = 38': {'environmental': False,
                                                      'normal': False,
                                                      'reading': 'Safe_High_Storage_T = 38',
                                                      'relevant': True,
                                                      'status': 'UNKNOWN',
                                                      'typ': 'Bool'},
                         'Safe_High_Storage_T = EHighest_Storage_T(Epoxy)': {'environmental': False,
                                                                             'normal': False,
                                                                             'reading': 'Safe_High_Storage_T = '
                                                                                        'EHighest_Storage_T(Epoxy)',
                                                                             'relevant': True,
                                                                             'status': 'UNIVERSAL',
                                                                             'typ': 'Bool',
                                                                             'value': True}},
 'Safe_Low_Storage_T': {'Safe_Low_Storage_T': {'environmental': False,
                                               'normal': True,
                                               'reading': 'Safe_Low_Storage_T',
                                               'relevant': True,
                                               'status': 'UNKNOWN',
                                               'typ': 'Int',
                                               'value': '',
                                               'values': ['0', '15', '16']},
                        'Safe_Low_Storage_T = 0': {'environmental': False,
                                                   'normal': False,
                                                   'reading': 'Safe_Low_Storage_T = 0',
                                                   'relevant': True,
                                                   'status': 'UNKNOWN',
                                                   'typ': 'Bool'},
                        'Safe_Low_Storage_T = 15': {'environmental': False,
                                                    'normal': False,
                                                    'reading': 'Safe_Low_Storage_T = 15',
                                                    'relevant': True,
                                                    'status': 'UNKNOWN',
                                                    'typ': 'Bool'},
                        'Safe_Low_Storage_T = 16': {'environmental': False,
                                                    'normal': False,
                                                    'reading': 'Safe_Low_Storage_T = 16',
                                                    'relevant': True,
                                                    'status': 'UNKNOWN',
                                                    'typ': 'Bool'},
                        'Safe_Low_Storage_T = ELowest_Storage_T(Epoxy)': {'environmental': False,
                                                                          'normal': False,
                                                                          'reading': 'Safe_Low_Storage_T = '
                                                                                     'ELowest_Storage_T(Epoxy)',
                                                                          'relevant': True,
                                                                          'status': 'UNIVERSAL',
                                                                          'typ': 'Bool',
                                                                          'value': True}},
 '_Max_Storage_T': {},
 '_Min_Storage_T': {}}
