
-- original ---------------------------------
// https://dmcommunity.org/challenge/challenge-may-2019/

vocabulary {
	type Country_t constructed from { Belgium, France, Luxembourg, Netherlands, Germany, Denmark } 
	type Color_t constructed from { Green, Red, Yellow, Orange } 
	Color(Country_t): Color_t
	Country_borders_Country(Country_t, Country_t)
}
theory {
	//Bordering countries can’t share colors
	!c1[Country_t]: !c2[Country_t]: Country_borders_Country(c1, c2) => Color(c1) ~= Color(c2).

}


structure {
	Country_borders_Country = {Belgium,France;Belgium,Luxembourg;Belgium,Netherlands;Belgium,Germany;Netherlands,Germany;Germany,France;Germany,Denmark;Germany,Luxembourg;France,Luxembourg;}
}

-- vocabulary -------------------------------

-- theory -----------------------------------
And(And(True,
        Not(Color(Belgium) == Color(France)),
        Not(Color(Belgium) == Color(Luxembourg)),
        Not(Color(Belgium) == Color(Netherlands)),
        Not(Color(Belgium) == Color(Germany)),
        True),
    Not(Color(France) == Color(Luxembourg)),
    True,
    Not(Color(Netherlands) == Color(Germany)),
    And(True,
        Not(Color(Germany) == Color(France)),
        Not(Color(Germany) == Color(Luxembourg)),
        True,
        True,
        Not(Color(Germany) == Color(Denmark))),
    True)

Or(Color(Belgium) == Green,
   Color(Belgium) == Red,
   Color(Belgium) == Yellow,
   Color(Belgium) == Orange)

Or(Color(France) == Green,
   Color(France) == Red,
   Color(France) == Yellow,
   Color(France) == Orange)

Or(Color(Luxembourg) == Green,
   Color(Luxembourg) == Red,
   Color(Luxembourg) == Yellow,
   Color(Luxembourg) == Orange)

Or(Color(Netherlands) == Green,
   Color(Netherlands) == Red,
   Color(Netherlands) == Yellow,
   Color(Netherlands) == Orange)

Or(Color(Germany) == Green,
   Color(Germany) == Red,
   Color(Germany) == Yellow,
   Color(Germany) == Orange)

Or(Color(Denmark) == Green,
   Color(Denmark) == Red,
   Color(Denmark) == Yellow,
   Color(Denmark) == Orange)

-- subtences ------------------------------------
∀c1[Country_t] : ∀c2[Country_t] : Country_borders_Country(c1,c2) ⇒ Color(c1) ≠ Color(c2)
Color(Belgium) = Green
Color(Belgium) = Red
Color(Belgium) = Yellow
Color(Belgium) = Orange
Color(France) = Green
Color(France) = Red
Color(France) = Yellow
Color(France) = Orange
Color(Luxembourg) = Green
Color(Luxembourg) = Red
Color(Luxembourg) = Yellow
Color(Luxembourg) = Orange
Color(Netherlands) = Green
Color(Netherlands) = Red
Color(Netherlands) = Yellow
Color(Netherlands) = Orange
Color(Germany) = Green
Color(Germany) = Red
Color(Germany) = Yellow
Color(Germany) = Orange
Color(Denmark) = Green
Color(Denmark) = Red
Color(Denmark) = Yellow
Color(Denmark) = Orange

-- GUILines ------------------------------------
Color(Belgium)
Color(France)
Color(Luxembourg)
Color(Netherlands)
Color(Germany)
Color(Denmark)
∀c1[Country_t] : ∀c2[Country_t] : Country_borders_Country(c1,c2) ⇒ Color(c1) ≠ Color(c2)
Color(Belgium) = Green
Color(Belgium) = Red
Color(Belgium) = Yellow
Color(Belgium) = Orange
Color(France) = Green
Color(France) = Red
Color(France) = Yellow
Color(France) = Orange
Color(Luxembourg) = Green
Color(Luxembourg) = Red
Color(Luxembourg) = Yellow
Color(Luxembourg) = Orange
Color(Netherlands) = Green
Color(Netherlands) = Red
Color(Netherlands) = Yellow
Color(Netherlands) = Orange
Color(Germany) = Green
Color(Germany) = Red
Color(Germany) = Yellow
Color(Germany) = Orange
Color(Denmark) = Green
Color(Denmark) = Red
Color(Denmark) = Yellow
Color(Denmark) = Orange

-- case -------------------------------------
Type:        
  
Definitions: 
  
Universals:  
  ∀c1[Country_t] : ∀c2[Country_t] : Country_borders_Country(c1,c2) ⇒ Color(c1) ≠ Color(c2)
Consequences:
  
