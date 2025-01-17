
-- original ---------------------------------
vocabulary {
    type t_epoxy := {e1, e2, e3}
    type t_cost := {0.539, -1}
    type t_safe_low_storage_t := {0, 15, 16}
    type t_safe_high_storage_t := {10, 25, 38}


    KnownCost, KnownHighStorageT, KnownLowStorageT:() → Bool

    Epoxy: ()→t_epoxy


    ECost:(t_epoxy)→ t_cost
    Min_Cost: ()→Real
    Max_Cost: ()→Real
    [slider: (Min_Cost, Max_Cost) in (0.2, 1)]
    Cost:()→t_cost

    Min_Storage_T: ()→Real
    Max_Storage_T: ()→Real

    ELowest_Storage_T: (t_epoxy)→ t_safe_low_storage_t
    EHighest_Storage_T: (t_epoxy)→ t_safe_high_storage_t
    [slider: (Min_Storage_T, ) in (-25, 25)]
    Safe_Low_Storage_T: ()→t_safe_low_storage_t
    [slider: ( , Max_Storage_T) in (-25, 25)]
    Safe_High_Storage_T: ()→t_safe_high_storage_t



}

theory {
    KnownCost() <=> ECost(Epoxy()) ~= -1. // Default t_cost is -1.
    KnownCost() => Min_Cost() =< ECost(Epoxy()) =< Max_Cost().
    Cost() = ECost(Epoxy()).

    KnownLowStorageT() <=> ELowest_Storage_T(Epoxy()) ~= -900.
    KnownHighStorageT() <=> EHighest_Storage_T(Epoxy()) ~= -900.

    ELowest_Storage_T(Epoxy()) =< Min_Storage_T() =< EHighest_Storage_T(Epoxy()).
    EHighest_Storage_T(Epoxy()) >= Max_Storage_T() >= ELowest_Storage_T(Epoxy()).
    Safe_Low_Storage_T() = ELowest_Storage_T(Epoxy()).
    Safe_High_Storage_T() = EHighest_Storage_T(Epoxy()).
}

structure {
    ECost := {e1 -> 0.539} else -1.
    ELowest_Storage_T := {e1 -> 16, e2-> 0, e3-> 15} else -900.
    EHighest_Storage_T := {e1-> 38, e2-> 10, e3-> 25} else -900.

}

structure default {
    Max_Storage_T := 23. // room temperature
}

display {
    hide(`Max_Storage_T, `Min_Storage_T).
    unit('eur', `ECost, `Min_Cost, `Max_Cost, `Cost).
    unit('degrees', `Min_Storage_T, `Max_Storage_T, `ELowest_Storage_T, `EHighest_Storage_T, `Safe_Low_Storage_T, `Safe_High_Storage_T).


}

