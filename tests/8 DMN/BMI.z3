
-- original ---------------------------------


vocabulary {
    type BMILevelt_t := { Obese_II, Obese_I, Normal, Severely_Underweight, Underweight, Overweight, Extreme_Obesity }
    type sext_t := { Male, Female }
    type riskLevelt_t := { High, Very_High, Low, Increased, Extremely_High }
    bmi: ()→Real
    length: ()→Real
    BMILevel: ()→BMILevelt_t
    sex: ()→sext_t
    riskLevel: ()→riskLevelt_t
    waist: ()→Real
    weight: ()→Real
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

    //BMI
    {
        bmi() = weight()/(length() * length()) <- true.
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
              'idpname': 'bmi',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'length',
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
              'idpname': 'sex',
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
              'idpname': 'waist',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'weight',
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
 'length': {'__rank': 9999,
            'length()': {'environmental': False,
                         'is_assignment': True,
                         'normal': True,
                         'reading': 'length',
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
                               'values': []}},
 'sex': {'__rank': 9999,
         'sex()': {'environmental': False,
                   'is_assignment': True,
                   'normal': True,
                   'reading': 'sex',
                   'relevant': True,
                   'status': 'UNKNOWN',
                   'typ': 'sext_t',
                   'value': '',
                   'values': []}},
 'waist': {'__rank': 9999,
           'waist()': {'environmental': False,
                       'is_assignment': True,
                       'normal': True,
                       'reading': 'waist',
                       'relevant': True,
                       'status': 'UNKNOWN',
                       'typ': 'Real',
                       'value': ''}},
 'weight': {'__rank': 9999,
            'weight()': {'environmental': False,
                         'is_assignment': True,
                         'normal': True,
                         'reading': 'weight',
                         'relevant': True,
                         'status': 'UNKNOWN',
                         'typ': 'Real',
                         'value': ''}}}
