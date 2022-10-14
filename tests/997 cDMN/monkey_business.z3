
-- original ---------------------------------
// https://dmcommunity.wordpress.com/challenge/challenge-nov-2015/

vocabulary {
	type Monkey_t := { Anna, Sam, Harriet, Mike }
	type Place_t := { Grass, Rock, Branch, Stream }
	type Fruit_t := { Apple, Pear, Banana, Orange }
	Place:(Monkey_t)→ Place_t
	Fruit:(Monkey_t)→ Fruit_t
}
theory {
	//Monkey Constraints
	!Monkey in Monkey_t: Monkey = Sam => Place(Monkey) = Grass & Fruit(Monkey) ~= Banana.

	!Monkey in Monkey_t: Place(Monkey) = Rock => Fruit(Monkey) = Apple.

	!Monkey in Monkey_t: Fruit(Monkey) = Pear => Place(Monkey) ~= Branch.

	!Monkey in Monkey_t: Monkey = Anna => Place(Monkey) = Stream & Fruit(Monkey) ~= Pear.

	!Monkey in Monkey_t: Monkey = Harriet => Place(Monkey) ~= Branch.

	!Monkey in Monkey_t: Monkey = Mike => Fruit(Monkey) ~= Orange.

	//Different Preferences
	!m1 in Monkey_t: !m2 in Monkey_t: m2 ~= m1 => Place(m1) ~= Place(m2) & Fruit(m1) ~= Fruit(m2).

}


structure {
}

