
-- original ---------------------------------
vocabulary {
    type num constructed from { Piet, Jan}
    same(num) : num
    negated(num) : num
} 

theory {
    { !x[num]: same(x) = x. }
    { !x[num]: negated(x) = (0-x). }
    same(Piet)= Piet.
    same(same(Piet))= negated(negated(Piet)).

}
 
view expanded
-- vocabulary -------------------------------

-- theory -----------------------------------
same(Piet) == Piet

same(same(Piet)) == negated(negated(Piet))

And((same(Piet) == Piet) == True,
    (same(Jan) == Piet) == False,
    (same(Piet) == Jan) == False,
    (same(Jan) == Jan) == True)

And((negated(Piet) == Piet) == True,
    (negated(Jan) == Piet) == False,
    (negated(Piet) == Jan) == False,
    (negated(Jan) == Jan) == True)

-- atoms ------------------------------------
same(Piet)
same(Jan)
negated(Piet)
negated(Jan)
same(Piet) = Piet
same(same(Piet)) = negated(negated(Piet))

-- case -------------------------------------
Type:        
  
Definitions: 
  Rule:∀['$same$0', '$same$'][]: same($same$0,$same$) ⇔((($same$0 = Piet) ∧ ($same$ = Piet)) ∨ (($same$0 = Jan) ∧ ($same$ = Jan)))
  Rule:∀['$negated$0', '$negated$'][]: negated($negated$0,$negated$) ⇔((($negated$0 = Piet) ∧ ($negated$ = Piet)) ∨ (($negated$0 = Jan) ∧ ($negated$ = Jan)))
Universals:  
  same(Piet) = Piet
  same(same(Piet)) = negated(negated(Piet))
Consequences:
  same(Piet) = Piet
  same(Jan) = Jan
  negated(Piet) = Piet
  negated(Jan) = Jan
Simplified:  
  
Irrelevant:  
  


-- propagation ------------------------------
{' Global': {'env_dec': False},
 'negated': {'negated(Jan)': {'environmental': False,
                              'normal': True,
                              'reading': 'negated(Jan)',
                              'relevant': True,
                              'status': 'CONSEQUENCE',
                              'typ': 'num',
                              'value': 'Jan',
                              'values': ['Piet', 'Jan']},
             'negated(Piet)': {'environmental': False,
                               'normal': True,
                               'reading': 'negated(Piet)',
                               'relevant': True,
                               'status': 'CONSEQUENCE',
                               'typ': 'num',
                               'value': 'Piet',
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
