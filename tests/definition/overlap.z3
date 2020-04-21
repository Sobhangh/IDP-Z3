
-- original ---------------------------------
vocabulary {
	type num constructed from {Jan, Piet}
    t:num
    t0: num
    t1: num  
}

theory {
    { t=t0. t=t1.}
    t0=Piet.
}
-- vocabulary -------------------------------

-- theory -----------------------------------
t0 == Piet

Or(t == Jan, t == Piet)

Or(t0 == Jan, t0 == Piet)

Or(t1 == Jan, t1 == Piet)

And((t == Jan) == Or(Jan == t0, Jan == t1),
    (t == Piet) == Or(Piet == t0, Piet == t1))

-- subtences ------------------------------------
t0 = Piet
t = Jan
t = Piet
t0 = Jan
t1 = Jan
t1 = Piet

-- GUILines ------------------------------------
t
t0
t1
t0 = Piet
t = Jan
t = Piet
t0 = Jan
t1 = Jan
t1 = Piet

-- case -------------------------------------
Type:        
  
Definitions: 
  Rule:∀['$t$'][]: t($t$) ⇔($t$ = t0) ∨ ($t$ = t1)
Universals:  
  t0 = Piet
Consequences:
  ~t = Jan
  t = Piet
  ~t0 = Jan
  ~t1 = Jan
  t1 = Piet
  t = Piet
  t0 = Piet
  t1 = Piet
Simplified:  
  
Irrelevant:  
  ~t = Jan
  t = Piet
  ~t0 = Jan
  ~t1 = Jan
  t1 = Piet


-- meta -------------------------------------
{'symbols': [{'idpname': 't', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'normal'},
             {'idpname': 't0', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'normal'},
             {'idpname': 't1', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 't': {'t': {'environmental': False,
             'normal': True,
             'reading': 't',
             'relevant': True,
             'status': 'CONSEQUENCE',
             'typ': 'num',
             'value': 'Piet',
             'values': ['Jan', 'Piet']},
       't = Jan': {'environmental': False,
                   'normal': False,
                   'reading': 't = Jan',
                   'relevant': False,
                   'status': 'CONSEQUENCE',
                   'typ': 'Bool',
                   'value': False},
       't = Piet': {'environmental': False,
                    'normal': False,
                    'reading': 't = Piet',
                    'relevant': False,
                    'status': 'CONSEQUENCE',
                    'typ': 'Bool',
                    'value': True}},
 't0': {'t0': {'environmental': False,
               'normal': True,
               'reading': 't0',
               'relevant': True,
               'status': 'CONSEQUENCE',
               'typ': 'num',
               'value': 'Piet',
               'values': ['Jan', 'Piet']},
        't0 = Jan': {'environmental': False,
                     'normal': False,
                     'reading': 't0 = Jan',
                     'relevant': False,
                     'status': 'CONSEQUENCE',
                     'typ': 'Bool',
                     'value': False},
        't0 = Piet': {'environmental': False,
                      'normal': False,
                      'reading': 't0 = Piet',
                      'relevant': True,
                      'status': 'UNIVERSAL',
                      'typ': 'Bool',
                      'value': True}},
 't1': {'t1': {'environmental': False,
               'normal': True,
               'reading': 't1',
               'relevant': True,
               'status': 'CONSEQUENCE',
               'typ': 'num',
               'value': 'Piet',
               'values': ['Jan', 'Piet']},
        't1 = Jan': {'environmental': False,
                     'normal': False,
                     'reading': 't1 = Jan',
                     'relevant': False,
                     'status': 'CONSEQUENCE',
                     'typ': 'Bool',
                     'value': False},
        't1 = Piet': {'environmental': False,
                      'normal': False,
                      'reading': 't1 = Piet',
                      'relevant': False,
                      'status': 'CONSEQUENCE',
                      'typ': 'Bool',
                      'value': True}}}
