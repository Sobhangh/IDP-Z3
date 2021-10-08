
-- original ---------------------------------
// https://dmcommunity.wordpress.com/challenge/make-a-good-burger/

vocabulary {
	type Item_t := {  Beef_Patty, Bun, Cheese, Onions, Pickles, Lettuce, Ketchup, Tomato }
	type Nat_t := { 0..10000 }
	Sodium:(Item_t)→ Nat_t
	Fat:(Item_t)→ Nat_t
	Calories:(Item_t)→ Nat_t
	Cost:(Item_t)→ Nat_t
	Number:(Item_t)→ Nat_t
	Total_Sodium: ()→Nat_t
	Total_Fat: ()→Nat_t
	Total_Calories: ()→Nat_t
	Total_Cost: ()→Nat_t
}
theory {
	//NumberConstraint
	!Item in Item_t: true => 01 =< Number(Item) & Number(Item) =< 05.

	!Item in Item_t: Item = Lettuce => Number(Item) = Number(Ketchup).

	!Item in Item_t: Item = Pickles => Number(Item) = Number(Tomato).

	//Determine Nutrition
	Total_Sodium() = sum{ Item in Item_t : true: Number(Item) * Sodium(Item) }.
	Total_Fat() = sum{ Item in Item_t : true: Number(Item) * Fat(Item) }.
	Total_Calories() = sum{ Item in Item_t : true: Number(Item) * Calories(Item) }.
	Total_Cost() = sum{ Item in Item_t : true: Number(Item) * Cost(Item) }.
	//Nutrition Constraints
	true => Total_Sodium() < 3000 & Total_Fat() < 150 & Total_Calories() < 3000.

}


structure {
	Sodium := {Beef_Patty → 50, Bun → 330, Cheese → 310, Onions → 1, Pickles → 260, Lettuce → 3, Ketchup → 160, Tomato → 3 } else 3
	Fat := {Beef_Patty → 17, Bun → 9, Cheese → 6, Onions → 2, Pickles → 0, Lettuce → 0, Ketchup → 0, Tomato → 0 } else 0
	Calories := {Beef_Patty → 220, Bun → 260, Cheese → 70, Onions → 10, Pickles → 5, Lettuce → 4, Ketchup → 20, Tomato → 9 } else 9
	Cost := {Beef_Patty → 25, Bun → 15, Cheese → 10, Onions → 9, Pickles → 3, Lettuce → 4, Ketchup → 2, Tomato → 4 } else 4
}

