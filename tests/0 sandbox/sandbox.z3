
-- original ---------------------------------
vocabulary V {
    type color constructed from {red, blue, green}
    Color: color
    opposite(color): color
}

structure S:V {
    opposite := {(red, green), (green, red)}
}

theory T:V {
    opposite(Color) is enumerated.
}


display {
  view = expanded.
}
-- meta -------------------------------------
{'optionalPropagation': False,
 'symbols': [{'environmental': False,
              'idpname': 'Color',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'expanded'},
             {'environmental': False,
              'idpname': 'opposite',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'Color': {'Color': {'environmental': False,
                     'is_assignment': True,
                     'normal': True,
                     'reading': 'Color',
                     'relevant': True,
                     'status': 'UNKNOWN',
                     'typ': 'color',
                     'value': '',
                     'values': ['red', 'blue', 'green']},
           'Color = blue': {'environmental': False,
                            'is_assignment': True,
                            'normal': False,
                            'reading': 'Color = blue',
                            'relevant': True,
                            'status': 'CONSEQUENCE',
                            'typ': 'Bool',
                            'value': False},
           'Color = green': {'environmental': False,
                             'is_assignment': True,
                             'normal': False,
                             'reading': 'Color = green',
                             'relevant': True,
                             'status': 'UNKNOWN',
                             'typ': 'Bool'},
           'Color = red': {'environmental': False,
                           'is_assignment': True,
                           'normal': False,
                           'reading': 'Color = red',
                           'relevant': True,
                           'status': 'UNKNOWN',
                           'typ': 'Bool'},
           '__rank': 1,
           'opposite(Color) is enumerated': {'environmental': False,
                                             'is_assignment': False,
                                             'normal': False,
                                             'reading': 'opposite(Color) is enumerated',
                                             'relevant': True,
                                             'status': 'UNIVERSAL',
                                             'typ': 'Bool',
                                             'value': True}},
 'opposite': {}}
