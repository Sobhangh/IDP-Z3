
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
    expand := {`Color}.
    goal_symbol := {`Color}.
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
              'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'Color': {'Color()': {'environmental': False,
                       'is_assignment': True,
                       'normal': True,
                       'reading': 'Color',
                       'relevant': True,
                       'status': 'UNKNOWN',
                       'typ': 'color',
                       'value': '',
                       'values': ['red', 'blue', 'green', 'rgb(t, t)', 'rgb(t, u)', 'rgb(u, t)', 'rgb(u, u)']}}}
