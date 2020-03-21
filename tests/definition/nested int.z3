
-- original ---------------------------------
vocabulary {
    type num = {-1; 0; 1}
    same(num) : num
    negated(num) : num
} 

theory {
    { !x[num]: same(x) = x. }
    { !x[num]: negated(x) = (0-x). }
    same(-1)= -1.
    negated(negated(-1)) = same(-1).

}
 
view expanded

-- vocabulary -------------------------------

-- theory -----------------------------------
same(-1) == -1

negated(negated(-1)) == same(-1)

And((same(-1) == -1) == True,
    (same(0) == -1) == False,
    (same(1) == -1) == False,
    (same(-1) == 0) == False,
    (same(0) == 0) == True,
    (same(1) == 0) == False,
    (same(-1) == 1) == False,
    (same(0) == 1) == False,
    (same(1) == 1) == True)

And((negated(-1) == -1) == True,
    (negated(0) == -1) == False,
    (negated(1) == -1) == False,
    (negated(-1) == 0) == False,
    (negated(0) == 0) == True,
    (negated(1) == 0) == False,
    (negated(-1) == 1) == False,
    (negated(0) == 1) == False,
    (negated(1) == 1) == True)

-- atoms ------------------------------------
same(-1)
same(0)
same(1)
negated(-1)
negated(0)
negated(1)
same(-(1)) = (-(1))
negated(negated(-(1))) = same(-(1))

-- case -------------------------------------
Type:        
  
Definitions: 
  Rule:∀['$same$0', '$same$'][]: same($same$0,$same$) ⇔((($same$0 = -1) ∧ ($same$ = -1)) ∨ (($same$0 = 0) ∧ ($same$ = 0)) ∨ (($same$0 = 1) ∧ ($same$ = 1)))
  Rule:∀['$negated$0', '$negated$'][]: negated($negated$0,$negated$) ⇔((($negated$0 = -1) ∧ ($negated$ = -1)) ∨ (($negated$0 = 0) ∧ ($negated$ = 0)) ∨ (($negated$0 = 1) ∧ ($negated$ = 1)))
Universals:  
  same(-(1)) = (-(1))
  negated(negated(-(1))) = same(-(1))
Consequences:
  same(-1) = -1
  same(0) = 0
  same(1) = 1
  negated(-1) = -1
  negated(0) = 0
  negated(1) = 1
Simplified:  
  
Irrelevant:  
  


-- propagation ------------------------------
{' Global': {'env_dec': False},
 'negated': {'negated(-1)': {'environmental': False,
                             'normal': True,
                             'reading': 'negated(-1)',
                             'relevant': True,
                             'status': 'CONSEQUENCE',
                             'typ': 'Int',
                             'value': '-1',
                             'values': ['-1', '0', '1']},
             'negated(0)': {'environmental': False,
                            'normal': True,
                            'reading': 'negated(0)',
                            'relevant': True,
                            'status': 'CONSEQUENCE',
                            'typ': 'Int',
                            'value': '0',
                            'values': ['-1', '0', '1']},
             'negated(1)': {'environmental': False,
                            'normal': True,
                            'reading': 'negated(1)',
                            'relevant': True,
                            'status': 'CONSEQUENCE',
                            'typ': 'Int',
                            'value': '1',
                            'values': ['-1', '0', '1']},
             'negated(negated(-(1))) = same(-(1))': {'environmental': False,
                                                     'normal': False,
                                                     'reading': 'negated(negated(-(1))) = same(-(1))',
                                                     'relevant': True,
                                                     'status': 'UNIVERSAL',
                                                     'typ': 'Bool',
                                                     'value': True}},
 'same': {'same(-(1)) = (-(1))': {'environmental': False,
                                  'normal': False,
                                  'reading': 'same(-(1)) = (-(1))',
                                  'relevant': True,
                                  'status': 'UNIVERSAL',
                                  'typ': 'Bool',
                                  'value': True},
          'same(-1)': {'environmental': False,
                       'normal': True,
                       'reading': 'same(-1)',
                       'relevant': True,
                       'status': 'CONSEQUENCE',
                       'typ': 'Int',
                       'value': '-1',
                       'values': ['-1', '0', '1']},
          'same(0)': {'environmental': False,
                      'normal': True,
                      'reading': 'same(0)',
                      'relevant': True,
                      'status': 'CONSEQUENCE',
                      'typ': 'Int',
                      'value': '0',
                      'values': ['-1', '0', '1']},
          'same(1)': {'environmental': False,
                      'normal': True,
                      'reading': 'same(1)',
                      'relevant': True,
                      'status': 'CONSEQUENCE',
                      'typ': 'Int',
                      'value': '1',
                      'values': ['-1', '0', '1']}}}
