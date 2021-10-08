
-- original ---------------------------------
// https://dmcommunity.org/challenge-june-2019/

vocabulary {
	type Country_t := { Belgium, France, Luxembourg, Netherlands, Germany, Denmark }
	type Color_t := { Green, Red, Yellow }
	type Number_t := { 0..10000 }
	Color:(Country_t)→ Color_t
	Violations: ()→Number_t
	Country_borders_Country:(Country_t ⨯ Country_t) → Bool
}
theory {
	//Coloring
	!c1 in Country_t: !c2 in Country_t: c1 ~= Luxembourg & c2 ~= Luxembourg & Country_borders_Country(c1, c2) => Color(c1) ~= Color(c2).

	//Coloring Violations
	Violations() = sum{ : Color(Luxembourg) = Color(France): 257 }+sum{ : Color(Luxembourg) = Color(Germany): 904 }+sum{ : Color(Luxembourg) = Color(Belgium): 568 }.
}


structure {
	Country_borders_Country := {(Belgium,France), (Belgium,Luxembourg), (Belgium,Netherlands),( Belgium,Germany),
	(Netherlands,Germany), (Germany,France), (Germany,Denmark), (Germany,Luxembourg), (France,Luxembourg)}
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
              'idpname': 'Violations',
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
{' Global': {'active': '{}', 'env_dec': False},
 'Color': {'Color(Belgium)': {'environmental': False,
                              'is_assignment': True,
                              'normal': True,
                              'reading': 'Color(Belgium)',
                              'relevant': True,
                              'status': 'UNKNOWN',
                              'typ': 'Color_t',
                              'value': '',
                              'values': []},
           'Color(Denmark)': {'environmental': False,
                              'is_assignment': True,
                              'normal': True,
                              'reading': 'Color(Denmark)',
                              'relevant': True,
                              'status': 'UNKNOWN',
                              'typ': 'Color_t',
                              'value': '',
                              'values': []},
           'Color(France)': {'environmental': False,
                             'is_assignment': True,
                             'normal': True,
                             'reading': 'Color(France)',
                             'relevant': True,
                             'status': 'UNKNOWN',
                             'typ': 'Color_t',
                             'value': '',
                             'values': []},
           'Color(Germany)': {'environmental': False,
                              'is_assignment': True,
                              'normal': True,
                              'reading': 'Color(Germany)',
                              'relevant': True,
                              'status': 'UNKNOWN',
                              'typ': 'Color_t',
                              'value': '',
                              'values': []},
           'Color(Luxembourg)': {'environmental': False,
                                 'is_assignment': True,
                                 'normal': True,
                                 'reading': 'Color(Luxembourg)',
                                 'relevant': True,
                                 'status': 'UNKNOWN',
                                 'typ': 'Color_t',
                                 'value': '',
                                 'values': []},
           'Color(Luxembourg) = Color(Belgium)': {'environmental': False,
                                                  'is_assignment': False,
                                                  'normal': False,
                                                  'reading': 'Color(Luxembourg) = Color(Belgium)',
                                                  'relevant': True,
                                                  'status': 'UNKNOWN',
                                                  'typ': 'Bool'},
           'Color(Luxembourg) = Color(France)': {'environmental': False,
                                                 'is_assignment': False,
                                                 'normal': False,
                                                 'reading': 'Color(Luxembourg) = Color(France)',
                                                 'relevant': True,
                                                 'status': 'UNKNOWN',
                                                 'typ': 'Bool'},
           'Color(Luxembourg) = Color(Germany)': {'environmental': False,
                                                  'is_assignment': False,
                                                  'normal': False,
                                                  'reading': 'Color(Luxembourg) = Color(Germany)',
                                                  'relevant': True,
                                                  'status': 'UNKNOWN',
                                                  'typ': 'Bool'},
           'Color(Netherlands)': {'environmental': False,
                                  'is_assignment': True,
                                  'normal': True,
                                  'reading': 'Color(Netherlands)',
                                  'relevant': True,
                                  'status': 'UNKNOWN',
                                  'typ': 'Color_t',
                                  'value': '',
                                  'values': []},
           '__rank': 9999,
           '∀c1 ∈ Country_t : ∀c2 ∈ Country_t : c1 ≠ Luxembourg ∧ c2 ≠ Luxembourg ∧ Country_borders_Country(c1, c2) ⇒ Color(c1) ≠ Color(c2)': {'environmental': False,
                                                                                                                                               'is_assignment': False,
                                                                                                                                               'normal': False,
                                                                                                                                               'reading': '∀c1 '
                                                                                                                                                          '∈ '
                                                                                                                                                          'Country_t '
                                                                                                                                                          ': '
                                                                                                                                                          '∀c2 '
                                                                                                                                                          '∈ '
                                                                                                                                                          'Country_t '
                                                                                                                                                          ': '
                                                                                                                                                          'c1 '
                                                                                                                                                          '≠ '
                                                                                                                                                          'Luxembourg '
                                                                                                                                                          '∧ '
                                                                                                                                                          'c2 '
                                                                                                                                                          '≠ '
                                                                                                                                                          'Luxembourg '
                                                                                                                                                          '∧ '
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
 'Country_borders_Country': {},
 'Violations': {'Violations()': {'environmental': False,
                                 'is_assignment': True,
                                 'normal': True,
                                 'reading': 'Violations',
                                 'relevant': True,
                                 'status': 'UNKNOWN',
                                 'typ': 'Int',
                                 'value': '',
                                 'values': []},
                'Violations() = sum{ : Color(Luxembourg) = Color(France) : 257} + sum{ : Color(Luxembourg) = Color(Germany) : 904} + sum{ : Color(Luxembourg) = Color(Belgium) : 568}': {'environmental': False,
                                                                                                                                                                                         'is_assignment': False,
                                                                                                                                                                                         'normal': False,
                                                                                                                                                                                         'reading': 'Violations '
                                                                                                                                                                                                    '= '
                                                                                                                                                                                                    'sum{ '
                                                                                                                                                                                                    ': '
                                                                                                                                                                                                    'Color(Luxembourg) '
                                                                                                                                                                                                    '= '
                                                                                                                                                                                                    'Color(France) '
                                                                                                                                                                                                    ': '
                                                                                                                                                                                                    '257} '
                                                                                                                                                                                                    '+ '
                                                                                                                                                                                                    'sum{ '
                                                                                                                                                                                                    ': '
                                                                                                                                                                                                    'Color(Luxembourg) '
                                                                                                                                                                                                    '= '
                                                                                                                                                                                                    'Color(Germany) '
                                                                                                                                                                                                    ': '
                                                                                                                                                                                                    '904} '
                                                                                                                                                                                                    '+ '
                                                                                                                                                                                                    'sum{ '
                                                                                                                                                                                                    ': '
                                                                                                                                                                                                    'Color(Luxembourg) '
                                                                                                                                                                                                    '= '
                                                                                                                                                                                                    'Color(Belgium) '
                                                                                                                                                                                                    ': '
                                                                                                                                                                                                    '568}',
                                                                                                                                                                                         'relevant': True,
                                                                                                                                                                                         'status': 'UNIVERSAL',
                                                                                                                                                                                         'typ': 'Bool',
                                                                                                                                                                                         'value': True},
                '__rank': 9999}}
