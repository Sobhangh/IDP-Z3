
-- original ---------------------------------
vocabulary {
    type color constructed from {red, blue, green}
    p
    q(color)
} 
theory {
    p <=> (∀c[color]: c=red).
    ∀c[color]: q(c).
}
view expanded
-- vocabulary -------------------------------

-- theory -----------------------------------
Not(p)

And(q(red), q(blue), q(green))

-- subtences ------------------------------------
p
∀c[color] : c = red
∀c[color] : q(c)

-- GUILines ------------------------------------
p
q(red)
q(blue)
q(green)
∀c[color] : c = red
∀c[color] : q(c)

-- case -------------------------------------
Type:        
  
Definitions: 
  
Universals:  
  ~p
  q(red)
  q(blue)
  q(green)
  ∀c[color] : q(c)
Consequences:
  
Simplified:  
  false ⇔ (false)
  ∀ : true
Irrelevant:  
  
Co-constraints:
  


-- meta -------------------------------------
{'symbols': [{'idpname': 'p', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'expanded'},
             {'idpname': 'q', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'p': {'p': {'environmental': False,
             'normal': True,
             'reading': 'p',
             'relevant': True,
             'status': 'UNIVERSAL',
             'typ': 'Bool',
             'value': False}},
 'q': {'q(blue)': {'environmental': False,
                   'normal': True,
                   'reading': 'q(blue)',
                   'relevant': True,
                   'status': 'UNIVERSAL',
                   'typ': 'Bool',
                   'value': True},
       'q(green)': {'environmental': False,
                    'normal': True,
                    'reading': 'q(green)',
                    'relevant': True,
                    'status': 'UNIVERSAL',
                    'typ': 'Bool',
                    'value': True},
       'q(red)': {'environmental': False,
                  'normal': True,
                  'reading': 'q(red)',
                  'relevant': True,
                  'status': 'UNIVERSAL',
                  'typ': 'Bool',
                  'value': True},
       '∀c[color] : q(c)': {'environmental': False,
                            'normal': False,
                            'reading': '∀c[color] : q(c)',
                            'relevant': True,
                            'status': 'UNIVERSAL',
                            'typ': 'Bool',
                            'value': True}}}
