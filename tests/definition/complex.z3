
-- original ---------------------------------
vocabulary {
    type num = {-1; 0; 1}
    same(num) : num
    negated(num) : num
} 

theory {
    { !x[num]: same(x) = x. }
    { !x[num]: same(x) = -(-x). }
    { !x[num]: negated(same(x)) = (0-x). }
    same(1)= 1.
    same(same(-1))= negated(negated(-1)).

}
 
view expanded
-- vocabulary -------------------------------

-- theory -----------------------------------
same(1) == 1

same(same(-1)) == negated(negated(-1))

Or(same(-1) == -1, same(-1) == 0, same(-1) == 1)

Or(same(0) == -1, same(0) == 0, same(0) == 1)

Or(same(1) == -1, same(1) == 0, same(1) == 1)

Or(negated(-1) == -1, negated(-1) == 0, negated(-1) == 1)

Or(negated(0) == -1, negated(0) == 0, negated(0) == 1)

Or(negated(1) == -1, negated(1) == 0, negated(1) == 1)

And(same(-1) == -1,
    Not(same(-1) == 0),
    Not(same(-1) == 1),
    Not(same(0) == -1),
    same(0) == 0,
    Not(same(0) == 1),
    Not(same(1) == -1),
    Not(same(1) == 0),
    same(1) == 1)

And(same(-1) == -1,
    Not(same(-1) == 0),
    Not(same(-1) == 1),
    Not(same(0) == -1),
    same(0) == 0,
    Not(same(0) == 1),
    Not(same(1) == -1),
    Not(same(1) == 0),
    same(1) == 1)

And((negated(-1) == -1) == (same(1) == -1),
    (negated(-1) == 0) == (same(0) == -1),
    (negated(-1) == 1) == (same(-1) == -1),
    (negated(0) == -1) == (same(1) == 0),
    (negated(0) == 0) == (same(0) == 0),
    (negated(0) == 1) == (same(-1) == 0),
    (negated(1) == -1) == (same(1) == 1),
    (negated(1) == 0) == (same(0) == 1),
    (negated(1) == 1) == (same(-1) == 1))

-- subtences ------------------------------------
same(1) = 1
same(1) = (-((-(1))))
same(-1) = (-((-(-1))))
negated(-1) = (0 - x)
-1 = same(x)
same(0) = (-((-(0))))
negated(-1) = same(x)
same(-1) = -1
same(-1) = 0
same(-1) = 1
same(0) = -1
same(0) = 0
same(0) = 1
same(1) = -1
same(1) = 0
negated(-1) = -1
negated(-1) = 0
negated(-1) = 1
negated(0) = -1
negated(0) = 0
negated(0) = 1
negated(1) = -1
negated(1) = 0
negated(1) = 1

-- GUILines ------------------------------------
same(-1)
same(0)
same(1)
negated(-1)
negated(0)
negated(1)
same(1) = 1
same(1) = (-((-(1))))
same(-1) = (-((-(-1))))
negated(-1) = (0 - x)
-1 = same(x)
same(0) = (-((-(0))))
negated(-1) = same(x)
same(-1) = -1
same(-1) = 0
same(-1) = 1
same(0) = -1
same(0) = 0
same(0) = 1
same(1) = -1
same(1) = 0
negated(-1) = -1
negated(-1) = 0
negated(-1) = 1
negated(0) = -1
negated(0) = 0
negated(0) = 1
negated(1) = -1
negated(1) = 0
negated(1) = 1

-- case -------------------------------------
Type:        
  
Definitions: 
  Rule:∀['$same!0$', '$same$'][]: same($same!0$,$same$) ⇔($same$ = $same!0$)
  Rule:∀['$same!0$', '$same$'][]: same($same!0$,$same$) ⇔($same$ = (-((-($same!0$)))))
  Rule:∀['$negated!0$', '$negated$'][]: negated($negated!0$,$negated$) ⇔((($negated$ = (1)) ∧ (($negated!0$ = same(-1)))) ∨ (($negated$ = (0)) ∧ (($negated!0$ = same(0)))) ∨ (($negated$ = (-1)) ∧ (($negated!0$ = same(1)))))
Universals:  
  same(1) = 1
