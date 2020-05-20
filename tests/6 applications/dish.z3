
-- original ---------------------------------


vocabulary {
	type desiredDish_t constructed from { Stew, Spareribs, Beans_salad, Steak, Light_salad, Pasta } 
	type season_t constructed from { Spring, Winter, Summer } 
	type dayType_t constructed from { Weekday, Holiday, Weekend } 
	temperature: real
	desiredDish: desiredDish_t
	season: season_t
	dayType: dayType_t
	guestCount: real
}
theory {
	//dishDecisionTable
	{
		desiredDish = Spareribs <- season = Winter & guestCount =< 08.
		desiredDish = Pasta <- season = Winter & guestCount > 08.
		desiredDish = Light_salad <- season = Summer & guestCount > 10.
		desiredDish = Beans_salad <- season = Summer & guestCount =< 10.
		desiredDish = Stew <- season = Spring & guestCount < 10.
		desiredDish = Steak <- season = Spring & guestCount >= 10.
	}

	//seasonDecisionTable
	{
		season = Summer <- temperature > 30.
		season = Winter <- temperature < 10.
		season = Spring <- 10 =< temperature & temperature =< 30.
	}

	//guestCountDecisionTable
	{
		guestCount = 04 <- dayType = Weekday.
		guestCount = 10 <- dayType = Holiday.
		guestCount = 15 <- dayType = Weekend.
	}

}


structure {
}

-- vocabulary -------------------------------

-- theory -----------------------------------
Or(desiredDish == Stew,
   desiredDish == Spareribs,
   desiredDish == Beans_salad,
   desiredDish == Steak,
   desiredDish == Light_salad,
   desiredDish == Pasta)

Or(season == Spring, season == Winter, season == Summer)

Or(dayType == Weekday,
   dayType == Holiday,
   dayType == Weekend)

And((desiredDish == Stew) ==
    And(season == Spring, guestCount < 10),
    (desiredDish == Spareribs) ==
    And(season == Winter, guestCount <= 8),
    (desiredDish == Beans_salad) ==
    And(season == Summer, guestCount <= 10),
    (desiredDish == Steak) ==
    And(season == Spring, guestCount >= 10),
    (desiredDish == Light_salad) ==
    And(season == Summer, guestCount > 10),
    (desiredDish == Pasta) ==
    And(season == Winter, guestCount > 8))

And((season == Spring) ==
    And(temperature >= 10, temperature <= 30),
    (season == Winter) == (temperature < 10),
    (season == Summer) == (temperature > 30))

ForAll(c!111,
       (guestCount == c!111) ==
       Or(And(c!111 == 4, dayType == Weekday),
          And(c!111 == 10, dayType == Holiday),
          And(c!111 == 15, dayType == Weekend)))

-- subtences ------------------------------------
desiredDish = Stew
desiredDish = Spareribs
desiredDish = Beans_salad
desiredDish = Steak
desiredDish = Light_salad
desiredDish = Pasta
season = Spring
season = Winter
season = Summer
dayType = Weekday
dayType = Holiday
dayType = Weekend

-- GUILines ------------------------------------
temperature
desiredDish
season
dayType
guestCount
desiredDish = Stew
desiredDish = Spareribs
desiredDish = Beans_salad
desiredDish = Steak
desiredDish = Light_salad
desiredDish = Pasta
season = Spring
season = Winter
season = Summer
dayType = Weekday
dayType = Holiday
dayType = Weekend

-- case -------------------------------------
Type:        
  
Definitions: 
  Rule:∀$desiredDish$[desiredDish_t]: desiredDish($desiredDish$) ⇔$desiredDish$ = Spareribs ∧ (season = Winter ∧ guestCount ≤ 08) ∨ $desiredDish$ = Pasta ∧ (season = Winter ∧ guestCount > 08) ∨ $desiredDish$ = Light_salad ∧ (season = Summer ∧ guestCount > 10) ∨ $desiredDish$ = Beans_salad ∧ (season = Summer ∧ guestCount ≤ 10) ∨ $desiredDish$ = Stew ∧ (season = Spring ∧ guestCount < 10) ∨ $desiredDish$ = Steak ∧ (season = Spring ∧ guestCount ≥ 10)
  Rule:∀$season$[season_t]: season($season$) ⇔$season$ = Summer ∧ temperature > 30 ∨ $season$ = Winter ∧ temperature < 10 ∨ $season$ = Spring ∧ (10 ≤ temperature ∧ temperature ≤ 30)
  Rule:∀$guestCount$[real]: guestCount($guestCount$) ⇔$guestCount$ = 04 ∧ dayType = Weekday ∨ $guestCount$ = 10 ∧ dayType = Holiday ∨ $guestCount$ = 15 ∧ dayType = Weekend
