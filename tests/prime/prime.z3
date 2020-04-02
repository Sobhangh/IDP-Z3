
-- original ---------------------------------
vocabulary {
    type num = {1..4}
    Prime(num)
}

theory {
	{ !x[num] : Prime(x) <- !y[num] : 1<y & y<x => x % y ~=0.}
}

goal Prime
-- vocabulary -------------------------------

-- theory -----------------------------------
And(Prime(1), Prime(2), Prime(3), Not(Prime(4)))

-- goal -----------------------------------
And(Prime(1), Prime(2), Prime(3), Not(Prime(4)))

-- subtences ------------------------------------
Prime(1)
Prime(2)
Prime(3)
Prime(4)

-- GUILines ------------------------------------
Prime(1)
Prime(2)
Prime(3)
Prime(4)

-- case -------------------------------------
Type:        
  
Definitions: 
  Rule:∀['$Prime!0$'][]: Prime($Prime!0$) ⇔(((2 < $Prime!0$) ⇒ (~(($Prime!0$ % 2) = 0))) ∧ ((3 < $Prime!0$) ⇒ (~(($Prime!0$ % 3) = 0))) ∧ ((4 < $Prime!0$) ⇒ (~(($Prime!0$ % 4) = 0))))
Universals:  
  
Consequences:
  Prime(1)
  Prime(2)
  Prime(3)
  ~Prime(4)
Simplified:  
  
Irrelevant:  
  


-- meta -------------------------------------
{'symbols': [{'idpname': 'Prime', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'Prime': {'Prime(1)': {'environmental': False,
                        'normal': True,
                        'reading': 'Prime(1)',
                        'relevant': True,
                        'status': 'CONSEQUENCE',
                        'typ': 'Bool',
                        'value': True},
           'Prime(2)': {'environmental': False,
                        'normal': True,
                        'reading': 'Prime(2)',
                        'relevant': True,
                        'status': 'CONSEQUENCE',
                        'typ': 'Bool',
                        'value': True},
           'Prime(3)': {'environmental': False,
                        'normal': True,
                        'reading': 'Prime(3)',
                        'relevant': True,
                        'status': 'CONSEQUENCE',
                        'typ': 'Bool',
                        'value': True},
           'Prime(4)': {'environmental': False,
                        'normal': True,
                        'reading': 'Prime(4)',
                        'relevant': True,
                        'status': 'CONSEQUENCE',
                        'typ': 'Bool',
                        'value': False}}}
