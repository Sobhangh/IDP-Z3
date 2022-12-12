
-- original ---------------------------------


vocabulary {
	type desiredDisht_t := { Pasta, Stew, Spareribs, Light_salad, Beans_salad, Steak }
	type seasont_t := { Spring, Summer, Winter }
	type dayTypet_t := { Holiday, Weekend, Weekday }
	desiredDish: ()→desiredDisht_t
	season: ()→seasont_t
	temperature: ()→Int
	guestCount: ()→Int
	dayType: ()→dayTypet_t
}
theory {
	//Dish Decision
	{
		desiredDish() = Spareribs <- season() = Winter & guestCount() =< 8.
		desiredDish() = Pasta <- season() = Winter & guestCount() > 8.
		desiredDish() = Light_salad <- season() = Summer & guestCount() > 10.
		desiredDish() = Beans_salad <- season() = Summer & guestCount() =< 10.
		desiredDish() = Stew <- season() = Spring & guestCount() < 10.
		desiredDish() = Steak <- season() = Spring & guestCount() >= 10.
	}

	//Season decision
	{
		season() = Summer <- temperature() > 30.
		season() = Winter <- temperature() < 10.
		season() = Spring <- 10 =< temperature() & temperature() =< 30.
	}

	//Guest Count
	{
		guestCount() = 4 <- dayType() = Weekday.
		guestCount() = 10 <- dayType() = Holiday.
		guestCount() = 15 <- dayType() = Weekend.
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
              'idpname': 'desiredDish',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'season',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'temperature',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'guestCount',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'dayType',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'dayType': {'dayType()': {'environmental': False,
                           'is_assignment': True,
                           'normal': True,
                           'reading': 'dayType',
                           'relevant': True,
                           'status': 'UNKNOWN',
                           'typ': 'dayTypet_t',
                           'values': ['Holiday', 'Weekend', 'Weekday']}},
 'desiredDish': {'desiredDish()': {'environmental': False,
                                   'is_assignment': True,
                                   'normal': True,
                                   'reading': 'desiredDish',
                                   'relevant': True,
                                   'status': 'UNKNOWN',
                                   'typ': 'desiredDisht_t',
                                   'values': ['Pasta', 'Stew', 'Spareribs', 'Light_salad', 'Beans_salad', 'Steak']}},
 'guestCount': {'guestCount()': {'environmental': False,
                                 'is_assignment': True,
                                 'normal': True,
                                 'reading': 'guestCount',
                                 'relevant': True,
                                 'status': 'UNKNOWN',
                                 'typ': 'Int'}},
 'season': {'season()': {'environmental': False,
                         'is_assignment': True,
                         'normal': True,
                         'reading': 'season',
                         'relevant': True,
                         'status': 'UNKNOWN',
                         'typ': 'seasont_t',
                         'values': ['Spring', 'Summer', 'Winter']}},
 'temperature': {'temperature()': {'environmental': False,
                                   'is_assignment': True,
                                   'normal': True,
                                   'reading': 'temperature',
                                   'relevant': True,
                                   'status': 'UNKNOWN',
                                   'typ': 'Int'}}}
