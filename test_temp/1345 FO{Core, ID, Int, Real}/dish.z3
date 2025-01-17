
-- original ---------------------------------


vocabulary {
	type desiredDish_t := { Stew, Spareribs, Beans_salad, Steak, Light_salad, Pasta }
	type season_t := { Spring, Winter, Summer }
	type dayType_t := { Weekday, Holiday, Weekend }
	temperature: ()→Real
	desiredDish: ()→desiredDish_t
	season: ()→season_t
	dayType: ()→dayType_t
	guestCount: ()→Real
}
theory {
	//dishDecisionTable
	{
		desiredDish() = Spareribs <- season() = Winter & guestCount() =< 08.
		desiredDish() = Pasta <- season() = Winter & guestCount() > 08.
		desiredDish() = Light_salad <- season() = Summer & guestCount() > 10.
		desiredDish() = Beans_salad <- season() = Summer & guestCount() =< 10.
		desiredDish() = Stew <- season() = Spring & guestCount() < 10.
		desiredDish() = Steak <- season() = Spring & guestCount() >= 10.
	}

	//seasonDecisionTable
	{
		season() = Summer <- temperature() > 30.
		season() = Winter <- temperature() < 10.
		season() = Spring <- 10 =< temperature() & temperature() =< 30.
	}

	//guestCountDecisionTable
	{
		guestCount() = 04 <- dayType() = Weekday.
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
              'idpname': 'temperature',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
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
              'idpname': 'dayType',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'guestCount',
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
                           'typ': 'dayType_t',
                           'values': ['Weekday', 'Holiday', 'Weekend']}},
 'desiredDish': {'desiredDish()': {'environmental': False,
                                   'is_assignment': True,
                                   'normal': True,
                                   'reading': 'desiredDish',
                                   'relevant': True,
                                   'status': 'UNKNOWN',
                                   'typ': 'desiredDish_t',
                                   'values': ['Stew', 'Spareribs', 'Beans_salad', 'Steak', 'Light_salad', 'Pasta']}},
 'guestCount': {'guestCount()': {'environmental': False,
                                 'is_assignment': True,
                                 'normal': True,
                                 'reading': 'guestCount',
                                 'relevant': True,
                                 'status': 'UNKNOWN',
                                 'typ': 'Real'}},
 'season': {'season()': {'environmental': False,
                         'is_assignment': True,
                         'normal': True,
                         'reading': 'season',
                         'relevant': True,
                         'status': 'UNKNOWN',
                         'typ': 'season_t',
                         'values': ['Spring', 'Winter', 'Summer']}},
 'temperature': {'temperature()': {'environmental': False,
                                   'is_assignment': True,
                                   'normal': True,
                                   'reading': 'temperature',
                                   'relevant': True,
                                   'status': 'UNKNOWN',
                                   'typ': 'Real'}}}
