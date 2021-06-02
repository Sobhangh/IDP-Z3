
-- original ---------------------------------


vocabulary {
	type sext_t := { Female, Male }
	type BMILevelt_t := { Severely_Underweight, Normal, Extreme_Obesity, Underweight, Obese_II, Overweight, Obese_I }
	type riskLevelt_t := { Extremely_High, High, Low, Increased, Very_High }
	sex: () →sext_t
	waist: () →Real
	bmi: () →Real
	BMILevel: () →BMILevelt_t
	riskLevel: () →riskLevelt_t
}
theory {
	//BMI Level
	{
		BMILevel() = Severely_Underweight <- bmi() < 18.5 & sex() = Male.
		BMILevel() = Underweight <- bmi() < 18.5 & sex() = Female.
		BMILevel() = Underweight <- 18.5 =< bmi() & bmi() =< 24.9 & sex() = Male.
		BMILevel() = Normal <- 18.5 =< bmi() & bmi() =< 24.9 & sex() = Female.
		BMILevel() = Normal <- 25 =< bmi() & bmi() =< 29.9 & sex() = Male.
		BMILevel() = Overweight <- 25 =< bmi() & bmi() =< 29.9 & sex() = Female.
		BMILevel() = Obese_I <- 30 =< bmi() & bmi() =< 34.9.
		BMILevel() = Obese_II <- 35 =< bmi() & bmi() =< 39.9.
		BMILevel() = Extreme_Obesity <- bmi() >= 40.
	}

	//Determine Risk Level
	{
		riskLevel() = Increased <- BMILevel() = Overweight & sex() = Male & waist() =< 102.
		riskLevel() = High <- BMILevel() = Overweight & sex() = Male & waist() > 102.
		riskLevel() = Increased <- BMILevel() = Overweight & sex() = Female & waist() =< 88.
		riskLevel() = High <- BMILevel() = Overweight & sex() = Female & waist() > 88.
		riskLevel() = High <- BMILevel() = Obese_I & sex() = Male & waist() =< 102.
		riskLevel() = Very_High <- BMILevel() = Obese_I & sex() = Male & waist() > 102.
		riskLevel() = High <- BMILevel() = Obese_I & sex() = Female & waist() =< 88.
		riskLevel() = Very_High <- BMILevel() = Obese_I & sex() = Female & waist() > 88.
		riskLevel() = Very_High <- BMILevel() = Obese_II.
		riskLevel() = Extremely_High <- BMILevel() = Extreme_Obesity.
		riskLevel() = Low <- ~(BMILevel() = Overweight | BMILevel() = Obese_I | BMILevel() = Obese_II | BMILevel() = Extreme_Obesity).
	}

}


structure {
}

