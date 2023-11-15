
-- original ---------------------------------


vocabulary {
	type Line_t := { First, Second, Third }
	type Digit_t := { 0..9 }
	type Syllables_t := { 0..7 }
	Allowed_Syllables: (Line_t)→ Syllables_t
	Syllables_for_Hundreds:(Digit_t)→ Syllables_t
	Syllables_for_Tens:(Digit_t)→ Syllables_t
	Syllables_for_Units:(Digit_t)→ Syllables_t
	Syllables:(Line_t)→ Syllables_t
	Solution:(Line_t)→ Int
	Hundreds:(Line_t)→ Digit_t
	Tens:(Line_t)→ Digit_t
	Units:(Line_t)→ Digit_t
}
theory {
	//Syllables for every Line
	{
		!Line in Line_t: Allowed_Syllables(Line) = 5 <- Line = First.
		!Line in Line_t: Allowed_Syllables(Line) = 6 <- Line = Second.
		!Line in Line_t: Allowed_Syllables(Line) = 3 <- Line = Third.
	}

	//Every line needs specific amount of syllables
	!Line in Line_t: true => Syllables(Line) = Allowed_Syllables(Line).

	//Calculate the lines
	!Line in Line_t: Solution(Line)  = sum(lambda : if Line = Line then Hundreds(Line) * 100 else 0)+sum(lambda : if Line = Line then Tens(Line) * 10 else 0)+sum(lambda : if Line = Line then Units(Line) else 0).
	//Solutions need to add up
	true => Solution(Third) = Solution(First) + Solution(Second).

	//Calculate syllables of line
	!Line in Line_t: Syllables(Line)  = sum(lambda : if Line = Line then Syllables_for_Hundreds(Hundreds(Line)) else 0)+sum(lambda : if Line = Line then Syllables_for_Tens(Tens(Line)) else 0)+sum(lambda : if Line = Line then Syllables_for_Units(Units(Line)) else 0).
}


structure {
	Syllables_for_Hundreds := {0→ 0, 1→ 3, 2→ 3, 3→ 3, 4→ 3, 5→ 3, 6→ 3, 7→ 4, 8 → 3, 9 → 3 } else 3.
	Syllables_for_Tens := {0 → 0, 1 → 7, 2 → 2, 3 → 2, 4 → 2, 5 → 2, 6 → 2, 7 → 3, 8 → 2, 9 → 2 } else 2.
	Syllables_for_Units := {0 → 0, 1 → 1, 2 → 1, 3 → 1, 4 → 1, 5 → 1, 6 → 1, 7 → 2, 8 → 1, 9 → 1 } else 1.
}

