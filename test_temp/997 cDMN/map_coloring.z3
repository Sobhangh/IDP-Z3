
-- original ---------------------------------
// https://dmcommunity.org/challenge/challenge-may-2019/

vocabulary {
	type Country_t := { Belgium, France, Luxembourg, Netherlands, Germany, Denmark }
	type Color_t := { Green, Red, Yellow, Orange }
	Color:(Country_t)→ Color_t
	Country_borders_Country:(Country_t ⨯ Country_t) → Bool
}
theory {
	//Bordering countries can’t share colors
	!c1 in Country_t, c2 in Country_t: Country_borders_Country(c1, c2) => Color(c1) ~= Color(c2).

}


structure {
	Country_borders_Country := {
Belgium	France
Belgium	, Luxembourg
Belgium, Netherlands
Belgium,Germany
Netherlands	Germany
Germany	    France
Germany	    Denmark
Germany	    Luxembourg
France	    Luxembourg }.
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
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Country_borders_Country',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'Color': {'Color(Belgium)': {'environmental': False,
                              'is_assignment': True,
                              'normal': True,
                              'reading': 'Color(Belgium)',
                              'relevant': True,
                              'status': 'UNKNOWN',
                              'typ': 'Color_t',
                              'values': ['Green', 'Red', 'Yellow', 'Orange']},
           'Color(Denmark)': {'environmental': False,
                              'is_assignment': True,
                              'normal': True,
                              'reading': 'Color(Denmark)',
                              'relevant': True,
                              'status': 'UNKNOWN',
                              'typ': 'Color_t',
                              'values': ['Green', 'Red', 'Yellow', 'Orange']},
           'Color(France)': {'environmental': False,
                             'is_assignment': True,
                             'normal': True,
                             'reading': 'Color(France)',
                             'relevant': True,
                             'status': 'UNKNOWN',
                             'typ': 'Color_t',
                             'values': ['Green', 'Red', 'Yellow', 'Orange']},
           'Color(Germany)': {'environmental': False,
                              'is_assignment': True,
                              'normal': True,
                              'reading': 'Color(Germany)',
                              'relevant': True,
                              'status': 'UNKNOWN',
                              'typ': 'Color_t',
                              'values': ['Green', 'Red', 'Yellow', 'Orange']},
           'Color(Luxembourg)': {'environmental': False,
                                 'is_assignment': True,
                                 'normal': True,
                                 'reading': 'Color(Luxembourg)',
                                 'relevant': True,
                                 'status': 'UNKNOWN',
                                 'typ': 'Color_t',
                                 'values': ['Green', 'Red', 'Yellow', 'Orange']},
           'Color(Netherlands)': {'environmental': False,
                                  'is_assignment': True,
                                  'normal': True,
                                  'reading': 'Color(Netherlands)',
                                  'relevant': True,
                                  'status': 'UNKNOWN',
                                  'typ': 'Color_t',
                                  'values': ['Green', 'Red', 'Yellow', 'Orange']},
           '∀ c1 ∈ Country_t,c2 ∈ Country_t: Country_borders_Country(c1, c2) ⇒ Color(c1) ≠ Color(c2)': {'environmental': False,
                                                                                                        'is_assignment': False,
                                                                                                        'normal': False,
                                                                                                        'reading': '∀ '
                                                                                                                   'c1 '
                                                                                                                   '∈ '
                                                                                                                   'Country_t,c2 '
                                                                                                                   '∈ '
                                                                                                                   'Country_t: '
                                                                                                                   'Country_borders_Country(c1, '
                                                                                                                   'c2) '
                                                                                                                   '⇒ '
                                                                                                                   'Color(c1) '
                                                                                                                   '≠ '
                                                                                                                   'Color(c2)',
                                                                                                        'relevant': False,
                                                                                                        'status': 'UNIVERSAL',
                                                                                                        'typ': 'Bool',
                                                                                                        'value': True}},
 'Country_borders_Country': {}}
