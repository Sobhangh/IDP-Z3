
-- original ---------------------------------
vocabulary environment {
    Depth : ()→Real
}
vocabulary decision {
    extern vocabulary environment

    type csid := {b, c, d, e, f}
    cSID : ()→csid
}
theory environment:environment {}
theory decision:decision {
     cSID() = b ⇔ 2.104 ≤ Depth() ≤ 2.476.
     cSID() = c ⇔ 2.768 ≤ Depth() ≤ 3.391.
     cSID() = d ⇔ 4.294 ≤ Depth() ≤ 5.206.
     cSID() = e ⇔ 5.474 ≤ Depth() ≤ 6.686.
     cSID() = f ⇔ 8.312 ≤ Depth() ≤ 10.748.
}

display {
    view() = expanded.
}


-- meta -------------------------------------
{'optionalPropagation': False,
 'symbols': [{'environmental': True,
              'idpname': 'Depth',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'expanded'},
             {'environmental': False,
              'idpname': 'cSID',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': True},
 'Depth': {'2.104 ≤ Depth() ≤ 2.476': {'environmental': True,
                                       'is_assignment': False,
                                       'normal': False,
                                       'reading': '2.104 ≤ Depth ≤ 2.476',
                                       'relevant': True,
                                       'status': 'UNKNOWN',
                                       'typ': 'Bool'},
           '2.768 ≤ Depth() ≤ 3.391': {'environmental': True,
                                       'is_assignment': False,
                                       'normal': False,
                                       'reading': '2.768 ≤ Depth ≤ 3.391',
                                       'relevant': True,
                                       'status': 'UNKNOWN',
                                       'typ': 'Bool'},
           '4.294 ≤ Depth() ≤ 5.206': {'environmental': True,
                                       'is_assignment': False,
                                       'normal': False,
                                       'reading': '4.294 ≤ Depth ≤ 5.206',
                                       'relevant': True,
                                       'status': 'UNKNOWN',
                                       'typ': 'Bool'},
           '5.474 ≤ Depth() ≤ 6.686': {'environmental': True,
                                       'is_assignment': False,
                                       'normal': False,
                                       'reading': '5.474 ≤ Depth ≤ 6.686',
                                       'relevant': True,
                                       'status': 'UNKNOWN',
                                       'typ': 'Bool'},
           '8.312 ≤ Depth() ≤ 10.748': {'environmental': True,
                                        'is_assignment': False,
                                        'normal': False,
                                        'reading': '8.312 ≤ Depth ≤ 10.748',
                                        'relevant': True,
                                        'status': 'UNKNOWN',
                                        'typ': 'Bool'},
           'Depth()': {'environmental': True,
                       'is_assignment': True,
                       'normal': True,
                       'reading': 'Depth',
                       'relevant': True,
                       'status': 'UNKNOWN',
                       'typ': 'Real',
                       'value': ''},
           '__rank': 9999},
 'cSID': {'__rank': 9999,
          'cSID()': {'environmental': False,
                     'is_assignment': True,
                     'normal': True,
                     'reading': 'cSID',
                     'relevant': True,
                     'status': 'UNKNOWN',
                     'typ': 'csid',
                     'value': '',
                     'values': ['b', 'c', 'd', 'e', 'f']},
          'cSID() = b': {'environmental': False,
                         'is_assignment': True,
                         'normal': False,
                         'reading': 'cSID = b',
                         'relevant': True,
                         'status': 'UNKNOWN',
                         'typ': 'Bool'},
          'cSID() = c': {'environmental': False,
                         'is_assignment': True,
                         'normal': False,
                         'reading': 'cSID = c',
                         'relevant': True,
                         'status': 'UNKNOWN',
                         'typ': 'Bool'},
          'cSID() = d': {'environmental': False,
                         'is_assignment': True,
                         'normal': False,
                         'reading': 'cSID = d',
                         'relevant': True,
                         'status': 'UNKNOWN',
                         'typ': 'Bool'},
          'cSID() = e': {'environmental': False,
                         'is_assignment': True,
                         'normal': False,
                         'reading': 'cSID = e',
                         'relevant': True,
                         'status': 'UNKNOWN',
                         'typ': 'Bool'},
          'cSID() = f': {'environmental': False,
                         'is_assignment': True,
                         'normal': False,
                         'reading': 'cSID = f',
                         'relevant': True,
                         'status': 'UNKNOWN',
                         'typ': 'Bool'}}}
