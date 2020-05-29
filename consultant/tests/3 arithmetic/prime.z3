
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
True

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
  Rule:∀$Prime!0$[num]: Prime($Prime!0$) ⇔true ∧ (2 < $Prime!0$ ⇒ ~($Prime!0$ % 2 = 0)) ∧ (3 < $Prime!0$ ⇒ ~($Prime!0$ % 3 = 0)) ∧ (4 < $Prime!0$ ⇒ ~($Prime!0$ % 4 = 0))
Universals:  
  Prime(1)
  Prime(2)
  Prime(3)
  ~Prime(4)
Consequences:
  
Simplified:  
  __goals(true,true,true,false)
Irrelevant:  
  
Co-constraints:
  true ⇔ true
  true ⇔ true
  true ⇔ true
  false ⇔ false


-- meta -------------------------------------
{'symbols': [{'environmental': False,
              'idpname': 'Prime',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'Prime': {'Prime(1)': {'environmental': False,
                        'normal': True,
                        'reading': 'Prime(1)',
                        'relevant': True,
                        'status': 'UNIVERSAL',
                        'typ': 'Bool',
                        'value': True},
           'Prime(2)': {'environmental': False,
                        'normal': True,
                        'reading': 'Prime(2)',
                        'relevant': True,
                        'status': 'UNIVERSAL',
                        'typ': 'Bool',
                        'value': True},
           'Prime(3)': {'environmental': False,
                        'normal': True,
                        'reading': 'Prime(3)',
                        'relevant': True,
                        'status': 'UNIVERSAL',
                        'typ': 'Bool',
                        'value': True},
           'Prime(4)': {'environmental': False,
                        'normal': True,
                        'reading': 'Prime(4)',
                        'relevant': True,
                        'status': 'UNIVERSAL',
                        'typ': 'Bool',
                        'value': False},
           '__rank': 1}}
