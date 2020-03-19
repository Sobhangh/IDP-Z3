
-- original ---------------------------------
vocabulary {
    type num = {1..4}
    Prime(num)
}

theory {
	{ !x[num] : Prime(x) <- !y[num] : 1<y & y<x => x % y ~=0.}
}


-- vocabulary -------------------------------
ForAll(c!650,
       Implies(Prime(c!650),
               And(And(c!650 >= 1, c!650 <= 4))))
-- theory -----------------------------------
ForAll(c!651,
       Prime(c!651) ==
       Or(c!651 == 1, c!651 == 2, c!651 == 3))

-- atoms ------------------------------------
Prime(1)
Prime(2)
Prime(3)
Prime(4)

-- case -------------------------------------
Type:        
  ForAll(c!650,
       Implies(Prime(c!650),
               And(And(c!650 >= 1, c!650 <= 4))))
Definitions: 
  Rule:∀[][[]]: Prime(1) ⇔($Prime$0 = 1)
Rule:∀[][[]]: Prime(2) ⇔($Prime$0 = 2)
Rule:∀[][[]]: Prime(3) ⇔($Prime$0 = 3)
Rule:∀[][[]]: Prime(4) ⇔(false)
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
