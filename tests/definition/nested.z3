
-- original ---------------------------------
vocabulary {
    type num constructed from { Piet, Jan}
    same(num) : num
    negated(num) : num
} 

theory {
    { !x[num]: same(x) = x. }
    { negated(Piet) = Jan.  negated(Jan) = Piet. }
    same(Piet)= Piet.
    same(same(Piet))= negated(negated(Piet)).

}
 
view expanded
-- vocabulary -------------------------------

-- theory -----------------------------------
same(Piet) == Piet

same(same(Piet)) == negated(negated(Piet))

Or(same(Piet) == Piet, same(Piet) == Jan)

Or(same(Jan) == Piet, same(Jan) == Jan)

Or(negated(Piet) == Piet, negated(Piet) == Jan)

Or(negated(Jan) == Piet, negated(Jan) == Jan)

And(same(Piet) == Piet,
    Not(same(Piet) == Jan),
    Not(same(Jan) == Piet),
    same(Jan) == Jan)

And(Not(negated(Piet) == Piet),
    negated(Piet) == Jan,
    negated(Jan) == Piet,
    Not(negated(Jan) == Jan))

-- subtences ------------------------------------
same(Piet) = Piet
negated(Piet) = Jan
negated(Piet) = Piet
same(Piet) = Jan
same(Jan) = Piet
same(Jan) = Jan
negated(Jan) = Piet
negated(Jan) = Jan

-- GUILines ------------------------------------
same(Piet)
same(Jan)
negated(Piet)
negated(Jan)
same(Piet) = Piet
negated(Piet) = Jan
negated(Piet) = Piet
same(Piet) = Jan
same(Jan) = Piet
same(Jan) = Jan
negated(Jan) = Piet
negated(Jan) = Jan

-- case -------------------------------------
Type:        
  
Definitions: 
  Rule:∀['$same!0$', '$same$'][]: same($same!0$,$same$) ⇔($same$ = $same!0$)
  Rule:∀['$negated!0$', '$negated$'][]: negated($negated!0$,$negated$) ⇔(($negated$ = Jan) ∧ (($negated!0$ = Piet))) ∨ (($negated$ = Piet) ∧ (($negated!0$ = Jan)))
Universals:  
  same(Piet) = Piet
Consequences:
  negated(Piet) = Jan <= Z3 proof
  ~negated(Piet) = Piet <= {'negated(Piet)'}
  ~same(Piet) = Jan <= {'same(Piet)'}
  ~same(Jan) = Piet <= Z3 proof
  same(Jan) = Jan <= {'(same(Jan) = Piet) ∨ (same(Jan) = Jan)', 'same(Jan) = Piet'}
  negated(Jan) = Piet <= Z3 proof
  ~negated(Jan) = Jan <= {'negated(Jan)'}
  same(Piet) = Piet
  same(Jan) = Jan
  negated(Piet) = Jan
  negated(Jan) = Piet
Simplified:  
  
Irrelevant:  
  ~same(Piet) = Jan <= {'same(Piet)'}


-- meta -------------------------------------
{'symbols': [{'idpname': 'same', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'},
             {'idpname': 'negated', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'negated': {'negated(Jan)': {'environmental': False,
                              'normal': True,
                              'reading': 'negated(Jan)',
                              'relevant': True,
                              'status': 'CONSEQUENCE',
                              'typ': 'num',
                              'value': 'Piet',
                              'values': ['Piet', 'Jan']},
             'negated(Jan) = Jan': {'environmental': False,
                                    'normal': False,
                                    'reading': 'negated(Jan) = Jan',
                                    'relevant': True,
                                    'status': 'CONSEQUENCE',
                                    'typ': 'Bool',
                                    'value': False},
             'negated(Jan) = Piet': {'environmental': False,
                                     'normal': False,
                                     'reading': 'negated(Jan) = Piet',
                                     'relevant': True,
                                     'status': 'CONSEQUENCE',
                                     'typ': 'Bool',
                                     'value': True},
             'negated(Piet)': {'environmental': False,
                               'normal': True,
                               'reading': 'negated(Piet)',
                               'relevant': True,
                               'status': 'CONSEQUENCE',
                               'typ': 'num',
                               'value': 'Jan',
                               'values': ['Piet', 'Jan']},
             'negated(Piet) = Jan': {'environmental': False,
                                     'normal': False,
                                     'reading': 'negated(Piet) = Jan',
                                     'relevant': True,
                                     'status': 'CONSEQUENCE',
                                     'typ': 'Bool',
                                     'value': True},
             'negated(Piet) = Piet': {'environmental': False,
                                      'normal': False,
                                      'reading': 'negated(Piet) = Piet',
                                      'relevant': True,
                                      'status': 'CONSEQUENCE',
                                      'typ': 'Bool',
                                      'value': False}},
 'same': {'same(Jan)': {'environmental': False,
                        'normal': True,
                        'reading': 'same(Jan)',
                        'relevant': True,
                        'status': 'CONSEQUENCE',
                        'typ': 'num',
                        'value': 'Jan',
                        'values': ['Piet', 'Jan']},
          'same(Jan) = Jan': {'environmental': False,
                              'normal': False,
                              'reading': 'same(Jan) = Jan',
                              'relevant': True,
                              'status': 'CONSEQUENCE',
                              'typ': 'Bool',
                              'value': True},
          'same(Jan) = Piet': {'environmental': False,
                               'normal': False,
                               'reading': 'same(Jan) = Piet',
                               'relevant': True,
                               'status': 'CONSEQUENCE',
                               'typ': 'Bool',
                               'value': False},
          'same(Piet)': {'environmental': False,
                         'normal': True,
                         'reading': 'same(Piet)',
                         'relevant': True,
                         'status': 'CONSEQUENCE',
                         'typ': 'num',
                         'value': 'Piet',
                         'values': ['Piet', 'Jan']},
          'same(Piet) = Jan': {'environmental': False,
                               'normal': False,
                               'reading': 'same(Piet) = Jan',
                               'relevant': False,
                               'status': 'CONSEQUENCE',
                               'typ': 'Bool',
                               'value': False},
          'same(Piet) = Piet': {'environmental': False,
                                'normal': False,
                                'reading': 'same(Piet) = Piet',
                                'relevant': True,
                                'status': 'UNIVERSAL',
                                'typ': 'Bool',
                                'value': True}}}
