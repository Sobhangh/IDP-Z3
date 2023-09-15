
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
 'manualRelevance': False,
 'optionalPropagation': False,
 'optionalRelevance': False,
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
              'idpname': 'riskLevel',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'BMILevel',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'BMILevel': {'BMILevel()': {'environmental': False,
                             'is_assignment': True,
                             'normal': True,
                             'reading': 'BMILevel',
                             'relevant': True,
                             'status': 'UNKNOWN',
                             'typ': 'BMILevelt_t',
                             'values': ['Severely_Underweight',
                                        'Normal',
                                        'Extreme_Obesity',
                                        'Underweight',
                                        'Obese_II',
                                        'Overweight',
                                        'Obese_I']}},
 'bmi': {'bmi()': {'environmental': False,
                   'is_assignment': True,
                   'normal': True,
                   'reading': 'bmi',
                   'relevant': True,
                   'status': 'UNKNOWN',
                   'typ': 'Real'}},
 'riskLevel': {'riskLevel()': {'environmental': False,
                               'is_assignment': True,
                               'normal': True,
                               'reading': 'riskLevel',
                               'relevant': True,
                               'status': 'UNKNOWN',
                               'typ': 'riskLevelt_t',
                               'values': ['Extremely_High', 'High', 'Low', 'Increased', 'Very_High']}},
 'sex': {'sex()': {'environmental': False,
                   'is_assignment': True,
                   'normal': True,
                   'reading': 'sex',
                   'relevant': True,
                   'status': 'UNKNOWN',
                   'typ': 'sext_t',
                   'values': ['Female', 'Male']}},
 'waist': {'waist()': {'environmental': False,
                       'is_assignment': True,
                       'normal': True,
                       'reading': 'waist',
                       'relevant': True,
                       'status': 'UNKNOWN',
                       'typ': 'Real'}}}