-- meta -------------------------------------
{'manualPropagation': False,
 'manualRelevance': False,
 'optionalPropagation': False,
 'optionalRelevance': False,
 'symbols': [{'environmental': False,
              'idpname': 'Sodium',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Fat',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Calories',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Cost',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Number',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Total_Sodium',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Total_Fat',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Total_Calories',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Total_Cost',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'active': '{}', 'env_dec': False},
 'Calories': {},
 'Cost': {},
 'Fat': {},
 'Number': {'Number(Beef_Patty)': {'environmental': False,
                                   'is_assignment': True,
                                   'normal': True,
                                   'reading': 'Number(Beef_Patty)',
                                   'relevant': True,
                                   'status': 'UNKNOWN',
                                   'typ': 'Int',
                                   'value': '',
                                   'values': []},
            'Number(Bun)': {'environmental': False,
                            'is_assignment': True,
                            'normal': True,
                            'reading': 'Number(Bun)',
                            'relevant': True,
                            'status': 'UNKNOWN',
                            'typ': 'Int',
                            'value': '',
                            'values': []},
            'Number(Cheese)': {'environmental': False,
                               'is_assignment': True,
                               'normal': True,
                               'reading': 'Number(Cheese)',
                               'relevant': True,
                               'status': 'UNKNOWN',
                               'typ': 'Int',
                               'value': '',
                               'values': []},
            'Number(Ketchup)': {'environmental': False,
                                'is_assignment': True,
                                'normal': True,
                                'reading': 'Number(Ketchup)',
                                'relevant': True,
                                'status': 'UNKNOWN',
                                'typ': 'Int',
                                'value': '',
                                'values': []},
            'Number(Lettuce)': {'environmental': False,
                                'is_assignment': True,
                                'normal': True,
                                'reading': 'Number(Lettuce)',
                                'relevant': True,
                                'status': 'UNKNOWN',
                                'typ': 'Int',
                                'value': '',
                                'values': []},
            'Number(Onions)': {'environmental': False,
                               'is_assignment': True,
                               'normal': True,
                               'reading': 'Number(Onions)',
                               'relevant': True,
                               'status': 'UNKNOWN',
                               'typ': 'Int',
                               'value': '',
                               'values': []},
            'Number(Pickles)': {'environmental': False,
                                'is_assignment': True,
                                'normal': True,
                                'reading': 'Number(Pickles)',
                                'relevant': True,
                                'status': 'UNKNOWN',
                                'typ': 'Int',
                                'value': '',
                                'values': []},
            'Number(Tomato)': {'environmental': False,
                               'is_assignment': True,
                               'normal': True,
                               'reading': 'Number(Tomato)',
                               'relevant': True,
                               'status': 'UNKNOWN',
                               'typ': 'Int',
                               'value': '',
                               'values': []},
            '__rank': 9999,
            '∀Item ∈ Item_t : Item = Lettuce ⇒ Number(Item) = Number(Ketchup)': {'environmental': False,
                                                                                 'is_assignment': False,
                                                                                 'normal': False,
                                                                                 'reading': '∀Item ∈ Item_t : Item = '
                                                                                            'Lettuce ⇒ Number(Item) = '
                                                                                            'Number(Ketchup)',
                                                                                 'relevant': False,
                                                                                 'status': 'UNIVERSAL',
                                                                                 'typ': 'Bool',
                                                                                 'value': True},
            '∀Item ∈ Item_t : Item = Pickles ⇒ Number(Item) = Number(Tomato)': {'environmental': False,
                                                                                'is_assignment': False,
                                                                                'normal': False,
                                                                                'reading': '∀Item ∈ Item_t : Item = '
                                                                                           'Pickles ⇒ Number(Item) = '
                                                                                           'Number(Tomato)',
                                                                                'relevant': False,
                                                                                'status': 'UNIVERSAL',
                                                                                'typ': 'Bool',
                                                                                'value': True},
            '∀Item ∈ Item_t : true ⇒ 01 ≤ Number(Item) ∧ Number(Item) ≤ 05': {'environmental': False,
                                                                              'is_assignment': False,
                                                                              'normal': False,
                                                                              'reading': '∀Item ∈ Item_t : true ⇒ 01 ≤ '
                                                                                         'Number(Item) ∧ Number(Item) '
                                                                                         '≤ 05',
                                                                              'relevant': False,
                                                                              'status': 'UNIVERSAL',
                                                                              'typ': 'Bool',
                                                                              'value': True}},
 'Sodium': {},
 'Total_Calories': {'Total_Calories()': {'environmental': False,
                                         'is_assignment': True,
                                         'normal': True,
                                         'reading': 'Total_Calories',
                                         'relevant': True,
                                         'status': 'UNKNOWN',
                                         'typ': 'Int',
                                         'value': '',
                                         'values': []},
                    'Total_Calories() < 3000': {'environmental': False,
                                                'is_assignment': False,
                                                'normal': False,
                                                'reading': 'Total_Calories < 3000',
                                                'relevant': True,
                                                'status': 'UNIVERSAL',
                                                'typ': 'Bool',
                                                'value': True},
                    'Total_Calories() = sum{Item ∈ Item_t : true : Number(Item) ⨯ Calories(Item)}': {'environmental': False,
                                                                                                     'is_assignment': False,
                                                                                                     'normal': False,
                                                                                                     'reading': 'Total_Calories '
                                                                                                                '= '
                                                                                                                'sum{Item '
                                                                                                                '∈ '
                                                                                                                'Item_t '
                                                                                                                ': '
                                                                                                                'true '
                                                                                                                ': '
                                                                                                                'Number(Item) '
                                                                                                                '⨯ '
                                                                                                                'Calories(Item)}',
                                                                                                     'relevant': True,
                                                                                                     'status': 'UNIVERSAL',
                                                                                                     'typ': 'Bool',
                                                                                                     'value': True},
                    '__rank': 9999},
 'Total_Cost': {'Total_Cost()': {'environmental': False,
                                 'is_assignment': True,
                                 'normal': True,
                                 'reading': 'Total_Cost',
                                 'relevant': True,
                                 'status': 'UNKNOWN',
                                 'typ': 'Int',
                                 'value': '',
                                 'values': []},
                'Total_Cost() = sum{Item ∈ Item_t : true : Number(Item) ⨯ Cost(Item)}': {'environmental': False,
                                                                                         'is_assignment': False,
                                                                                         'normal': False,
                                                                                         'reading': 'Total_Cost = '
                                                                                                    'sum{Item ∈ Item_t '
                                                                                                    ': true : '
                                                                                                    'Number(Item) ⨯ '
                                                                                                    'Cost(Item)}',
                                                                                         'relevant': True,
                                                                                         'status': 'UNIVERSAL',
                                                                                         'typ': 'Bool',
                                                                                         'value': True},
                '__rank': 9999},
 'Total_Fat': {'Total_Fat()': {'environmental': False,
                               'is_assignment': True,
                               'normal': True,
                               'reading': 'Total_Fat',
                               'relevant': True,
                               'status': 'UNKNOWN',
                               'typ': 'Int',
                               'value': '',
                               'values': []},
               'Total_Fat() < 150': {'environmental': False,
                                     'is_assignment': False,
                                     'normal': False,
                                     'reading': 'Total_Fat < 150',
                                     'relevant': True,
                                     'status': 'UNIVERSAL',
                                     'typ': 'Bool',
                                     'value': True},
               'Total_Fat() = sum{Item ∈ Item_t : true : Number(Item) ⨯ Fat(Item)}': {'environmental': False,
                                                                                      'is_assignment': False,
                                                                                      'normal': False,
                                                                                      'reading': 'Total_Fat = sum{Item '
                                                                                                 '∈ Item_t : true : '
                                                                                                 'Number(Item) ⨯ '
                                                                                                 'Fat(Item)}',
                                                                                      'relevant': True,
                                                                                      'status': 'UNIVERSAL',
                                                                                      'typ': 'Bool',
                                                                                      'value': True},
               '__rank': 9999},
 'Total_Sodium': {'Total_Sodium()': {'environmental': False,
                                     'is_assignment': True,
                                     'normal': True,
                                     'reading': 'Total_Sodium',
                                     'relevant': True,
                                     'status': 'UNKNOWN',
                                     'typ': 'Int',
                                     'value': '',
                                     'values': []},
                  'Total_Sodium() < 3000': {'environmental': False,
                                            'is_assignment': False,
                                            'normal': False,
                                            'reading': 'Total_Sodium < 3000',
                                            'relevant': True,
                                            'status': 'UNIVERSAL',
                                            'typ': 'Bool',
                                            'value': True},
                  'Total_Sodium() = sum{Item ∈ Item_t : true : Number(Item) ⨯ Sodium(Item)}': {'environmental': False,
                                                                                               'is_assignment': False,
                                                                                               'normal': False,
                                                                                               'reading': 'Total_Sodium '
                                                                                                          '= sum{Item '
                                                                                                          '∈ Item_t : '
                                                                                                          'true : '
                                                                                                          'Number(Item) '
                                                                                                          '⨯ '
                                                                                                          'Sodium(Item)}',
                                                                                               'relevant': True,
                                                                                               'status': 'UNIVERSAL',
                                                                                               'typ': 'Bool',
                                                                                               'value': True},
                  '__rank': 9999}}