Consequences:
  same(1) = (-((-(1))))
  same(-1) = (-((-(-1))))
  ~negated(-1) = (0 - x)
  ~-1 = same(x)
  same(0) = (-((-(0))))
  ~negated(-1) = same(x)
  same(-1) = -1
  ~same(-1) = 0
  ~same(-1) = 1
  ~same(0) = -1
  same(0) = 0
  ~same(0) = 1
  ~same(1) = -1
  ~same(1) = 0
  ~negated(-1) = -1
  ~negated(-1) = 0
  negated(-1) = 1
  ~negated(0) = -1
  negated(0) = 0
  negated(0) = 1
  negated(1) = -1
  negated(1) = 0
  negated(1) = 1
  same(-1) = -1
  same(0) = 0
  same(1) = 1
  negated(-1) = 1
  negated(0) = 0
  negated(1) = -1
Simplified:  
  same(same(-1)) = negated(negated(-1))
Irrelevant:  
  ~same(1) = -1
  ~same(1) = 0


-- meta -------------------------------------
{'symbols': [{'idpname': 'same', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'},
             {'idpname': 'negated', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'negated': {'negated(-1)': {'environmental': False,
                             'normal': True,
                             'reading': 'negated(-1)',
                             'relevant': True,
                             'status': 'CONSEQUENCE',
                             'typ': 'Int',
                             'value': '1',
                             'values': ['-1', '0', '1']},
             'negated(-1) = (0 - x)': {'environmental': False,
                                       'normal': False,
                                       'reading': '$negated$ = (0 - x)',
                                       'relevant': True,
                                       'status': 'CONSEQUENCE',
                                       'typ': 'Bool',
                                       'value': False},
             'negated(-1) = -1': {'environmental': False,
                                  'normal': False,
                                  'reading': 'negated(-1) = -1',
                                  'relevant': True,
                                  'status': 'CONSEQUENCE',
                                  'typ': 'Bool',
                                  'value': False},
             'negated(-1) = 0': {'environmental': False,
                                 'normal': False,
                                 'reading': 'negated(-1) = 0',
                                 'relevant': True,
                                 'status': 'CONSEQUENCE',
                                 'typ': 'Bool',
                                 'value': False},
             'negated(-1) = 1': {'environmental': False,
                                 'normal': False,
                                 'reading': 'negated(-1) = 1',
                                 'relevant': True,
                                 'status': 'CONSEQUENCE',
                                 'typ': 'Bool',
                                 'value': True},
             'negated(-1) = same(x)': {'environmental': False,
                                       'normal': False,
                                       'reading': '$negated!0$ = same(x)',
                                       'relevant': True,
                                       'status': 'CONSEQUENCE',
                                       'typ': 'Bool',
                                       'value': False},
             'negated(0)': {'environmental': False,
                            'normal': True,
                            'reading': 'negated(0)',
                            'relevant': True,
                            'status': 'CONSEQUENCE',
                            'typ': 'Int',
                            'value': '0',
                            'values': ['-1', '0', '1']},
             'negated(0) = -1': {'environmental': False,
                                 'normal': False,
                                 'reading': 'negated(0) = -1',
                                 'relevant': True,
                                 'status': 'CONSEQUENCE',
                                 'typ': 'Bool',
                                 'value': False},
             'negated(0) = 0': {'environmental': False,
                                'normal': False,
                                'reading': 'negated(0) = 0',
                                'relevant': True,
                                'status': 'CONSEQUENCE',
                                'typ': 'Bool',
                                'value': True},
             'negated(0) = 1': {'environmental': False,
                                'normal': False,
                                'reading': 'negated(0) = 1',
                                'relevant': True,
                                'status': 'CONSEQUENCE',
                                'typ': 'Bool',
                                'value': True},
             'negated(1)': {'environmental': False,
                            'normal': True,
                            'reading': 'negated(1)',
                            'relevant': True,
                            'status': 'CONSEQUENCE',
                            'typ': 'Int',
                            'value': '-1',
                            'values': ['-1', '0', '1']},
             'negated(1) = -1': {'environmental': False,
                                 'normal': False,
                                 'reading': 'negated(1) = -1',
                                 'relevant': True,
                                 'status': 'CONSEQUENCE',
                                 'typ': 'Bool',
                                 'value': True},
             'negated(1) = 0': {'environmental': False,
                                'normal': False,
                                'reading': 'negated(1) = 0',
                                'relevant': True,
                                'status': 'CONSEQUENCE',
                                'typ': 'Bool',
                                'value': True},
             'negated(1) = 1': {'environmental': False,
                                'normal': False,
                                'reading': 'negated(1) = 1',
                                'relevant': True,
                                'status': 'CONSEQUENCE',
                                'typ': 'Bool',
                                'value': True}},
 'same': {'-1 = same(x)': {'environmental': False,
                           'normal': False,
                           'reading': '$negated!0$ = same(x)',
                           'relevant': True,
                           'status': 'CONSEQUENCE',
                           'typ': 'Bool',
                           'value': False},
          'same(-1)': {'environmental': False,
                       'normal': True,
                       'reading': 'same(-1)',
                       'relevant': True,
                       'status': 'CONSEQUENCE',
                       'typ': 'Int',
                       'value': '-1',
                       'values': ['-1', '0', '1']},
          'same(-1) = (-((-(-1))))': {'environmental': False,
                                      'normal': False,
                                      'reading': '$same$ = (-((-(x))))',
                                      'relevant': True,
                                      'status': 'CONSEQUENCE',
                                      'typ': 'Bool',
                                      'value': True},
          'same(-1) = -1': {'environmental': False,
                            'normal': False,
                            'reading': 'same(-1) = -1',
                            'relevant': True,
                            'status': 'CONSEQUENCE',
                            'typ': 'Bool',
                            'value': True},
          'same(-1) = 0': {'environmental': False,
                           'normal': False,
                           'reading': 'same(-1) = 0',
                           'relevant': True,
                           'status': 'CONSEQUENCE',
                           'typ': 'Bool',
                           'value': False},
          'same(-1) = 1': {'environmental': False,
                           'normal': False,
                           'reading': 'same(-1) = 1',
                           'relevant': True,
                           'status': 'CONSEQUENCE',
                           'typ': 'Bool',
                           'value': False},
          'same(0)': {'environmental': False,
                      'normal': True,
                      'reading': 'same(0)',
                      'relevant': True,
                      'status': 'CONSEQUENCE',
                      'typ': 'Int',
                      'value': '0',
                      'values': ['-1', '0', '1']},
          'same(0) = (-((-(0))))': {'environmental': False,
                                    'normal': False,
                                    'reading': '$same$ = (-((-(x))))',
                                    'relevant': True,
                                    'status': 'CONSEQUENCE',
                                    'typ': 'Bool',
                                    'value': True},
          'same(0) = -1': {'environmental': False,
                           'normal': False,
                           'reading': 'same(0) = -1',
                           'relevant': True,
                           'status': 'CONSEQUENCE',
                           'typ': 'Bool',
                           'value': False},
          'same(0) = 0': {'environmental': False,
                          'normal': False,
                          'reading': 'same(0) = 0',
                          'relevant': True,
                          'status': 'CONSEQUENCE',
                          'typ': 'Bool',
                          'value': True},
          'same(0) = 1': {'environmental': False,
                          'normal': False,
                          'reading': 'same(0) = 1',
                          'relevant': True,
                          'status': 'CONSEQUENCE',
                          'typ': 'Bool',
                          'value': False},
          'same(1)': {'environmental': False,
                      'normal': True,
                      'reading': 'same(1)',
                      'relevant': True,
                      'status': 'CONSEQUENCE',
                      'typ': 'Int',
                      'value': '1',
                      'values': ['-1', '0', '1']},
          'same(1) = (-((-(1))))': {'environmental': False,
                                    'normal': False,
                                    'reading': '$same$ = (-((-(x))))',
                                    'relevant': True,
                                    'status': 'CONSEQUENCE',
                                    'typ': 'Bool',
                                    'value': True},
          'same(1) = -1': {'environmental': False,
                           'normal': False,
                           'reading': 'same(1) = -1',
                           'relevant': False,
                           'status': 'CONSEQUENCE',
                           'typ': 'Bool',
                           'value': False},
          'same(1) = 0': {'environmental': False,
                          'normal': False,
                          'reading': 'same(1) = 0',
                          'relevant': False,
                          'status': 'CONSEQUENCE',
                          'typ': 'Bool',
                          'value': False},
          'same(1) = 1': {'environmental': False,
                          'normal': False,
                          'reading': 'same(1) = 1',
                          'relevant': True,
                          'status': 'UNIVERSAL',
                          'typ': 'Bool',
                          'value': True}}}
