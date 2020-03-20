
-- original ---------------------------------
vocabulary {
    type num = {1..4}
    Prime(num)
}

theory {
	{ !x[num] : Prime(x) <- !y[num] : 1<y & y<x => x % y ~=0.}
}


-- vocabulary -------------------------------

-- theory -----------------------------------
ForAll(c!355,
       Prime(c!355) ==
       Or(Or(c!355 == 1, c!355 == 2, c!355 == 3, False)))

-- atoms ------------------------------------
Prime(1)
Prime(2)
Prime(3)
Prime(4)

-- case -------------------------------------
Type:        
  
Definitions: 
  Rule:∀['$Prime$0'][]: Prime($Prime$0) ⇔(($Prime$0 = 1) ∨ ($Prime$0 = 2) ∨ ($Prime$0 = 3) ∨ (false))
Universals:  
  
Consequences:
  Prime(1)
  Prime(2)
  Prime(3)
  ~Prime(4)
Simplified:  
  
Irrelevant:  
  


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