Simplified:  
  ∀ : ((true) ∧ (~(Color(Belgium) = Color(France))) ∧ (~(Color(Belgium) = Color(Luxembourg))) ∧ (~(Color(Belgium) = Color(Netherlands))) ∧ (~(Color(Belgium) = Color(Germany))) ∧ (true)) ∧ (~(Color(France) = Color(Luxembourg))) ∧ (true) ∧ (~(Color(Netherlands) = Color(Germany))) ∧ ((true) ∧ (~(Color(Germany) = Color(France))) ∧ (~(Color(Germany) = Color(Luxembourg))) ∧ (true) ∧ (true) ∧ (~(Color(Germany) = Color(Denmark)))) ∧ (true)
  Color(Belgium) = Green ∨ Color(Belgium) = Red ∨ Color(Belgium) = Yellow ∨ Color(Belgium) = Orange
  Color(France) = Green ∨ Color(France) = Red ∨ Color(France) = Yellow ∨ Color(France) = Orange
  Color(Luxembourg) = Green ∨ Color(Luxembourg) = Red ∨ Color(Luxembourg) = Yellow ∨ Color(Luxembourg) = Orange
  Color(Netherlands) = Green ∨ Color(Netherlands) = Red ∨ Color(Netherlands) = Yellow ∨ Color(Netherlands) = Orange
  Color(Germany) = Green ∨ Color(Germany) = Red ∨ Color(Germany) = Yellow ∨ Color(Germany) = Orange
  Color(Denmark) = Green ∨ Color(Denmark) = Red ∨ Color(Denmark) = Yellow ∨ Color(Denmark) = Orange
Irrelevant:  
  
Co-constraints:
  


