
-- original ---------------------------------
vocabulary {
    type epoxy constructed from {e1, e2, e3}
    type brand constructed from {Huntsman, Sadechaf, Jowat}
    type family constructed from {_2c_Epoxy, _1c_Epoxy}
    type cost = {0.539; 100}
    type color constructed from {amber, black_fluorescent, blackish_grey}
    type shelf_life = {0; 6; 12}
    type lowest_storage_t = {0; 15; 16}
    type highest_storage_t = {10; 25; 38}
    type mixing_ratio constructed from {_1_1, _2_1, na}
    type specific_gravity_resin = {1.05; 1.12; 1.17}
    type specific_gravity_hardener = {0; 0.92; 1.28}    


    
    Epoxy: epoxy
    Brand: brand
    Family: family

    Cost: cost
    Min_Cost: real
    Max_Cost: real
    Known_Cost

    Color: color

    Shelf_Life: shelf_life
    Min_Shelf_Life: real
    Max_Shelf_Life: real
    Known_Shelf_Life
   
}


theory {
    
    { // Every epoxy has a known brand.
        Brand = Huntsman <- Epoxy = e1.
        Brand = Sadechaf <- Epoxy = e2.
        Brand = Jowat <- Epoxy = e3.
    }

    { // Every epoxy has a known family.
        Family = _2c_Epoxy <- Epoxy = e1 | Epoxy = e3.
        Family = _1c_Epoxy <- Epoxy = e2.
    }

    
    { // The default value for unknown costs is 100.
        Cost = 0.539 <- Epoxy = e1.
        Cost = 100 <- Epoxy = e2 | Epoxy = e3.
    }

    Known_Cost <=> Cost ~= 100.
    Known_Cost => Min_Cost =< Cost.
    Known_Cost => Max_Cost >= Cost.


    { // Every epoxy has a known color.
        Color = amber <- Epoxy = e1.
        Color = black_fluorescent <- Epoxy = e2.
        Color = blackish_grey <- Epoxy = e3.
    }

    
    { // The dfqsdfq
        Shelf_Life = 12 <- Epoxy = e1.
        Shelf_Life = 6 <- Epoxy = e2.
        Shelf_Life = 0 <- Epoxy = e3.
    }
}




view expanded

-- vocabulary -------------------------------

-- theory -----------------------------------
Known_Cost == Not(Cost == 100)

Or(Not(Known_Cost), Min_Cost <= Cost)

Or(Not(Known_Cost), Max_Cost >= Cost)

Or(Epoxy == e1, Epoxy == e2, Epoxy == e3)

Or(Brand == Huntsman, Brand == Sadechaf, Brand == Jowat)

Or(Family == _2c_Epoxy, Family == _1c_Epoxy)

Or(Cost == 539/1000, Cost == 100)

Or(Color == amber,
   Color == black_fluorescent,
   Color == blackish_grey)

Or(Shelf_Life == 0, Shelf_Life == 6, Shelf_Life == 12)

And((Brand == Huntsman) == (Epoxy == e1),
    (Brand == Sadechaf) == (Epoxy == e2),
    (Brand == Jowat) == (Epoxy == e3))

And((Family == _2c_Epoxy) == Or(Epoxy == e1, Epoxy == e3),
    (Family == _1c_Epoxy) == (Epoxy == e2))

And((Cost == 539/1000) == (Epoxy == e1),
    (Cost == 100) == Or(Epoxy == e2, Epoxy == e3))

And((Color == amber) == (Epoxy == e1),
    (Color == black_fluorescent) == (Epoxy == e2),
    (Color == blackish_grey) == (Epoxy == e3))

And((Shelf_Life == 0) == (Epoxy == e3),
    (Shelf_Life == 6) == (Epoxy == e2),
    (Shelf_Life == 12) == (Epoxy == e1))

-- subtences ------------------------------------
Known_Cost
Cost = 100
Cost = 0.539
Epoxy = e1
Epoxy = e2
Epoxy = e3
Min_Cost ≤ Cost
Max_Cost ≥ Cost
Brand = Huntsman
Brand = Sadechaf
Brand = Jowat
Family = _2c_Epoxy
Family = _1c_Epoxy
Color = amber
Color = black_fluorescent
Color = blackish_grey
Shelf_Life = 0
Shelf_Life = 6
Shelf_Life = 12

-- GUILines ------------------------------------
Epoxy
Brand
Family
Cost
Min_Cost
Max_Cost
Known_Cost
Color
Shelf_Life
Min_Shelf_Life
Max_Shelf_Life
Known_Shelf_Life
Cost = 100
Cost = 0.539
Epoxy = e1
Epoxy = e2
Epoxy = e3
Min_Cost ≤ Cost
Max_Cost ≥ Cost
Brand = Huntsman
Brand = Sadechaf
Brand = Jowat
Family = _2c_Epoxy
Family = _1c_Epoxy
Color = amber
Color = black_fluorescent
Color = blackish_grey
Shelf_Life = 0
Shelf_Life = 6
Shelf_Life = 12

-- case -------------------------------------
Type:        
  
