
-- original ---------------------------------
vocabulary {
    type num = {1..4}
    Prime(num)
}

theory {
	{ !x[num] : Prime(x) <- !y[num] : 1<y & y<x => x % y ~=0.}
}


-- vocabulary -------------------------------
ForAll(c!764,
       Implies(Prime(c!764),
               And(And(c!764 >= 1, c!764 <= 4))))
-- theory -----------------------------------
ForAll(c!765,
       Prime(c!765) ==
       Or(c!765 == 1, c!765 == 2, c!765 == 3))

-- atoms ------------------------------------
Prime(1)
Prime(2)
Prime(3)
Prime(4)

-- case -------------------------------------
Type:        
  ForAll(c!764,
       Implies(Prime(c!764),
               And(And(c!764 >= 1, c!764 <= 4))))
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