-- meta -------------------------------------
{'manualPropagation': False,
 'manualRelevance': False,
 'optionalPropagation': False,
 'optionalRelevance': False,
 'symbols': [{'environmental': False,
              'idpname': 'Place',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Fruit',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'Fruit': {'Fruit(Anna)': {'environmental': False,
                           'is_assignment': True,
                           'normal': True,
                           'reading': 'Fruit(Anna)',
                           'relevant': False,
                           'status': 'UNIVERSAL',
                           'typ': 'Fruit_t',
                           'value': 'Orange',
                           'values': ['Orange']},
           'Fruit(Harriet)': {'environmental': False,
                              'is_assignment': True,
                              'normal': True,
                              'reading': 'Fruit(Harriet)',
                              'relevant': False,
                              'status': 'UNIVERSAL',
                              'typ': 'Fruit_t',
                              'value': 'Apple',
                              'values': ['Apple']},
           'Fruit(Mike)': {'environmental': False,
                           'is_assignment': True,
                           'normal': True,
                           'reading': 'Fruit(Mike)',
                           'relevant': False,
                           'status': 'UNIVERSAL',
                           'typ': 'Fruit_t',
                           'value': 'Banana',
                           'values': ['Banana']},
           'Fruit(Sam)': {'environmental': False,
                          'is_assignment': True,
                          'normal': True,
                          'reading': 'Fruit(Sam)',
                          'relevant': False,
                          'status': 'UNIVERSAL',
                          'typ': 'Fruit_t',
                          'value': 'Pear',
                          'values': ['Pear']},
           '∀ Monkey ∈ Monkey_t: Fruit(Monkey) = Pear ⇒ Place(Monkey) ≠ Branch': {'environmental': False,
                                                                                  'is_assignment': False,
                                                                                  'normal': False,
                                                                                  'reading': '∀ Monkey ∈ Monkey_t: '
                                                                                             'Fruit(Monkey) = Pear ⇒ '
                                                                                             'Place(Monkey) ≠ Branch',
                                                                                  'relevant': False,
                                                                                  'status': 'UNIVERSAL',
                                                                                  'typ': 'Bool',
                                                                                  'value': True},
           '∀ Monkey ∈ Monkey_t: Monkey = Mike ⇒ Fruit(Monkey) ≠ Orange': {'environmental': False,
                                                                           'is_assignment': False,
                                                                           'normal': False,
                                                                           'reading': '∀ Monkey ∈ Monkey_t: Monkey = '
                                                                                      'Mike ⇒ Fruit(Monkey) ≠ Orange',
                                                                           'relevant': False,
                                                                           'status': 'UNIVERSAL',
                                                                           'typ': 'Bool',
                                                                           'value': True}},
 'Place': {'Place(Anna)': {'environmental': False,
                           'is_assignment': True,
                           'normal': True,
                           'reading': 'Place(Anna)',
                           'relevant': False,
                           'status': 'UNIVERSAL',
                           'typ': 'Place_t',
                           'value': 'Stream',
                           'values': ['Stream']},
           'Place(Harriet)': {'environmental': False,
                              'is_assignment': True,
                              'normal': True,
                              'reading': 'Place(Harriet)',
                              'relevant': False,
                              'status': 'UNIVERSAL',
                              'typ': 'Place_t',
                              'value': 'Rock',
                              'values': ['Rock']},
           'Place(Mike)': {'environmental': False,
                           'is_assignment': True,
                           'normal': True,
                           'reading': 'Place(Mike)',
                           'relevant': False,
                           'status': 'UNIVERSAL',
                           'typ': 'Place_t',
                           'value': 'Branch',
                           'values': ['Branch']},
           'Place(Sam)': {'environmental': False,
                          'is_assignment': True,
                          'normal': True,
                          'reading': 'Place(Sam)',
                          'relevant': False,
                          'status': 'UNIVERSAL',
                          'typ': 'Place_t',
                          'value': 'Grass',
                          'values': ['Grass']},
           '∀ Monkey ∈ Monkey_t: Monkey = Anna ⇒ Place(Monkey) = Stream ∧ Fruit(Monkey) ≠ Pear': {'environmental': False,
                                                                                                  'is_assignment': False,
                                                                                                  'normal': False,
                                                                                                  'reading': '∀ Monkey '
                                                                                                             '∈ '
                                                                                                             'Monkey_t: '
                                                                                                             'Monkey = '
                                                                                                             'Anna ⇒ '
                                                                                                             'Place(Monkey) '
                                                                                                             '= Stream '
                                                                                                             '∧ '
                                                                                                             'Fruit(Monkey) '
                                                                                                             '≠ Pear',
                                                                                                  'relevant': False,
                                                                                                  'status': 'UNIVERSAL',
                                                                                                  'typ': 'Bool',
                                                                                                  'value': True},
           '∀ Monkey ∈ Monkey_t: Monkey = Harriet ⇒ Place(Monkey) ≠ Branch': {'environmental': False,
                                                                              'is_assignment': False,
                                                                              'normal': False,
                                                                              'reading': '∀ Monkey ∈ Monkey_t: Monkey '
                                                                                         '= Harriet ⇒ Place(Monkey) ≠ '
                                                                                         'Branch',
                                                                              'relevant': False,
                                                                              'status': 'UNIVERSAL',
                                                                              'typ': 'Bool',
                                                                              'value': True},
           '∀ Monkey ∈ Monkey_t: Monkey = Sam ⇒ Place(Monkey) = Grass ∧ Fruit(Monkey) ≠ Banana': {'environmental': False,
                                                                                                  'is_assignment': False,
                                                                                                  'normal': False,
                                                                                                  'reading': '∀ Monkey '
                                                                                                             '∈ '
                                                                                                             'Monkey_t: '
                                                                                                             'Monkey = '
                                                                                                             'Sam ⇒ '
                                                                                                             'Place(Monkey) '
                                                                                                             '= Grass '
                                                                                                             '∧ '
                                                                                                             'Fruit(Monkey) '
                                                                                                             '≠ Banana',
                                                                                                  'relevant': False,
                                                                                                  'status': 'UNIVERSAL',
                                                                                                  'typ': 'Bool',
                                                                                                  'value': True},
           '∀ Monkey ∈ Monkey_t: Place(Monkey) = Rock ⇒ Fruit(Monkey) = Apple': {'environmental': False,
                                                                                 'is_assignment': False,
                                                                                 'normal': False,
                                                                                 'reading': '∀ Monkey ∈ Monkey_t: '
                                                                                            'Place(Monkey) = Rock ⇒ '
                                                                                            'Fruit(Monkey) = Apple',
                                                                                 'relevant': False,
                                                                                 'status': 'UNIVERSAL',
                                                                                 'typ': 'Bool',
                                                                                 'value': True},
           '∀ m1 ∈ Monkey_t: ∀ m2 ∈ Monkey_t: m2 ≠ m1 ⇒ Place(m1) ≠ Place(m2) ∧ Fruit(m1) ≠ Fruit(m2)': {'environmental': False,
                                                                                                         'is_assignment': False,
                                                                                                         'normal': False,
                                                                                                         'reading': '∀ '
                                                                                                                    'm1 '
                                                                                                                    '∈ '
                                                                                                                    'Monkey_t: '
                                                                                                                    '∀ '
                                                                                                                    'm2 '
                                                                                                                    '∈ '
                                                                                                                    'Monkey_t: '
                                                                                                                    'm2 '
                                                                                                                    '≠ '
                                                                                                                    'm1 '
                                                                                                                    '⇒ '
                                                                                                                    'Place(m1) '
                                                                                                                    '≠ '
                                                                                                                    'Place(m2) '
                                                                                                                    '∧ '
                                                                                                                    'Fruit(m1) '
                                                                                                                    '≠ '
                                                                                                                    'Fruit(m2)',
                                                                                                         'relevant': False,
                                                                                                         'status': 'UNIVERSAL',
                                                                                                         'typ': 'Bool',
                                                                                                         'value': True}}}