-- meta -------------------------------------
{'manualPropagation': False,
 'manualRelevance': False,
 'optionalPropagation': False,
 'optionalRelevance': False,
 'symbols': [{'environmental': False,
              'idpname': 'Syllables_for_Hundreds',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Syllables_for_Tens',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Syllables_for_Units',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Syllables',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Solution',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Hundreds',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Tens',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Units',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Allowed_Syllables',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'Allowed_Syllables': {'Allowed_Syllables(First)': {'environmental': False,
                                                    'is_assignment': True,
                                                    'normal': True,
                                                    'reading': 'Allowed_Syllables(First)',
                                                    'relevant': False,
                                                    'status': 'UNIVERSAL',
                                                    'typ': 'Int',
                                                    'value': '5',
                                                    'values': ['5']},
                       'Allowed_Syllables(Second)': {'environmental': False,
                                                     'is_assignment': True,
                                                     'normal': True,
                                                     'reading': 'Allowed_Syllables(Second)',
                                                     'relevant': False,
                                                     'status': 'UNIVERSAL',
                                                     'typ': 'Int',
                                                     'value': '6',
                                                     'values': ['6']},
                       'Allowed_Syllables(Third)': {'environmental': False,
                                                    'is_assignment': True,
                                                    'normal': True,
                                                    'reading': 'Allowed_Syllables(Third)',
                                                    'relevant': False,
                                                    'status': 'UNIVERSAL',
                                                    'typ': 'Int',
                                                    'value': '3',
                                                    'values': ['3']}},
 'Hundreds': {'Hundreds(First)': {'environmental': False,
                                  'is_assignment': True,
                                  'normal': True,
                                  'reading': 'Hundreds(First)',
                                  'relevant': True,
                                  'status': 'UNKNOWN',
                                  'typ': 'Int',
                                  'values': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']},
              'Hundreds(Second)': {'environmental': False,
                                   'is_assignment': True,
                                   'normal': True,
                                   'reading': 'Hundreds(Second)',
                                   'relevant': True,
                                   'status': 'UNKNOWN',
                                   'typ': 'Int',
                                   'values': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']},
              'Hundreds(Third)': {'environmental': False,
                                  'is_assignment': True,
                                  'normal': True,
                                  'reading': 'Hundreds(Third)',
                                  'relevant': True,
                                  'status': 'UNKNOWN',
                                  'typ': 'Int',
                                  'values': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']}},
 'Solution': {'Solution(First)': {'environmental': False,
                                  'is_assignment': True,
                                  'normal': True,
                                  'reading': 'Solution(First)',
                                  'relevant': True,
                                  'status': 'UNKNOWN',
                                  'typ': 'Int'},
              'Solution(Second)': {'environmental': False,
                                   'is_assignment': True,
                                   'normal': True,
                                   'reading': 'Solution(Second)',
                                   'relevant': True,
                                   'status': 'UNKNOWN',
                                   'typ': 'Int'},
              'Solution(Third)': {'environmental': False,
                                  'is_assignment': True,
                                  'normal': True,
                                  'reading': 'Solution(Third)',
                                  'relevant': True,
                                  'status': 'UNKNOWN',
                                  'typ': 'Int'},
              'Solution(Third) = Solution(First) + Solution(Second)': {'environmental': False,
                                                                       'is_assignment': False,
                                                                       'normal': False,
                                                                       'reading': 'Solution(Third) = Solution(First) + '
                                                                                  'Solution(Second)',
                                                                       'relevant': False,
                                                                       'status': 'UNIVERSAL',
                                                                       'typ': 'Bool',
                                                                       'value': True},
              '∀ Line ∈ Line_t: Solution(Line) = sum(lambda  : if Line = Line then Hundreds(Line) ⨯ 100 else 0) + sum(lambda  : if Line = Line then Tens(Line) ⨯ 10 else 0) + sum(lambda  : if Line = Line then Units(Line) else 0)': {'environmental': False,
                                                                                                                                                                                                                                       'is_assignment': False,
                                                                                                                                                                                                                                       'normal': False,
                                                                                                                                                                                                                                       'reading': '∀ '
                                                                                                                                                                                                                                                  'Line '
                                                                                                                                                                                                                                                  '∈ '
                                                                                                                                                                                                                                                  'Line_t: '
                                                                                                                                                                                                                                                  'Solution(Line) '
                                                                                                                                                                                                                                                  '= '
                                                                                                                                                                                                                                                  'sum(lambda  '
                                                                                                                                                                                                                                                  ': '
                                                                                                                                                                                                                                                  'if '
                                                                                                                                                                                                                                                  'Line '
                                                                                                                                                                                                                                                  '= '
                                                                                                                                                                                                                                                  'Line '
                                                                                                                                                                                                                                                  'then '
                                                                                                                                                                                                                                                  'Hundreds(Line) '
                                                                                                                                                                                                                                                  '⨯ '
                                                                                                                                                                                                                                                  '100 '
                                                                                                                                                                                                                                                  'else '
                                                                                                                                                                                                                                                  '0) '
                                                                                                                                                                                                                                                  '+ '
                                                                                                                                                                                                                                                  'sum(lambda  '
                                                                                                                                                                                                                                                  ': '
                                                                                                                                                                                                                                                  'if '
                                                                                                                                                                                                                                                  'Line '
                                                                                                                                                                                                                                                  '= '
                                                                                                                                                                                                                                                  'Line '
                                                                                                                                                                                                                                                  'then '
                                                                                                                                                                                                                                                  'Tens(Line) '
                                                                                                                                                                                                                                                  '⨯ '
                                                                                                                                                                                                                                                  '10 '
                                                                                                                                                                                                                                                  'else '
                                                                                                                                                                                                                                                  '0) '
                                                                                                                                                                                                                                                  '+ '
                                                                                                                                                                                                                                                  'sum(lambda  '
                                                                                                                                                                                                                                                  ': '
                                                                                                                                                                                                                                                  'if '
                                                                                                                                                                                                                                                  'Line '
                                                                                                                                                                                                                                                  '= '
                                                                                                                                                                                                                                                  'Line '
                                                                                                                                                                                                                                                  'then '
                                                                                                                                                                                                                                                  'Units(Line) '
                                                                                                                                                                                                                                                  'else '
                                                                                                                                                                                                                                                  '0)',
                                                                                                                                                                                                                                       'relevant': False,
                                                                                                                                                                                                                                       'status': 'UNIVERSAL',
                                                                                                                                                                                                                                       'typ': 'Bool',
                                                                                                                                                                                                                                       'value': True}},
 'Syllables': {'Syllables(First)': {'environmental': False,
                                    'is_assignment': True,
                                    'normal': True,
                                    'reading': 'Syllables(First)',
                                    'relevant': False,
                                    'status': 'UNIVERSAL',
                                    'typ': 'Int',
                                    'value': '5',
                                    'values': ['5']},
               'Syllables(Second)': {'environmental': False,
                                     'is_assignment': True,
                                     'normal': True,
                                     'reading': 'Syllables(Second)',
                                     'relevant': False,
                                     'status': 'UNIVERSAL',
                                     'typ': 'Int',
                                     'value': '6',
                                     'values': ['6']},
               'Syllables(Third)': {'environmental': False,
                                    'is_assignment': True,
                                    'normal': True,
                                    'reading': 'Syllables(Third)',
                                    'relevant': False,
                                    'status': 'UNIVERSAL',
                                    'typ': 'Int',
                                    'value': '3',
                                    'values': ['3']},
               '∀ Line ∈ Line_t: Syllables(Line) = sum(lambda  : if Line = Line then Syllables_for_Hundreds(Hundreds(Line)) else 0) + sum(lambda  : if Line = Line then Syllables_for_Tens(Tens(Line)) else 0) + sum(lambda  : if Line = Line then Syllables_for_Units(Units(Line)) else 0)': {'environmental': False,
                                                                                                                                                                                                                                                                                               'is_assignment': False,
                                                                                                                                                                                                                                                                                               'normal': False,
                                                                                                                                                                                                                                                                                               'reading': '∀ '
                                                                                                                                                                                                                                                                                                          'Line '
                                                                                                                                                                                                                                                                                                          '∈ '
                                                                                                                                                                                                                                                                                                          'Line_t: '
                                                                                                                                                                                                                                                                                                          'Syllables(Line) '
                                                                                                                                                                                                                                                                                                          '= '
                                                                                                                                                                                                                                                                                                          'sum(lambda  '
                                                                                                                                                                                                                                                                                                          ': '
                                                                                                                                                                                                                                                                                                          'if '
                                                                                                                                                                                                                                                                                                          'Line '
                                                                                                                                                                                                                                                                                                          '= '
                                                                                                                                                                                                                                                                                                          'Line '
                                                                                                                                                                                                                                                                                                          'then '
                                                                                                                                                                                                                                                                                                          'Syllables_for_Hundreds(Hundreds(Line)) '
                                                                                                                                                                                                                                                                                                          'else '
                                                                                                                                                                                                                                                                                                          '0) '
                                                                                                                                                                                                                                                                                                          '+ '
                                                                                                                                                                                                                                                                                                          'sum(lambda  '
                                                                                                                                                                                                                                                                                                          ': '
                                                                                                                                                                                                                                                                                                          'if '
                                                                                                                                                                                                                                                                                                          'Line '
                                                                                                                                                                                                                                                                                                          '= '
                                                                                                                                                                                                                                                                                                          'Line '
                                                                                                                                                                                                                                                                                                          'then '
                                                                                                                                                                                                                                                                                                          'Syllables_for_Tens(Tens(Line)) '
                                                                                                                                                                                                                                                                                                          'else '
                                                                                                                                                                                                                                                                                                          '0) '
                                                                                                                                                                                                                                                                                                          '+ '
                                                                                                                                                                                                                                                                                                          'sum(lambda  '
                                                                                                                                                                                                                                                                                                          ': '
                                                                                                                                                                                                                                                                                                          'if '
                                                                                                                                                                                                                                                                                                          'Line '
                                                                                                                                                                                                                                                                                                          '= '
                                                                                                                                                                                                                                                                                                          'Line '
                                                                                                                                                                                                                                                                                                          'then '
                                                                                                                                                                                                                                                                                                          'Syllables_for_Units(Units(Line)) '
                                                                                                                                                                                                                                                                                                          'else '
                                                                                                                                                                                                                                                                                                          '0)',
                                                                                                                                                                                                                                                                                               'relevant': False,
                                                                                                                                                                                                                                                                                               'status': 'UNIVERSAL',
                                                                                                                                                                                                                                                                                               'typ': 'Bool',
                                                                                                                                                                                                                                                                                               'value': True},
               '∀ Line ∈ Line_t: true ⇒ Syllables(Line) = Allowed_Syllables(Line)': {'environmental': False,
                                                                                     'is_assignment': False,
                                                                                     'normal': False,
                                                                                     'reading': '∀ Line ∈ Line_t: true '
                                                                                                '⇒ Syllables(Line) = '
                                                                                                'Allowed_Syllables(Line)',
                                                                                     'relevant': False,
                                                                                     'status': 'UNIVERSAL',
                                                                                     'typ': 'Bool',
                                                                                     'value': True}},
 'Syllables_for_Hundreds': {},
 'Syllables_for_Tens': {},
 'Syllables_for_Units': {},
 'Tens': {'Tens(First)': {'environmental': False,
                          'is_assignment': True,
                          'normal': True,
                          'reading': 'Tens(First)',
                          'relevant': True,
                          'status': 'UNKNOWN',
                          'typ': 'Int',
                          'values': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']},
          'Tens(Second)': {'environmental': False,
                           'is_assignment': True,
                           'normal': True,
                           'reading': 'Tens(Second)',
                           'relevant': True,
                           'status': 'UNKNOWN',
                           'typ': 'Int',
                           'values': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']},
          'Tens(Third)': {'environmental': False,
                          'is_assignment': True,
                          'normal': True,
                          'reading': 'Tens(Third)',
                          'relevant': False,
                          'status': 'UNIVERSAL',
                          'typ': 'Int',
                          'value': '0',
                          'values': ['0']}},
 'Units': {'Units(First)': {'environmental': False,
                            'is_assignment': True,
                            'normal': True,
                            'reading': 'Units(First)',
                            'relevant': True,
                            'status': 'UNKNOWN',
                            'typ': 'Int',
                            'values': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']},
           'Units(Second)': {'environmental': False,
                             'is_assignment': True,
                             'normal': True,
                             'reading': 'Units(Second)',
                             'relevant': True,
                             'status': 'UNKNOWN',
                             'typ': 'Int',
                             'values': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']},
           'Units(Third)': {'environmental': False,
                            'is_assignment': True,
                            'normal': True,
                            'reading': 'Units(Third)',
                            'relevant': False,
                            'status': 'UNIVERSAL',
                            'typ': 'Int',
                            'value': '0',
                            'values': ['0']}}}