Definitions: 
  Rule:∀['$Brand$'][]: Brand($Brand$) ⇔(($Brand$ = Huntsman) ∧ (Epoxy = e1)) ∨ (($Brand$ = Sadechaf) ∧ (Epoxy = e2)) ∨ (($Brand$ = Jowat) ∧ (Epoxy = e3))
  Rule:∀['$Family$'][]: Family($Family$) ⇔(($Family$ = _2c_Epoxy) ∧ ((Epoxy = e1) ∨ (Epoxy = e3))) ∨ (($Family$ = _1c_Epoxy) ∧ (Epoxy = e2))
  Rule:∀['$Cost$'][]: Cost($Cost$) ⇔(($Cost$ = 0.539) ∧ (Epoxy = e1)) ∨ (($Cost$ = 100) ∧ ((Epoxy = e2) ∨ (Epoxy = e3)))
  Rule:∀['$Color$'][]: Color($Color$) ⇔(($Color$ = amber) ∧ (Epoxy = e1)) ∨ (($Color$ = black_fluorescent) ∧ (Epoxy = e2)) ∨ (($Color$ = blackish_grey) ∧ (Epoxy = e3))
  Rule:∀['$Shelf_Life$'][]: Shelf_Life($Shelf_Life$) ⇔(($Shelf_Life$ = 12) ∧ (Epoxy = e1)) ∨ (($Shelf_Life$ = 6) ∧ (Epoxy = e2)) ∨ (($Shelf_Life$ = 0) ∧ (Epoxy = e3))
Universals:  
  
Consequences:
  
Simplified:  
  Known_Cost ⇔ (~(Cost = 100))
  Known_Cost ⇒ (Min_Cost ≤ Cost)
  Known_Cost ⇒ (Max_Cost ≥ Cost)
  (Epoxy = e1) ∨ (Epoxy = e2) ∨ (Epoxy = e3)
  (Cost = 0.539) ∨ (Cost = 100)
Irrelevant:  
  ~Brand = Huntsman
  ~Brand = Sadechaf
  ~Brand = Jowat
  ~Family = _2c_Epoxy
  ~Family = _1c_Epoxy
  ~Color = amber
  ~Color = black_fluorescent
  ~Color = blackish_grey
  ~Shelf_Life = 0
  ~Shelf_Life = 6
  ~Shelf_Life = 12


