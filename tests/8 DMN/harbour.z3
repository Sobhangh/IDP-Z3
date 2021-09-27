
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
{'manualPropagation': False,
 'manualRelevance': False,
 'optionalPropagation': False,
 'optionalRelevance': False,
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
{' Global': {'active': '{}', 'env_dec': False},
 'Capacity': {'Capacity()': {'environmental': False,
                             'is_assignment': True,
                             'normal': True,
                             'reading': 'Capacity',
                             'relevant': True,
                             'status': 'UNKNOWN',
                             'typ': 'Int',
                             'value': ''},
              '__rank': 9999},
 'Cargo': {'Cargo()': {'environmental': False,
                       'is_assignment': True,
                       'normal': True,
                       'reading': 'Cargo',
                       'relevant': True,
                       'status': 'UNKNOWN',
                       'typ': 'Int',
                       'value': ''},
           '__rank': 9999},
 'Draft': {'Draft()': {'environmental': False,
                       'is_assignment': True,
                       'normal': True,
                       'reading': 'Draft',
                       'relevant': True,
                       'status': 'UNKNOWN',
                       'typ': 'Int',
                       'value': ''},
           '__rank': 9999},
 'Enter': {'Enter()': {'environmental': False,
                       'is_assignment': False,
                       'normal': True,
                       'reading': 'Enter',
                       'relevant': True,
                       'status': 'UNKNOWN',
                       'typ': 'Bool'},
           '__rank': 9999},
 'Length': {'Length()': {'environmental': False,
                         'is_assignment': True,
                         'normal': True,
                         'reading': 'Length',
                         'relevant': True,
                         'status': 'UNKNOWN',
                         'typ': 'Int',
                         'value': ''},
            '__rank': 9999},
 'Refuel_Area': {'Refuel_Area()': {'environmental': False,
                                   'is_assignment': True,
                                   'normal': True,
                                   'reading': 'Refuel_Area',
                                   'relevant': True,
                                   'status': 'UNKNOWN',
                                   'typ': 'Refuel_Areat_t',
                                   'value': '',
                                   'values': []},
                 '__rank': 9999}}
