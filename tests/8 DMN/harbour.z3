
-- original ---------------------------------


vocabulary {
	type Refuel_Areat_t := { NA, outdoor, indoor }
	Draft: ()→Int
	Refuel_Area: ()→Refuel_Areat_t
	Length: ()→Int
	Capacity: ()→Int
	Cargo: ()→Int
	Enter:() → Bool
}
theory {
	//Ship Clearance
	{
		Enter() <- Length() < 260 & Draft() < 10 & Capacity() < 1000.
		Enter() <- Length() < 260 & 10 =< Draft() & Draft() =< 12 & Capacity() < 4000 & Cargo() =< 0.75.
		Enter() <- 260 =< Length() & Length() < 320 & 10 < Draft() & Draft() =< 13 & Capacity() < 6000 & Cargo() =< 0.5.
		Enter() <- 320 =< Length() & Length() < 400 & Draft() >= 13 & Capacity() > 4000 & Cargo() =< 0.25.
	}

	//Refuel Area Determination
	{
		Refuel_Area() = NA <- ~(Enter()).
		Refuel_Area() = indoor <- Enter() & Length() =< 350.
		Refuel_Area() = indoor <- Enter() & Length() > 350 & Cargo() =< 0.3.
		Refuel_Area() = outdoor <- Enter() & Length() > 350 & Cargo() > 0.3.
	}

}


structure {
}

-- meta -------------------------------------
{'optionalPropagation': False,
 'symbols': [{'environmental': False,
              'idpname': 'Draft',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Refuel_Area',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Length',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Capacity',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Cargo',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Enter',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'Capacity': {'Capacity': {'environmental': False,
                           'is_assignment': True,
                           'normal': True,
                           'reading': 'Capacity',
                           'relevant': False,
                           'status': 'UNKNOWN',
                           'typ': 'Int',
                           'value': ''},
              '__rank': 9999},
 'Cargo': {'Cargo': {'environmental': False,
                     'is_assignment': True,
                     'normal': True,
                     'reading': 'Cargo',
                     'relevant': False,
                     'status': 'UNKNOWN',
                     'typ': 'Int',
                     'value': ''},
           '__rank': 9999},
 'Draft': {'Draft': {'environmental': False,
                     'is_assignment': True,
                     'normal': True,
                     'reading': 'Draft',
                     'relevant': False,
                     'status': 'UNKNOWN',
                     'typ': 'Int',
                     'value': ''},
           '__rank': 9999},
 'Enter': {'Enter': {'environmental': False,
                     'is_assignment': False,
                     'normal': True,
                     'reading': 'Enter',
                     'relevant': False,
                     'status': 'UNKNOWN',
                     'typ': 'Bool'},
           '__rank': 9999},
 'Length': {'Length': {'environmental': False,
                       'is_assignment': True,
                       'normal': True,
                       'reading': 'Length',
                       'relevant': False,
                       'status': 'UNKNOWN',
                       'typ': 'Int',
                       'value': ''},
            '__rank': 9999},
 'Refuel_Area': {'Refuel_Area': {'environmental': False,
                                 'is_assignment': True,
                                 'normal': True,
                                 'reading': 'Refuel_Area',
                                 'relevant': False,
                                 'status': 'UNKNOWN',
                                 'typ': 'Refuel_Areat_t',
                                 'value': '',
                                 'values': ['NA', 'outdoor', 'indoor']},
                 'Refuel_Area = NA': {'environmental': False,
                                      'is_assignment': True,
                                      'normal': False,
                                      'reading': 'Refuel_Area = NA',
                                      'relevant': False,
                                      'status': 'UNKNOWN',
                                      'typ': 'Bool'},
                 'Refuel_Area = indoor': {'environmental': False,
                                          'is_assignment': True,
                                          'normal': False,
                                          'reading': 'Refuel_Area = indoor',
                                          'relevant': False,
                                          'status': 'UNKNOWN',
                                          'typ': 'Bool'},
                 'Refuel_Area = outdoor': {'environmental': False,
                                           'is_assignment': True,
                                           'normal': False,
                                           'reading': 'Refuel_Area = outdoor',
                                           'relevant': False,
                                           'status': 'CONSEQUENCE',
                                           'typ': 'Bool',
                                           'value': False},
                 '__rank': 9999}}
