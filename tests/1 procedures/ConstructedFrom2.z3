
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
           '__rank': 9999}}