-- meta -------------------------------------
{'manualPropagation': False,
 'manualRelevance': False,
 'optionalPropagation': False,
 'optionalRelevance': False,
 'symbols': [{'environmental': False,
              'idpname': 'KnownCost',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'KnownHighStorageT',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'KnownLowStorageT',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Epoxy',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'ECost',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'unit': 'eur',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Min_Cost',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'unit': 'eur',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Max_Cost',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'unit': 'eur',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Cost',
              'priority': 'core',
              'showOptimize': True,
              'slider': {'lower_bound': '0.2',
                         'lower_symbol': 'Min_Cost',
                         'upper_bound': '1',
                         'upper_symbol': 'Max_Cost'},
              'type': 'function',
              'unit': 'eur',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Min_Storage_T',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'unit': 'degrees',
              'view': 'hidden'},
             {'environmental': False,
              'idpname': 'Max_Storage_T',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'unit': 'degrees',
              'view': 'hidden'},
             {'environmental': False,
              'idpname': 'ELowest_Storage_T',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'unit': 'degrees',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'EHighest_Storage_T',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'unit': 'degrees',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Safe_Low_Storage_T',
              'priority': 'core',
              'showOptimize': True,
              'slider': {'lower_bound': '-25',
                         'lower_symbol': 'Min_Storage_T',
                         'upper_bound': '25',
                         'upper_symbol': ''},
              'type': 'function',
              'unit': 'degrees',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Safe_High_Storage_T',
              'priority': 'core',
              'showOptimize': True,
              'slider': {'lower_bound': '-25',
                         'lower_symbol': ' ',
                         'upper_bound': '25',
                         'upper_symbol': 'Max_Storage_T'},
              'type': 'function',
              'unit': 'degrees',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'Cost': {'Cost()': {'environmental': False,
                     'is_assignment': True,
                     'normal': True,
                     'reading': 'Cost',
                     'relevant': True,
                     'status': 'UNKNOWN',
                     'typ': 'Real',
                     'values': ['0.539', '-1']},
          'Cost() = ECost(Epoxy())': {'environmental': False,
                                      'is_assignment': False,
                                      'normal': False,
                                      'reading': 'Cost = ECost(Epoxy)',
                                      'relevant': False,
                                      'status': 'UNIVERSAL',
                                      'typ': 'Bool',
                                      'value': True}},
 'ECost': {},
 'EHighest_Storage_T': {},
 'ELowest_Storage_T': {},
 'Epoxy': {'EHighest_Storage_T(Epoxy()) ≥ Max_Storage_T() ≥ ELowest_Storage_T(Epoxy())': {'environmental': False,
                                                                                          'is_assignment': False,
                                                                                          'normal': False,
                                                                                          'reading': 'EHighest_Storage_T(Epoxy) '
                                                                                                     '≥ Max_Storage_T '
                                                                                                     '≥ '
                                                                                                     'ELowest_Storage_T(Epoxy)',
                                                                                          'relevant': False,
                                                                                          'status': 'UNIVERSAL',
                                                                                          'typ': 'Bool',
                                                                                          'value': True},
           'ELowest_Storage_T(Epoxy()) ≤ Min_Storage_T() ≤ EHighest_Storage_T(Epoxy())': {'environmental': False,
                                                                                          'is_assignment': False,
                                                                                          'normal': False,
                                                                                          'reading': 'ELowest_Storage_T(Epoxy) '
                                                                                                     '≤ Min_Storage_T '
                                                                                                     '≤ '
                                                                                                     'EHighest_Storage_T(Epoxy)',
                                                                                          'relevant': False,
                                                                                          'status': 'UNIVERSAL',
                                                                                          'typ': 'Bool',
                                                                                          'value': True},
           'Epoxy()': {'environmental': False,
                       'is_assignment': True,
                       'normal': True,
                       'reading': 'Epoxy',
                       'relevant': True,
                       'status': 'UNKNOWN',
                       'typ': 't_epoxy',
                       'values': ['e1', 'e2', 'e3']},
           'Epoxy() = e1': {'environmental': False,
                            'is_assignment': True,
                            'normal': False,
                            'reading': 'Epoxy = e1',
                            'relevant': True,
                            'status': 'UNKNOWN',
                            'typ': 'Bool'},
           'Epoxy() = e2': {'environmental': False,
                            'is_assignment': True,
                            'normal': False,
                            'reading': 'Epoxy = e2',
                            'relevant': True,
                            'status': 'CONSEQUENCE',
                            'typ': 'Bool',
                            'value': False},
           'Epoxy() = e3': {'environmental': False,
                            'is_assignment': True,
                            'normal': False,
                            'reading': 'Epoxy = e3',
                            'relevant': True,
                            'status': 'UNKNOWN',
                            'typ': 'Bool'}},
 'KnownCost': {'KnownCost()': {'environmental': False,
                               'is_assignment': False,
                               'normal': True,
                               'reading': 'KnownCost',
                               'relevant': True,
                               'status': 'UNKNOWN',
                               'typ': 'Bool'}},
 'KnownHighStorageT': {'KnownHighStorageT()': {'environmental': False,
                                               'is_assignment': False,
                                               'normal': True,
                                               'reading': 'KnownHighStorageT',
                                               'relevant': False,
                                               'status': 'UNIVERSAL',
                                               'typ': 'Bool',
                                               'value': True}},
 'KnownLowStorageT': {'KnownLowStorageT()': {'environmental': False,
                                             'is_assignment': False,
                                             'normal': True,
                                             'reading': 'KnownLowStorageT',
                                             'relevant': False,
                                             'status': 'UNIVERSAL',
                                             'typ': 'Bool',
                                             'value': True}},
 'Max_Cost': {'Max_Cost()': {'environmental': False,
                             'is_assignment': True,
                             'normal': True,
                             'reading': 'Max_Cost',
                             'relevant': True,
                             'status': 'UNKNOWN',
                             'typ': 'Real'}},
 'Max_Storage_T': {'Max_Storage_T()': {'environmental': False,
                                       'is_assignment': True,
                                       'normal': True,
                                       'reading': 'Max_Storage_T',
                                       'relevant': True,
                                       'status': 'DEFAULT',
                                       'typ': 'Real',
                                       'value': '23'}},
 'Min_Cost': {'Min_Cost()': {'environmental': False,
                             'is_assignment': True,
                             'normal': True,
                             'reading': 'Min_Cost',
                             'relevant': True,
                             'status': 'UNKNOWN',
                             'typ': 'Real'},
              'Min_Cost() ≤ ECost(Epoxy()) ≤ Max_Cost()': {'environmental': False,
                                                           'is_assignment': False,
                                                           'normal': False,
                                                           'reading': 'Min_Cost ≤ ECost(Epoxy) ≤ Max_Cost',
                                                           'relevant': True,
                                                           'status': 'UNKNOWN',
                                                           'typ': 'Bool'}},
 'Min_Storage_T': {'Min_Storage_T()': {'environmental': False,
                                       'is_assignment': True,
                                       'normal': True,
                                       'reading': 'Min_Storage_T',
                                       'relevant': True,
                                       'status': 'UNKNOWN',
                                       'typ': 'Real'}},
 'Safe_High_Storage_T': {'Safe_High_Storage_T()': {'environmental': False,
                                                   'is_assignment': True,
                                                   'normal': True,
                                                   'reading': 'Safe_High_Storage_T',
                                                   'relevant': True,
                                                   'status': 'UNKNOWN',
                                                   'typ': 'Int',
                                                   'values': ['10', '25', '38']},
                         'Safe_High_Storage_T() = EHighest_Storage_T(Epoxy())': {'environmental': False,
                                                                                 'is_assignment': False,
                                                                                 'normal': False,
                                                                                 'reading': 'Safe_High_Storage_T = '
                                                                                            'EHighest_Storage_T(Epoxy)',
                                                                                 'relevant': False,
                                                                                 'status': 'UNIVERSAL',
                                                                                 'typ': 'Bool',
                                                                                 'value': True}},
 'Safe_Low_Storage_T': {'Safe_Low_Storage_T()': {'environmental': False,
                                                 'is_assignment': True,
                                                 'normal': True,
                                                 'reading': 'Safe_Low_Storage_T',
                                                 'relevant': True,
                                                 'status': 'UNKNOWN',
                                                 'typ': 'Int',
                                                 'values': ['0', '15', '16']},
                        'Safe_Low_Storage_T() = ELowest_Storage_T(Epoxy())': {'environmental': False,
                                                                              'is_assignment': False,
                                                                              'normal': False,
                                                                              'reading': 'Safe_Low_Storage_T = '
                                                                                         'ELowest_Storage_T(Epoxy)',
                                                                              'relevant': False,
                                                                              'status': 'UNIVERSAL',
                                                                              'typ': 'Bool',
                                                                              'value': True}}}