-- meta -------------------------------------
{'symbols': [{'idpname': 'Color', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'Color': {'Color(Belgium)': {'environmental': False,
                              'normal': True,
                              'reading': 'Color(Belgium)',
                              'relevant': True,
                              'status': 'UNKNOWN',
                              'typ': 'Color_t',
                              'value': '',
                              'values': ['Green', 'Red', 'Yellow', 'Orange']},
           'Color(Belgium) = Green': {'environmental': False,
                                      'normal': False,
                                      'reading': 'Color(Belgium) = Green',
                                      'relevant': True,
                                      'status': 'UNKNOWN',
                                      'typ': 'Bool'},
           'Color(Belgium) = Orange': {'environmental': False,
                                       'normal': False,
                                       'reading': 'Color(Belgium) = Orange',
                                       'relevant': True,
                                       'status': 'UNKNOWN',
                                       'typ': 'Bool'},
           'Color(Belgium) = Red': {'environmental': False,
                                    'normal': False,
                                    'reading': 'Color(Belgium) = Red',
                                    'relevant': True,
                                    'status': 'UNKNOWN',
                                    'typ': 'Bool'},
           'Color(Belgium) = Yellow': {'environmental': False,
                                       'normal': False,
                                       'reading': 'Color(Belgium) = Yellow',
                                       'relevant': True,
                                       'status': 'UNKNOWN',
                                       'typ': 'Bool'},
           'Color(Denmark)': {'environmental': False,
                              'normal': True,
                              'reading': 'Color(Denmark)',
                              'relevant': True,
                              'status': 'UNKNOWN',
                              'typ': 'Color_t',
                              'value': '',
                              'values': ['Green', 'Red', 'Yellow', 'Orange']},
           'Color(Denmark) = Green': {'environmental': False,
                                      'normal': False,
                                      'reading': 'Color(Denmark) = Green',
                                      'relevant': True,
                                      'status': 'UNKNOWN',
                                      'typ': 'Bool'},
           'Color(Denmark) = Orange': {'environmental': False,
                                       'normal': False,
                                       'reading': 'Color(Denmark) = Orange',
                                       'relevant': True,
                                       'status': 'UNKNOWN',
                                       'typ': 'Bool'},
           'Color(Denmark) = Red': {'environmental': False,
                                    'normal': False,
                                    'reading': 'Color(Denmark) = Red',
                                    'relevant': True,
                                    'status': 'UNKNOWN',
                                    'typ': 'Bool'},
           'Color(Denmark) = Yellow': {'environmental': False,
                                       'normal': False,
                                       'reading': 'Color(Denmark) = Yellow',
                                       'relevant': True,
                                       'status': 'UNKNOWN',
                                       'typ': 'Bool'},
           'Color(France)': {'environmental': False,
                             'normal': True,
                             'reading': 'Color(France)',
                             'relevant': True,
                             'status': 'UNKNOWN',
                             'typ': 'Color_t',
                             'value': '',
                             'values': ['Green', 'Red', 'Yellow', 'Orange']},
           'Color(France) = Green': {'environmental': False,
                                     'normal': False,
                                     'reading': 'Color(France) = Green',
                                     'relevant': True,
                                     'status': 'UNKNOWN',
                                     'typ': 'Bool'},
           'Color(France) = Orange': {'environmental': False,
                                      'normal': False,
                                      'reading': 'Color(France) = Orange',
                                      'relevant': True,
                                      'status': 'UNKNOWN',
                                      'typ': 'Bool'},
           'Color(France) = Red': {'environmental': False,
                                   'normal': False,
                                   'reading': 'Color(France) = Red',
                                   'relevant': True,
                                   'status': 'UNKNOWN',
                                   'typ': 'Bool'},
           'Color(France) = Yellow': {'environmental': False,
                                      'normal': False,
                                      'reading': 'Color(France) = Yellow',
                                      'relevant': True,
                                      'status': 'UNKNOWN',
                                      'typ': 'Bool'},
           'Color(Germany)': {'environmental': False,
                              'normal': True,
                              'reading': 'Color(Germany)',
                              'relevant': True,
                              'status': 'UNKNOWN',
                              'typ': 'Color_t',
                              'value': '',
                              'values': ['Green', 'Red', 'Yellow', 'Orange']},
           'Color(Germany) = Green': {'environmental': False,
                                      'normal': False,
                                      'reading': 'Color(Germany) = Green',
                                      'relevant': True,
                                      'status': 'UNKNOWN',
                                      'typ': 'Bool'},
           'Color(Germany) = Orange': {'environmental': False,
                                       'normal': False,
                                       'reading': 'Color(Germany) = Orange',
                                       'relevant': True,
                                       'status': 'UNKNOWN',
                                       'typ': 'Bool'},
           'Color(Germany) = Red': {'environmental': False,
                                    'normal': False,
                                    'reading': 'Color(Germany) = Red',
                                    'relevant': True,
                                    'status': 'UNKNOWN',
                                    'typ': 'Bool'},
           'Color(Germany) = Yellow': {'environmental': False,
                                       'normal': False,
                                       'reading': 'Color(Germany) = Yellow',
                                       'relevant': True,
                                       'status': 'UNKNOWN',
                                       'typ': 'Bool'},
           'Color(Luxembourg)': {'environmental': False,
                                 'normal': True,
                                 'reading': 'Color(Luxembourg)',
                                 'relevant': True,
                                 'status': 'UNKNOWN',
                                 'typ': 'Color_t',
                                 'value': '',
                                 'values': ['Green', 'Red', 'Yellow', 'Orange']},
           'Color(Luxembourg) = Green': {'environmental': False,
                                         'normal': False,
                                         'reading': 'Color(Luxembourg) = Green',
                                         'relevant': True,
                                         'status': 'UNKNOWN',
                                         'typ': 'Bool'},
           'Color(Luxembourg) = Orange': {'environmental': False,
                                          'normal': False,
                                          'reading': 'Color(Luxembourg) = Orange',
                                          'relevant': True,
                                          'status': 'UNKNOWN',
                                          'typ': 'Bool'},
           'Color(Luxembourg) = Red': {'environmental': False,
                                       'normal': False,
                                       'reading': 'Color(Luxembourg) = Red',
                                       'relevant': True,
                                       'status': 'UNKNOWN',
                                       'typ': 'Bool'},
           'Color(Luxembourg) = Yellow': {'environmental': False,
                                          'normal': False,
                                          'reading': 'Color(Luxembourg) = Yellow',
                                          'relevant': True,
                                          'status': 'UNKNOWN',
                                          'typ': 'Bool'},
           'Color(Netherlands)': {'environmental': False,
                                  'normal': True,
                                  'reading': 'Color(Netherlands)',
                                  'relevant': True,
                                  'status': 'UNKNOWN',
                                  'typ': 'Color_t',
                                  'value': '',
                                  'values': ['Green', 'Red', 'Yellow', 'Orange']},
           'Color(Netherlands) = Green': {'environmental': False,
                                          'normal': False,
                                          'reading': 'Color(Netherlands) = Green',
                                          'relevant': True,
                                          'status': 'UNKNOWN',
                                          'typ': 'Bool'},
           'Color(Netherlands) = Orange': {'environmental': False,
                                           'normal': False,
                                           'reading': 'Color(Netherlands) = Orange',
                                           'relevant': True,
                                           'status': 'UNKNOWN',
                                           'typ': 'Bool'},
           'Color(Netherlands) = Red': {'environmental': False,
                                        'normal': False,
                                        'reading': 'Color(Netherlands) = Red',
                                        'relevant': True,
                                        'status': 'UNKNOWN',
                                        'typ': 'Bool'},
           'Color(Netherlands) = Yellow': {'environmental': False,
                                           'normal': False,
                                           'reading': 'Color(Netherlands) = Yellow',
                                           'relevant': True,
                                           'status': 'UNKNOWN',
                                           'typ': 'Bool'},
           '__rank': 1,
           '∀c1[Country_t] : ∀c2[Country_t] : Country_borders_Country(c1,c2) ⇒ Color(c1) ≠ Color(c2)': {'environmental': False,
                                                                                                        'normal': False,
                                                                                                        'reading': '∀c1[Country_t] '
                                                                                                                   ': '
                                                                                                                   '∀c2[Country_t] '
                                                                                                                   ': '
                                                                                                                   'Country_borders_Country(c1,c2) '
                                                                                                                   '⇒ '
                                                                                                                   'Color(c1) '
                                                                                                                   '≠ '
                                                                                                                   'Color(c2)',
                                                                                                        'relevant': True,
                                                                                                        'status': 'UNIVERSAL',
                                                                                                        'typ': 'Bool',
                                                                                                        'value': True}}}