Universals:  
  
Consequences:
  
Simplified:  
  
Irrelevant:  
  ? temperature
  ? desiredDish
  ? season
  ? dayType
  ? guestCount
  ? desiredDish = Stew
  ? desiredDish = Spareribs
  ? desiredDish = Beans_salad
  ? desiredDish = Steak
  ? desiredDish = Light_salad
  ? desiredDish = Pasta
  ? season = Spring
  ? season = Winter
  ? season = Summer
  ? dayType = Weekday
  ? dayType = Holiday
  ? dayType = Weekend
Co-constraints:
  


-- meta -------------------------------------
{'symbols': [{'idpname': 'temperature', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'normal'},
             {'idpname': 'desiredDish', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'normal'},
             {'idpname': 'season', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'normal'},
             {'idpname': 'dayType', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'normal'},
             {'idpname': 'guestCount', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'dayType': {'__rank': 9999,
             'dayType': {'environmental': False,
                         'normal': True,
                         'reading': 'dayType',
                         'relevant': False,
                         'status': 'UNKNOWN',
                         'typ': 'dayType_t',
                         'value': '',
                         'values': ['Weekday', 'Holiday', 'Weekend']},
             'dayType = Holiday': {'environmental': False,
                                   'normal': False,
                                   'reading': 'dayType = Holiday',
                                   'relevant': False,
                                   'status': 'UNKNOWN',
                                   'typ': 'Bool'},
             'dayType = Weekday': {'environmental': False,
                                   'normal': False,
                                   'reading': 'dayType = Weekday',
                                   'relevant': False,
                                   'status': 'UNKNOWN',
                                   'typ': 'Bool'},
             'dayType = Weekend': {'environmental': False,
                                   'normal': False,
                                   'reading': 'dayType = Weekend',
                                   'relevant': False,
                                   'status': 'UNKNOWN',
                                   'typ': 'Bool'}},
 'desiredDish': {'__rank': 9999,
                 'desiredDish': {'environmental': False,
                                 'normal': True,
                                 'reading': 'desiredDish',
                                 'relevant': False,
                                 'status': 'UNKNOWN',
                                 'typ': 'desiredDish_t',
                                 'value': '',
                                 'values': ['Stew', 'Spareribs', 'Beans_salad', 'Steak', 'Light_salad', 'Pasta']},
                 'desiredDish = Beans_salad': {'environmental': False,
                                               'normal': False,
                                               'reading': 'desiredDish = Beans_salad',
                                               'relevant': False,
                                               'status': 'UNKNOWN',
                                               'typ': 'Bool'},
                 'desiredDish = Light_salad': {'environmental': False,
                                               'normal': False,
                                               'reading': 'desiredDish = Light_salad',
                                               'relevant': False,
                                               'status': 'UNKNOWN',
                                               'typ': 'Bool'},
                 'desiredDish = Pasta': {'environmental': False,
                                         'normal': False,
                                         'reading': 'desiredDish = Pasta',
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
                               'typ': 'Real',
                               'value': ''}},
 'season': {'__rank': 9999,
            'season': {'environmental': False,
                       'normal': True,
                       'reading': 'season',
                       'relevant': False,
                       'status': 'UNKNOWN',
                       'typ': 'season_t',
                       'value': '',
                       'values': ['Spring', 'Winter', 'Summer']},
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
                                'typ': 'Bool'}},
 'temperature': {'__rank': 9999,
                 'temperature': {'environmental': False,
                                 'normal': True,
                                 'reading': 'temperature',
                                 'relevant': False,
                                 'status': 'UNKNOWN',
                                 'typ': 'Real',
                                 'value': ''}}}