-- meta -------------------------------------
{'manualPropagation': False,
 'optionalPropagation': False,
 'symbols': [{'environmental': False,
              'idpname': 'sex',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'waist',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'bmi',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'BMILevel',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'riskLevel',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'active': '{}', 'env_dec': False},
 'BMILevel': {'BMILevel()': {'environmental': False,
                             'is_assignment': True,
                             'normal': True,
                             'reading': 'BMILevel',
                             'relevant': True,
                             'status': 'UNKNOWN',
                             'typ': 'BMILevelt_t',
                             'value': '',
                             'values': []},
              'BMILevel() = Extreme_Obesity': {'environmental': False,
                                               'is_assignment': True,
                                               'normal': False,
                                               'reading': 'BMILevel = Extreme_Obesity',
                                               'relevant': True,
                                               'status': 'UNKNOWN',
                                               'typ': 'Bool'},
              'BMILevel() = Normal': {'environmental': False,
                                      'is_assignment': True,
                                      'normal': False,
                                      'reading': 'BMILevel = Normal',
                                      'relevant': True,
                                      'status': 'UNKNOWN',
                                      'typ': 'Bool'},
              'BMILevel() = Obese_I': {'environmental': False,
                                       'is_assignment': True,
                                       'normal': False,
                                       'reading': 'BMILevel = Obese_I',
                                       'relevant': True,
                                       'status': 'UNKNOWN',
                                       'typ': 'Bool'},
              'BMILevel() = Obese_II': {'environmental': False,
                                        'is_assignment': True,
                                        'normal': False,
                                        'reading': 'BMILevel = Obese_II',
                                        'relevant': True,
                                        'status': 'UNKNOWN',
                                        'typ': 'Bool'},
              'BMILevel() = Overweight': {'environmental': False,
                                          'is_assignment': True,
                                          'normal': False,
                                          'reading': 'BMILevel = Overweight',
                                          'relevant': True,
                                          'status': 'UNKNOWN',
                                          'typ': 'Bool'},
              'BMILevel() = Severely_Underweight': {'environmental': False,
                                                    'is_assignment': True,
                                                    'normal': False,
                                                    'reading': 'BMILevel = Severely_Underweight',
                                                    'relevant': True,
                                                    'status': 'UNKNOWN',
                                                    'typ': 'Bool'},
              'BMILevel() = Underweight': {'environmental': False,
                                           'is_assignment': True,
                                           'normal': False,
                                           'reading': 'BMILevel = Underweight',
                                           'relevant': True,
                                           'status': 'UNKNOWN',
                                           'typ': 'Bool'},
              '__rank': 9999},
 'bmi': {'__rank': 9999,
         'bmi()': {'environmental': False,
                   'is_assignment': True,
                   'normal': True,
                   'reading': 'bmi',
                   'relevant': True,
                   'status': 'UNKNOWN',
                   'typ': 'Real',
                   'value': ''}},
 'riskLevel': {'__rank': 9999,
               'riskLevel()': {'environmental': False,
                               'is_assignment': True,
                               'normal': True,
                               'reading': 'riskLevel',
                               'relevant': True,
                               'status': 'UNKNOWN',
                               'typ': 'riskLevelt_t',
                               'value': '',
                               'values': []},
               'riskLevel() = Extremely_High': {'environmental': False,
                                                'is_assignment': True,
                                                'normal': False,
                                                'reading': 'riskLevel = Extremely_High',
                                                'relevant': True,
                                                'status': 'UNKNOWN',
                                                'typ': 'Bool'},
               'riskLevel() = High': {'environmental': False,
                                      'is_assignment': True,
                                      'normal': False,
                                      'reading': 'riskLevel = High',
                                      'relevant': True,
                                      'status': 'UNKNOWN',
                                      'typ': 'Bool'},
               'riskLevel() = Increased': {'environmental': False,
                                           'is_assignment': True,
                                           'normal': False,
                                           'reading': 'riskLevel = Increased',
                                           'relevant': True,
                                           'status': 'UNKNOWN',
                                           'typ': 'Bool'},
               'riskLevel() = Low': {'environmental': False,
                                     'is_assignment': True,
                                     'normal': False,
                                     'reading': 'riskLevel = Low',
                                     'relevant': True,
                                     'status': 'UNKNOWN',
                                     'typ': 'Bool'},
               'riskLevel() = Very_High': {'environmental': False,
                                           'is_assignment': True,
                                           'normal': False,
                                           'reading': 'riskLevel = Very_High',
                                           'relevant': True,
                                           'status': 'UNKNOWN',
                                           'typ': 'Bool'}},
 'sex': {'__rank': 9999,
         'sex()': {'environmental': False,
                   'is_assignment': True,
                   'normal': True,
                   'reading': 'sex',
                   'relevant': True,
                   'status': 'UNKNOWN',
                   'typ': 'sext_t',
                   'value': '',
                   'values': []},
         'sex() = Female': {'environmental': False,
                            'is_assignment': True,
                            'normal': False,
                            'reading': 'sex = Female',
                            'relevant': True,
                            'status': 'UNKNOWN',
                            'typ': 'Bool'},
         'sex() = Male': {'environmental': False,
                          'is_assignment': True,
                          'normal': False,
                          'reading': 'sex = Male',
                          'relevant': True,
                          'status': 'UNKNOWN',
                          'typ': 'Bool'}},
 'waist': {'__rank': 9999,
           'waist()': {'environmental': False,
                       'is_assignment': True,
                       'normal': True,
                       'reading': 'waist',
                       'relevant': True,
                       'status': 'UNKNOWN',
                       'typ': 'Real',
                       'value': ''}}}