-- meta -------------------------------------
{'symbols': [{'idpname': 'Epoxy', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'},
             {'idpname': 'Brand', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'},
             {'idpname': 'Family', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'},
             {'idpname': 'Cost', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'},
             {'idpname': 'Min_Cost', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'},
             {'idpname': 'Max_Cost', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'},
             {'idpname': 'Known_Cost',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'expanded'},
             {'idpname': 'Color', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'},
             {'idpname': 'Shelf_Life',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'Brand': {'Brand': {'environmental': False,
                     'normal': True,
                     'reading': 'Brand',
                     'relevant': False,
                     'status': 'UNKNOWN',
                     'typ': 'brand',
                     'value': '',
                     'values': ['Huntsman', 'Sadechaf', 'Jowat']},
           'Brand = Huntsman': {'environmental': False,
                                'normal': False,
                                'reading': 'Brand = Huntsman',
                                'relevant': False,
                                'status': 'UNKNOWN',
                                'typ': 'Bool'},
           'Brand = Jowat': {'environmental': False,
                             'normal': False,
                             'reading': 'Brand = Jowat',
                             'relevant': False,
                             'status': 'UNKNOWN',
                             'typ': 'Bool'},
           'Brand = Sadechaf': {'environmental': False,
                                'normal': False,
                                'reading': 'Brand = Sadechaf',
                                'relevant': False,
                                'status': 'UNKNOWN',
                                'typ': 'Bool'}},
 'Color': {'Color': {'environmental': False,
                     'normal': True,
                     'reading': 'Color',
                     'relevant': False,
                     'status': 'UNKNOWN',
                     'typ': 'color',
                     'value': '',
                     'values': ['amber', 'black_fluorescent', 'blackish_grey']},
           'Color = amber': {'environmental': False,
                             'normal': False,
                             'reading': 'Color = amber',
                             'relevant': False,
                             'status': 'UNKNOWN',
                             'typ': 'Bool'},
           'Color = black_fluorescent': {'environmental': False,
                                         'normal': False,
                                         'reading': 'Color = black_fluorescent',
                                         'relevant': False,
                                         'status': 'UNKNOWN',
                                         'typ': 'Bool'},
           'Color = blackish_grey': {'environmental': False,
                                     'normal': False,
                                     'reading': 'Color = blackish_grey',
                                     'relevant': False,
                                     'status': 'UNKNOWN',
                                     'typ': 'Bool'}},
 'Cost': {'Cost': {'environmental': False,
                   'normal': True,
                   'reading': 'Cost',
                   'relevant': True,
                   'status': 'UNKNOWN',
                   'typ': 'Real',
                   'value': '',
                   'values': ['0.539', '100']},
          'Cost = 0.539': {'environmental': False,
                           'normal': False,
                           'reading': 'Cost = 0.539',
                           'relevant': True,
                           'status': 'UNKNOWN',
                           'typ': 'Bool'},
          'Cost = 100': {'environmental': False,
                         'normal': False,
                         'reading': 'Cost = 100',
                         'relevant': True,
                         'status': 'UNKNOWN',
                         'typ': 'Bool'}},
 'Epoxy': {'Epoxy': {'environmental': False,
                     'normal': True,
                     'reading': 'Epoxy',
                     'relevant': True,
                     'status': 'UNKNOWN',
                     'typ': 'epoxy',
                     'value': '',
                     'values': ['e1', 'e2', 'e3']},
           'Epoxy = e1': {'environmental': False,
                          'normal': False,
                          'reading': 'Epoxy = e1',
                          'relevant': True,
                          'status': 'UNKNOWN',
                          'typ': 'Bool'},
           'Epoxy = e2': {'environmental': False,
                          'normal': False,
                          'reading': 'Epoxy = e2',
                          'relevant': True,
                          'status': 'UNKNOWN',
                          'typ': 'Bool'},
           'Epoxy = e3': {'environmental': False,
                          'normal': False,
                          'reading': 'Epoxy = e3',
                          'relevant': True,
                          'status': 'UNKNOWN',
                          'typ': 'Bool'}},
 'Family': {'Family': {'environmental': False,
                       'normal': True,
                       'reading': 'Family',
                       'relevant': False,
                       'status': 'UNKNOWN',
                       'typ': 'family',
                       'value': '',
                       'values': ['_2c_Epoxy', '_1c_Epoxy']},
            'Family = _1c_Epoxy': {'environmental': False,
                                   'normal': False,
                                   'reading': 'Family = _1c_Epoxy',
                                   'relevant': False,
                                   'status': 'UNKNOWN',
                                   'typ': 'Bool'},
            'Family = _2c_Epoxy': {'environmental': False,
                                   'normal': False,
                                   'reading': 'Family = _2c_Epoxy',
                                   'relevant': False,
                                   'status': 'UNKNOWN',
                                   'typ': 'Bool'}},
 'Known_Cost': {'Known_Cost': {'environmental': False,
                               'normal': True,
                               'reading': 'Known_Cost',
                               'relevant': True,
                               'status': 'UNKNOWN',
                               'typ': 'Bool'}},
 'Known_Shelf_Life': {'Known_Shelf_Life': {'environmental': False,
                                           'normal': True,
                                           'reading': 'Known_Shelf_Life',
                                           'relevant': False,
                                           'status': 'UNKNOWN',
                                           'typ': 'Bool'}},
 'Max_Cost': {'Max_Cost': {'environmental': False,
                           'normal': True,
                           'reading': 'Max_Cost',
                           'relevant': True,
                           'status': 'UNKNOWN',
                           'typ': 'Real',
                           'value': ''},
              'Max_Cost ≥ Cost': {'environmental': False,
                                  'normal': False,
                                  'reading': 'Max_Cost ≥ Cost',
                                  'relevant': True,
                                  'status': 'UNKNOWN',
                                  'typ': 'Bool'}},
 'Max_Shelf_Life': {'Max_Shelf_Life': {'environmental': False,
                                       'normal': True,
                                       'reading': 'Max_Shelf_Life',
                                       'relevant': False,
                                       'status': 'UNKNOWN',
                                       'typ': 'Real',
                                       'value': ''}},
 'Min_Cost': {'Min_Cost': {'environmental': False,
                           'normal': True,
                           'reading': 'Min_Cost',
                           'relevant': True,
                           'status': 'UNKNOWN',
                           'typ': 'Real',
                           'value': ''},
              'Min_Cost ≤ Cost': {'environmental': False,
                                  'normal': False,
                                  'reading': 'Min_Cost ≤ Cost',
                                  'relevant': True,
                                  'status': 'UNKNOWN',
                                  'typ': 'Bool'}},
 'Min_Shelf_Life': {'Min_Shelf_Life': {'environmental': False,
                                       'normal': True,
                                       'reading': 'Min_Shelf_Life',
                                       'relevant': False,
                                       'status': 'UNKNOWN',
                                       'typ': 'Real',
                                       'value': ''}},
 'Shelf_Life': {'Shelf_Life': {'environmental': False,
                               'normal': True,
                               'reading': 'Shelf_Life',
                               'relevant': False,
                               'status': 'UNKNOWN',
                               'typ': 'Int',
                               'value': '',
                               'values': ['0', '6', '12']},
                'Shelf_Life = 0': {'environmental': False,
                                   'normal': False,
                                   'reading': 'Shelf_Life = 0',
                                   'relevant': False,
                                   'status': 'UNKNOWN',
                                   'typ': 'Bool'},
                'Shelf_Life = 12': {'environmental': False,
                                    'normal': False,
                                    'reading': 'Shelf_Life = 12',
                                    'relevant': False,
                                    'status': 'UNKNOWN',
                                    'typ': 'Bool'},
                'Shelf_Life = 6': {'environmental': False,
                                   'normal': False,
                                   'reading': 'Shelf_Life = 6',
                                   'relevant': False,
                                   'status': 'UNKNOWN',
                                   'typ': 'Bool'}}}
