
-- original ---------------------------------


vocabulary {
	type seasont_t := { Fall, Summer, Winter, Spring }
	type beveragest_t := { Pinot_Noir, Guiness, Aecht_Schlenkerla_Rauchbier, Water, Bordeaux, Apple_Juice }
	type desiredDisht_t := { Stew, Steak, Roastbeef, Dry_Aged_Gourmet_Steak, Light_Salad_and_a_nice_Steak, Spareribs }
	season: ()→seasont_t
	guestCount: ()→Int
	beverages: ()→beveragest_t
	desiredDish: ()→desiredDisht_t
	guestsWithChildren:() → Bool
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
{'manualPropagation': False,
 'manualRelevance': False,
 'optionalPropagation': False,
 'optionalRelevance': False,
 'symbols': [{'environmental': False,
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
 'beverages': {'beverages()': {'environmental': False,
                               'is_assignment': True,
                               'normal': True,
                               'reading': 'beverages',
                               'relevant': True,
                               'status': 'UNKNOWN',
                               'typ': 'beveragest_t',
                               'values': ['Pinot_Noir',
                                          'Guiness',
                                          'Aecht_Schlenkerla_Rauchbier',
                                          'Water',
                                          'Bordeaux',
                                          'Apple_Juice']}},
 'desiredDish': {'desiredDish()': {'environmental': False,
                                   'is_assignment': True,
                                   'normal': True,
                                   'reading': 'desiredDish',
                                   'relevant': True,
                                   'status': 'UNKNOWN',
                                   'typ': 'desiredDisht_t',
                                   'values': ['Stew',
                                              'Steak',
                                              'Roastbeef',
                                              'Dry_Aged_Gourmet_Steak',
                                              'Light_Salad_and_a_nice_Steak',
                                              'Spareribs']}},
 'guestCount': {'guestCount()': {'environmental': False,
                                 'is_assignment': True,
                                 'normal': True,
                                 'reading': 'guestCount',
                                 'relevant': True,
                                 'status': 'UNKNOWN',
                                 'typ': 'Int'}},
 'guestsWithChildren': {'guestsWithChildren()': {'environmental': False,
                                                 'is_assignment': False,
                                                 'normal': True,
                                                 'reading': 'guestsWithChildren',
                                                 'relevant': True,
                                                 'status': 'UNKNOWN',
                                                 'typ': 'Bool'}},
 'season': {'season()': {'environmental': False,
                         'is_assignment': True,
                         'normal': True,
                         'reading': 'season',
                         'relevant': True,
                         'status': 'UNKNOWN',
                         'typ': 'seasont_t',
                         'values': ['Fall', 'Summer', 'Winter', 'Spring']}}}
