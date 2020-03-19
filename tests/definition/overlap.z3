
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

ForAll(c!34, (t == c!34) == Or(c!34 == t0, c!34 == t1))

-- atoms ------------------------------------
t
t0
t1
t0 = Piet

-- case -------------------------------------
Type:        
  
Definitions: 
  Rule:∀[][[]]: t(t0) ⇔($t$ = t0)
Rule:∀[][[]]: t(t1) ⇔($t$ = t1)
Universals:  
  t0 = Piet
Consequences:
  t = Piet
  t0 = Piet
  t1 = Piet
Simplified:  
  
Irrelevant:  
  


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
