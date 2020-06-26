
-- original ---------------------------------


vocabulary {
	type seasont_t constructed from { Fall, Summer, Winter, Spring } 
	type beveragest_t constructed from { Pinot_Noir, Guiness, Aecht_Schlenkerla_Rauchbier, Water, Bordeaux, Apple_Juice } 
	type desiredDisht_t constructed from { Stew, Steak, Roastbeef, Dry_Aged_Gourmet_Steak, Light_Salad_and_a_nice_Steak, Spareribs } 
	season: seasont_t
	guestCount: int
	beverages: beveragest_t
	desiredDish: desiredDisht_t
	guestsWithChildren
}
theory {
	//Beverages
	{
		beverages() = Aecht_Schlenkerla_Rauchbier <- desiredDish() = Spareribs & guestsWithChildren().
		beverages() = Guiness <- desiredDish() = Stew & guestsWithChildren().
		beverages() = Bordeaux <- desiredDish() = Roastbeef & guestsWithChildren().
		beverages() = Pinot_Noir <- desiredDish() = Steak & guestsWithChildren().
		beverages() = Apple_Juice <- guestsWithChildren().
		beverages() = Water <- ~(guestsWithChildren()).
	}

	//Dish
	{
		desiredDish() = Spareribs <- season() = Fall & guestCount() =< 8.
		desiredDish() = Roastbeef <- season() = Winter & guestCount() =< 8.
		desiredDish() = Dry_Aged_Gourmet_Steak <- season() = Spring & guestCount() =< 4.
		desiredDish() = Steak <- season() = Spring & 5 =< guestCount() & guestCount() =< 8.
		desiredDish() = Stew <- season() = Fall & guestCount() > 8.
		desiredDish() = Light_Salad_and_a_nice_Steak <- season() = Summer.
	}

}


structure {
}

