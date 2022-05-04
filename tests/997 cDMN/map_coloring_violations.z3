
-- original ---------------------------------
// https://dmcommunity.org/challenge-june-2019/

vocabulary {
	type Country_t := { Belgium, France, Luxembourg, Netherlands, Germany, Denmark }
	type Color_t := { Green, Red, Yellow }
	Color:(Country_t)→ Color_t
	Violations: ()→Int
	Country_borders_Country:(Country_t ⨯ Country_t) → Bool
}
theory {
	//Coloring
	!c1 in Country_t: !c2 in Country_t: c1 ~= Luxembourg & c2 ~= Luxembourg & Country_borders_Country(c1, c2) => Color(c1) ~= Color(c2).

	//Coloring Violations
	Violations() = sum(lambda : if Color(Luxembourg) = Color(France) then 257 else 0)+sum(lambda : if Color(Luxembourg) = Color(Germany) then 904 else 0)+sum(lambda : if Color(Luxembourg) = Color(Belgium) then 568 else 0).
}


structure {
	Country_borders_Country := {(Belgium,France), (Belgium,Luxembourg), (Belgium,Netherlands),( Belgium,Germany),
	(Netherlands,Germany), (Germany,France), (Germany,Denmark), (Germany,Luxembourg), (France,Luxembourg)}.
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
{' Global': {'env_dec': False},
 'Color': {'Color(Belgium)': {'environmental': False,
                              'is_assignment': True,
                              'normal': True,
                              'reading': 'Color(Belgium)',
                              'relevant': True,
                              'status': 'UNKNOWN',
                              'typ': 'Color_t',
                              'value': '',
                              'values': ['Green', 'Red', 'Yellow']},
           'Color(Denmark)': {'environmental': False,
                              'is_assignment': True,
                              'normal': True,
                              'reading': 'Color(Denmark)',
                              'relevant': True,
                              'status': 'UNKNOWN',
                              'typ': 'Color_t',
                              'value': '',
                              'values': ['Green', 'Red', 'Yellow']},
           'Color(France)': {'environmental': False,
                             'is_assignment': True,
                             'normal': True,
                             'reading': 'Color(France)',
                             'relevant': True,
                             'status': 'UNKNOWN',
                             'typ': 'Color_t',
                             'value': '',
                             'values': ['Green', 'Red', 'Yellow']},
           'Color(Germany)': {'environmental': False,
                              'is_assignment': True,
                              'normal': True,
                              'reading': 'Color(Germany)',
                              'relevant': True,
                              'status': 'UNKNOWN',
                              'typ': 'Color_t',
                              'value': '',
                              'values': ['Green', 'Red', 'Yellow']},
           'Color(Luxembourg)': {'environmental': False,
                                 'is_assignment': True,
                                 'normal': True,
                                 'reading': 'Color(Luxembourg)',
                                 'relevant': True,
                                 'status': 'UNKNOWN',
                                 'typ': 'Color_t',
                                 'value': '',
                                 'values': ['Green', 'Red', 'Yellow']},
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
                                  'values': ['Green', 'Red', 'Yellow']},
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
                                 'value': ''},
                'Violations() = sum(lambda  :  if   Color(Luxembourg) = Color(France) then 257 else 0) + sum(lambda  :  if   Color(Luxembourg) = Color(Germany) then 904 else 0) + sum(lambda  :  if   Color(Luxembourg) = Color(Belgium) then 568 else 0)': {'environmental': False,
                                                                                                                                                                                                                                                              'is_assignment': False,
                                                                                                                                                                                                                                                              'normal': False,
                                                                                                                                                                                                                                                              'reading': 'Violations '
                                                                                                                                                                                                                                                                         '= '
                                                                                                                                                                                                                                                                         'sum(lambda  '
                                                                                                                                                                                                                                                                         ':  '
                                                                                                                                                                                                                                                                         'if   '
                                                                                                                                                                                                                                                                         'Color(Luxembourg) '
                                                                                                                                                                                                                                                                         '= '
                                                                                                                                                                                                                                                                         'Color(France) '
                                                                                                                                                                                                                                                                         'then '
                                                                                                                                                                                                                                                                         '257 '
                                                                                                                                                                                                                                                                         'else '
                                                                                                                                                                                                                                                                         '0) '
                                                                                                                                                                                                                                                                         '+ '
                                                                                                                                                                                                                                                                         'sum(lambda  '
                                                                                                                                                                                                                                                                         ':  '
                                                                                                                                                                                                                                                                         'if   '
                                                                                                                                                                                                                                                                         'Color(Luxembourg) '
                                                                                                                                                                                                                                                                         '= '
                                                                                                                                                                                                                                                                         'Color(Germany) '
                                                                                                                                                                                                                                                                         'then '
                                                                                                                                                                                                                                                                         '904 '
                                                                                                                                                                                                                                                                         'else '
                                                                                                                                                                                                                                                                         '0) '
                                                                                                                                                                                                                                                                         '+ '
                                                                                                                                                                                                                                                                         'sum(lambda  '
                                                                                                                                                                                                                                                                         ':  '
                                                                                                                                                                                                                                                                         'if   '
                                                                                                                                                                                                                                                                         'Color(Luxembourg) '
                                                                                                                                                                                                                                                                         '= '
                                                                                                                                                                                                                                                                         'Color(Belgium) '
                                                                                                                                                                                                                                                                         'then '
                                                                                                                                                                                                                                                                         '568 '
                                                                                                                                                                                                                                                                         'else '
                                                                                                                                                                                                                                                                         '0)',
                                                                                                                                                                                                                                                              'relevant': True,
                                                                                                                                                                                                                                                              'status': 'UNIVERSAL',
                                                                                                                                                                                                                                                              'typ': 'Bool',
                                                                                                                                                                                                                                                              'value': True}}}
