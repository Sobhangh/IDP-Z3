
-- original ---------------------------------
vocabulary {
    type num constructed from { Piet, Jan}
    same(num) : num
    negated(num) : num
} 

theory {
    { !x[num]: !y[num]: same(x) = y <- y=x. } //TODO { !x[num]: same(x) = x. }
    { negated(Piet) = Jan. negated(Jan)=Piet.} //TODO { !x[num]: negated(x) = (0-x). }
    same(Piet)= Piet.
    same(same(Piet))= negated(negated(Piet)).

}
 
view expanded
-- vocabulary -------------------------------

-- theory -----------------------------------
same(Piet) == Piet

same(same(Piet)) == negated(negated(Piet))

ForAll([c!47, c!48],
       (same(c!47) == c!48) ==
       Or(Or(And(c!47 == Piet, c!48 == Piet),
             And(c!47 == Jan, c!48 == Jan))))

ForAll([c!49, c!50],
       (negated(c!49) == c!50) ==
       Or(And(c!49 == Piet, c!50 == Jan, True),
          And(c!49 == Jan, c!50 == Piet, True)))

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
  Rule:∀['$negated$0', '$negated$'][]: negated($negated$0,$negated$) ⇔($negated$0 = Piet) ∧ ($negated$ = Jan) ∧ true
Rule:∀['$negated$0', '$negated$'][]: negated($negated$0,$negated$) ⇔($negated$0 = Jan) ∧ ($negated$ = Piet) ∧ true
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
