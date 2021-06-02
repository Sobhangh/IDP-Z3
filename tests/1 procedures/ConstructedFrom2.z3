
-- original ---------------------------------
vocabulary V {
    type byte := {t,u}
    type color := constructed from {red, blue, green, rgb(R: byte, byte)}
    Color: () -> color
}

theory T:V {
    R(rgb(t,u)) = t.
}
display {
    goal(`Color).
}

-- meta -------------------------------------
{'manualPropagation': False,
 'optionalPropagation': False,
 'symbols': [{'environmental': False,
              'idpname': 'Color',
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
           'Color() = blue': {'environmental': False,
                              'is_assignment': True,
                              'normal': False,
                              'reading': 'Color = blue',
                              'relevant': True,
                              'status': 'UNKNOWN',
                              'typ': 'Bool'},
           'Color() = green': {'environmental': False,
                               'is_assignment': True,
                               'normal': False,
                               'reading': 'Color = green',
                               'relevant': True,
                               'status': 'UNKNOWN',
                               'typ': 'Bool'},
           'Color() = red': {'environmental': False,
                             'is_assignment': True,
                             'normal': False,
                             'reading': 'Color = red',
                             'relevant': True,
                             'status': 'UNKNOWN',
                             'typ': 'Bool'},
           'Color() = rgb(t, t)': {'environmental': False,
                                   'is_assignment': False,
                                   'normal': False,
                                   'reading': 'Color = rgb(t, t)',
                                   'relevant': True,
                                   'status': 'UNKNOWN',
                                   'typ': 'Bool'},
           'Color() = rgb(t, u)': {'environmental': False,
                                   'is_assignment': False,
                                   'normal': False,
                                   'reading': 'Color = rgb(t, u)',
                                   'relevant': True,
                                   'status': 'UNKNOWN',
                                   'typ': 'Bool'},
           'Color() = rgb(u, t)': {'environmental': False,
                                   'is_assignment': False,
                                   'normal': False,
                                   'reading': 'Color = rgb(u, t)',
                                   'relevant': True,
                                   'status': 'UNKNOWN',
                                   'typ': 'Bool'},
           'Color() = rgb(u, u)': {'environmental': False,
                                   'is_assignment': False,
                                   'normal': False,
                                   'reading': 'Color = rgb(u, u)',
                                   'relevant': True,
                                   'status': 'UNKNOWN',
                                   'typ': 'Bool'},
           '__rank': 9999}}
