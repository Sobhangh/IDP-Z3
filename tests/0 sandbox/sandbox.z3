
-- original ---------------------------------
vocabulary V {
    type color := {red, blue, green}
    Color: () -> color
    opposite: color → color
}

structure S:V {
    opposite := {red-> green, green-> red}
}

theory T:V {
    opposite(Color()) is enumerated.
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
{' Global': {'active': '{}', 'env_dec': False},
 'Color': {'Color()': {'environmental': False,
                       'is_assignment': True,
                       'normal': True,
                       'reading': 'Color',
                       'relevant': True,
                       'status': 'UNKNOWN',
                       'typ': 'color',
                       'value': '',
                       'values': []},
           '__rank': 9999,
           'opposite(Color())': {'environmental': False,
                                 'is_assignment': True,
                                 'normal': False,
                                 'reading': 'opposite(Color)',
                                 'relevant': True,
                                 'status': 'UNKNOWN',
                                 'typ': 'color',
                                 'value': '',
                                 'values': []},
           'opposite(Color()) is enumerated': {'environmental': False,
                                               'is_assignment': False,
                                               'normal': False,
                                               'reading': 'opposite(Color) is enumerated',
                                               'relevant': True,
                                               'status': 'UNIVERSAL',
                                               'typ': 'Bool',
                                               'value': True}},
 'opposite': {}}
