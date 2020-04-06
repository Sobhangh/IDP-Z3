
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

And((t == Jan) == Or(Jan == t0, Jan == t1),
    (t == Piet) == Or(Piet == t0, Piet == t1))

-- subtences ------------------------------------
t0 = Piet

-- GUILines ------------------------------------
t
t0
t1
t0 = Piet

-- case -------------------------------------
Type:        
  
Definitions: 
  Rule:∀['$t$'][]: t($t$) ⇔($t$ = t0) ∨ ($t$ = t1)
Universals:  
  t0 = Piet
Consequences:
  t = Piet
  t0 = Piet
  t1 = Piet
Simplified:  
  
Irrelevant:  
  


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
             'values': ['Jan', 'Piet']}},
 't0': {'t0': {'environmental': False,
               'normal': True,
               'reading': 't0',
               'relevant': True,
               'status': 'CONSEQUENCE',
               'typ': 'num',
               'value': 'Piet',
               'values': ['Jan', 'Piet']},
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
               'values': ['Jan', 'Piet']}}}