-- meta -------------------------------------
{'symbols': [{'environmental': False,
              'idpname': 'season',
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
              'idpname': 'beverages',
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
              'idpname': 'guestsWithChildren',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'beverages': {'__rank': 9999,
               'beverages': {'environmental': False,
                             'normal': True,
                             'reading': 'beverages',
                             'relevant': False,
                             'status': 'UNKNOWN',
                             'typ': 'beveragest_t',
                             'value': '',
                             'values': ['Pinot_Noir',
                                        'Guiness',
                                        'Aecht_Schlenkerla_Rauchbier',
                                        'Water',
                                        'Bordeaux',
                                        'Apple_Juice']},
               'beverages = Aecht_Schlenkerla_Rauchbier': {'environmental': False,
                                                           'normal': False,
                                                           'reading': 'beverages = Aecht_Schlenkerla_Rauchbier',
                                                           'relevant': False,
                                                           'status': 'CONSEQUENCE',
                                                           'typ': 'Bool',
                                                           'value': False},
               'beverages = Apple_Juice': {'environmental': False,
                                           'normal': False,
                                           'reading': 'beverages = Apple_Juice',
                                           'relevant': False,
                                           'status': 'UNKNOWN',
                                           'typ': 'Bool'},
               'beverages = Bordeaux': {'environmental': False,
                                        'normal': False,
                                        'reading': 'beverages = Bordeaux',
                                        'relevant': False,
                                        'status': 'CONSEQUENCE',
                                        'typ': 'Bool',
                                        'value': False},
               'beverages = Guiness': {'environmental': False,
                                       'normal': False,
                                       'reading': 'beverages = Guiness',
                                       'relevant': False,
                                       'status': 'CONSEQUENCE',
                                       'typ': 'Bool',
                                       'value': False},
               'beverages = Pinot_Noir': {'environmental': False,
                                          'normal': False,
                                          'reading': 'beverages = Pinot_Noir',
                                          'relevant': False,
                                          'status': 'CONSEQUENCE',
                                          'typ': 'Bool',
                                          'value': False},
               'beverages = Water': {'environmental': False,
                                     'normal': False,
                                     'reading': 'beverages = Water',
                                     'relevant': False,
                                     'status': 'UNKNOWN',
                                     'typ': 'Bool'}},
 'desiredDish': {'__rank': 9999,
                 'desiredDish': {'environmental': False,
                                 'normal': True,
                                 'reading': 'desiredDish',
                                 'relevant': False,
                                 'status': 'UNKNOWN',
                                 'typ': 'desiredDisht_t',
                                 'value': '',
                                 'values': ['Stew',
                                            'Steak',
                                            'Roastbeef',
                                            'Dry_Aged_Gourmet_Steak',
                                            'Light_Salad_and_a_nice_Steak',
                                            'Spareribs']},
                 'desiredDish = Dry_Aged_Gourmet_Steak': {'environmental': False,
                                                          'normal': False,
                                                          'reading': 'desiredDish = Dry_Aged_Gourmet_Steak',
                                                          'relevant': False,
                                                          'status': 'UNKNOWN',
                                                          'typ': 'Bool'},
                 'desiredDish = Light_Salad_and_a_nice_Steak': {'environmental': False,
                                                                'normal': False,
                                                                'reading': 'desiredDish = Light_Salad_and_a_nice_Steak',
                                                                'relevant': False,
                                                                'status': 'UNKNOWN',
                                                                'typ': 'Bool'},
                 'desiredDish = Roastbeef': {'environmental': False,
                                             'normal': False,
                                             'reading': 'desiredDish = Roastbeef',
                                             'relevant': False,
                                             'status': 'UNKNOWN',
                                             'typ': 'Bool'},
                 'desiredDish = Spareribs': {'environmental': False,
                                             'normal': False,
                                             'reading': 'desiredDish = Spareribs',
                                             'relevant': False,
                                             'status': 'UNKNOWN',
                                             'typ': 'Bool'},
                 'desiredDish = Steak': {'environmental': False,
                                         'normal': False,
                                         'reading': 'desiredDish = Steak',
                                         'relevant': False,
                                         'status': 'UNKNOWN',
                                         'typ': 'Bool'},
                 'desiredDish = Stew': {'environmental': False,
                                        'normal': False,
                                        'reading': 'desiredDish = Stew',
                                        'relevant': False,
                                        'status': 'UNKNOWN',
                                        'typ': 'Bool'}},
 'guestCount': {'__rank': 9999,
                'guestCount': {'environmental': False,
                               'normal': True,
                               'reading': 'guestCount',
                               'relevant': False,
                               'status': 'UNKNOWN',
                               'typ': 'Int',
                               'value': ''}},
 'guestsWithChildren': {'__rank': 9999,
                        'guestsWithChildren': {'environmental': False,
                                               'normal': True,
                                               'reading': 'guestsWithChildren',
                                               'relevant': False,
                                               'status': 'UNKNOWN',
                                               'typ': 'Bool'}},
 'season': {'__rank': 9999,
            'season': {'environmental': False,
                       'normal': True,
                       'reading': 'season',
                       'relevant': False,
                       'status': 'UNKNOWN',
                       'typ': 'seasont_t',
                       'value': '',
                       'values': ['Fall', 'Summer', 'Winter', 'Spring']},
            'season = Fall': {'environmental': False,
                              'normal': False,
                              'reading': 'season = Fall',
                              'relevant': False,
                              'status': 'UNKNOWN',
                              'typ': 'Bool'},
            'season = Spring': {'environmental': False,
                                'normal': False,
                                'reading': 'season = Spring',
                                'relevant': False,
                                'status': 'UNKNOWN',
                                'typ': 'Bool'},
            'season = Summer': {'environmental': False,
                                'normal': False,
                                'reading': 'season = Summer',
                                'relevant': False,
                                'status': 'UNKNOWN',
                                'typ': 'Bool'},
            'season = Winter': {'environmental': False,
                                'normal': False,
                                'reading': 'season = Winter',
                                'relevant': False,
                                'status': 'UNKNOWN',
                                'typ': 'Bool'}}}
