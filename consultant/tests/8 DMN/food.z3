
-- original ---------------------------------


vocabulary {
	type desiredDisht_t constructed from { Pasta, Stew, Spareribs, Light_salad, Beans_salad, Steak } 
	type seasont_t constructed from { Spring, Summer, Winter } 
	type dayTypet_t constructed from { Holiday, Weekend, Weekday } 
	desiredDish: desiredDisht_t
	season: seasont_t
	temperature: int
	guestCount: int
	dayType: dayTypet_t
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
{'symbols': [{'environmental': False,
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
 'dayType': {'__rank': 9999,
             'dayType': {'environmental': False,
                         'is_assignment': True,
                         'normal': True,
                         'reading': 'dayType',
                         'relevant': False,
                         'status': 'UNKNOWN',
                         'typ': 'dayTypet_t',
                         'value': '',
                         'values': ['Holiday', 'Weekend', 'Weekday']},
             'dayType = Holiday': {'environmental': False,
                                   'is_assignment': True,
                                   'normal': False,
                                   'reading': 'dayType = Holiday',
                                   'relevant': False,
                                   'status': 'UNKNOWN',
                                   'typ': 'Bool'},
             'dayType = Weekday': {'environmental': False,
                                   'is_assignment': True,
                                   'normal': False,
                                   'reading': 'dayType = Weekday',
                                   'relevant': False,
                                   'status': 'UNKNOWN',
                                   'typ': 'Bool'},
             'dayType = Weekend': {'environmental': False,
                                   'is_assignment': True,
                                   'normal': False,
                                   'reading': 'dayType = Weekend',
                                   'relevant': False,
                                   'status': 'UNKNOWN',
                                   'typ': 'Bool'}},
 'desiredDish': {'__rank': 9999,
                 'desiredDish': {'environmental': False,
                                 'is_assignment': True,
                                 'normal': True,
                                 'reading': 'desiredDish',
                                 'relevant': False,
                                 'status': 'UNKNOWN',
                                 'typ': 'desiredDisht_t',
                                 'value': '',
                                 'values': ['Pasta', 'Stew', 'Spareribs', 'Light_salad', 'Beans_salad', 'Steak']},
                 'desiredDish = Beans_salad': {'environmental': False,
                                               'is_assignment': True,
                                               'normal': False,
                                               'reading': 'desiredDish = Beans_salad',
                                               'relevant': False,
                                               'status': 'UNKNOWN',
                                               'typ': 'Bool'},
                 'desiredDish = Light_salad': {'environmental': False,
                                               'is_assignment': True,
                                               'normal': False,
                                               'reading': 'desiredDish = Light_salad',
                                               'relevant': False,
                                               'status': 'UNKNOWN',
                                               'typ': 'Bool'},
                 'desiredDish = Pasta': {'environmental': False,
                                         'is_assignment': True,
                                         'normal': False,
                                         'reading': 'desiredDish = Pasta',
                                         'relevant': False,
                                         'status': 'UNKNOWN',
                                         'typ': 'Bool'},
                 'desiredDish = Spareribs': {'environmental': False,
                                             'is_assignment': True,
                                             'normal': False,
                                             'reading': 'desiredDish = Spareribs',
                                             'relevant': False,
                                             'status': 'UNKNOWN',
                                             'typ': 'Bool'},
                 'desiredDish = Steak': {'environmental': False,
                                         'is_assignment': True,
                                         'normal': False,
                                         'reading': 'desiredDish = Steak',
                                         'relevant': False,
                                         'status': 'UNKNOWN',
                                         'typ': 'Bool'},
                 'desiredDish = Stew': {'environmental': False,
                                        'is_assignment': True,
                                        'normal': False,
                                        'reading': 'desiredDish = Stew',
                                        'relevant': False,
                                        'status': 'UNKNOWN',
                                        'typ': 'Bool'}},
 'guestCount': {'__rank': 9999,
                'guestCount': {'environmental': False,
                               'is_assignment': True,
                               'normal': True,
                               'reading': 'guestCount',
                               'relevant': False,
                               'status': 'UNKNOWN',
                               'typ': 'Int',
                               'value': ''}},
 'season': {'__rank': 9999,
            'season': {'environmental': False,
                       'is_assignment': True,
                       'normal': True,
                       'reading': 'season',
                       'relevant': False,
                       'status': 'UNKNOWN',
                       'typ': 'seasont_t',
                       'value': '',
                       'values': ['Spring', 'Summer', 'Winter']},
            'season = Spring': {'environmental': False,
                                'is_assignment': True,
                                'normal': False,
                                'reading': 'season = Spring',
                                'relevant': False,
                                'status': 'UNKNOWN',
                                'typ': 'Bool'},
            'season = Summer': {'environmental': False,
                                'is_assignment': True,
                                'normal': False,
                                'reading': 'season = Summer',
                                'relevant': False,
                                'status': 'UNKNOWN',
                                'typ': 'Bool'},
            'season = Winter': {'environmental': False,
                                'is_assignment': True,
                                'normal': False,
                                'reading': 'season = Winter',
                                'relevant': False,
                                'status': 'UNKNOWN',
                                'typ': 'Bool'}},
 'temperature': {'__rank': 9999,
                 'temperature': {'environmental': False,
                                 'is_assignment': True,
                                 'normal': True,
                                 'reading': 'temperature',
                                 'relevant': False,
                                 'status': 'UNKNOWN',
                                 'typ': 'Int',
                                 'value': ''}}}
