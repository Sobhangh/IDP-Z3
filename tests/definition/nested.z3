
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

And(same(Piet) == Piet,
    Not(same(Jan) == Piet),
    Not(same(Piet) == Jan),
    same(Jan) == Jan)

And(Not(negated(Piet) == Piet),
    negated(Jan) == Piet,
    negated(Piet) == Jan,
    Not(negated(Jan) == Jan))

-- subtences ------------------------------------
same(Piet) = Piet
same(same(Piet)) = negated(negated(Piet))

-- GUILines ------------------------------------
same(Piet)
same(Jan)
negated(Piet)
negated(Jan)
same(Piet) = Piet
same(same(Piet)) = negated(negated(Piet))

-- case -------------------------------------
Type:        
  
Definitions: 
  Rule:∀['$same!0$', '$same$'][]: same($same!0$,$same$) ⇔($same$ = $same!0$)
  Rule:∀['$negated!0$', '$negated$'][]: negated($negated!0$,$negated$) ⇔(($negated$ = Jan) ∧ ($negated!0$ = Piet)) ∨ (($negated$ = Piet) ∧ ($negated!0$ = Jan))
Universals:  
  same(Piet) = Piet
  same(same(Piet)) = negated(negated(Piet))
Consequences:
  same(Piet) = Piet
  same(Jan) = Jan
  negated(Piet) = Jan
  negated(Jan) = Piet
Simplified:  
  
Irrelevant:  
  


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
             'negated(Piet)': {'environmental': False,
                               'normal': True,
                               'reading': 'negated(Piet)',
                               'relevant': True,
                               'status': 'CONSEQUENCE',
                               'typ': 'num',
                               'value': 'Jan',
                               'values': ['Piet', 'Jan']}},
 'same': {'same(Jan)': {'environmental': False,
                        'normal': True,
                        'reading': 'same(Jan)',
                        'relevant': True,
                        'status': 'CONSEQUENCE',
                        'typ': 'num',
                        'value': 'Jan',
                        'values': ['Piet', 'Jan']},
          'same(Piet)': {'environmental': False,
                         'normal': True,
                         'reading': 'same(Piet)',
                         'relevant': True,
                         'status': 'CONSEQUENCE',
                         'typ': 'num',
                         'value': 'Piet',
                         'values': ['Piet', 'Jan']},
          'same(Piet) = Piet': {'environmental': False,
                                'normal': False,
                                'reading': 'same(Piet) = Piet',
                                'relevant': True,
                                'status': 'UNIVERSAL',
                                'typ': 'Bool',
                                'value': True},
          'same(same(Piet)) = negated(negated(Piet))': {'environmental': False,
                                                        'normal': False,
                                                        'reading': 'same(same(Piet)) = negated(negated(Piet))',
                                                        'relevant': True,
                                                        'status': 'UNIVERSAL',
                                                        'typ': 'Bool',
                                                        'value': True}}}
