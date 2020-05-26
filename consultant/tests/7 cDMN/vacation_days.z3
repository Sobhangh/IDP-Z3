
-- original ---------------------------------
// https://dmcommunity.wordpress.com/challenge/challenge-jan-2016/

vocabulary {
	type Vacation_Days_t = { 0..100 } 
	type Age_t = { 0..100 } 
	type Service_Years_t = { 0..100 } 
	type Employee_t constructed from { Huey, Dewey, Louie, Donald } 
	Vacation_Days(Employee_t): Vacation_Days_t
	Age(Employee_t): Age_t
	Service_Years(Employee_t): Service_Years_t
}
theory {
	//Vacation days of employee
	!Employee[Employee_t]: Vacation_Days(Employee)  = sum{  : Employee = Employee: 22 }+sum{  : Age(Employee) < 18 & Employee = Employee: 05 }+sum{  : Age(Employee) >= 60 & Employee = Employee: 05 }+sum{  : 18 =< Age(Employee) & Age(Employee) < 60 & Service_Years(Employee) >= 30 & Employee = Employee: 05 }+sum{  : Service_Years(Employee) >= 30 & Employee = Employee: 03 }+sum{  : Age(Employee) < 60 & Service_Years(Employee) < 30 & Employee = Employee: 03 }+sum{  : Age(Employee) < 45 & 15 =< Service_Years(Employee) & Service_Years(Employee) < 30 & Employee = Employee: 02 }+sum{  : 45 =< Age(Employee) & Age(Employee) < 60 & Service_Years(Employee) < 30 & Employee = Employee: 02 }.
}


structure {
	Age = {Huey, 17; Dewey, 70; Louie, 35; Donald, 46; } else 46 
	Service_Years = {Huey, 1; Dewey, 31; Louie, 16; Donald, 10; } else 10 
}

-- vocabulary -------------------------------

-- theory -----------------------------------
And(Vacation_Days(Huey) == 30,
    Vacation_Days(Dewey) == 30,
    Vacation_Days(Louie) == 27,
    Vacation_Days(Donald) == 27)

And(Vacation_Days(Huey) >= 0, Vacation_Days(Huey) <= 100)

And(Vacation_Days(Dewey) >= 0, Vacation_Days(Dewey) <= 100)

And(Vacation_Days(Louie) >= 0, Vacation_Days(Louie) <= 100)

And(Vacation_Days(Donald) >= 0,
    Vacation_Days(Donald) <= 100)

And(Age(Huey) >= 0, Age(Huey) <= 100)

And(Age(Dewey) >= 0, Age(Dewey) <= 100)

And(Age(Louie) >= 0, Age(Louie) <= 100)

And(Age(Donald) >= 0, Age(Donald) <= 100)

And(Service_Years(Huey) >= 0, Service_Years(Huey) <= 100)

And(Service_Years(Dewey) >= 0, Service_Years(Dewey) <= 100)

And(Service_Years(Louie) >= 0, Service_Years(Louie) <= 100)

And(Service_Years(Donald) >= 0,
    Service_Years(Donald) <= 100)

-- subtences ------------------------------------
∀Employee[Employee_t] : Vacation_Days(Employee) = sum{ : Employee = Employee : 22} + sum{ : Age(Employee) < 18 ∧ Employee = Employee : 05} + sum{ : Age(Employee) ≥ 60 ∧ Employee = Employee : 05} + sum{ : 18 ≤ Age(Employee) ∧ Age(Employee) < 60 ∧ Service_Years(Employee) ≥ 30 ∧ Employee = Employee : 05} + sum{ : Service_Years(Employee) ≥ 30 ∧ Employee = Employee : 03} + sum{ : Age(Employee) < 60 ∧ Service_Years(Employee) < 30 ∧ Employee = Employee : 03} + sum{ : Age(Employee) < 45 ∧ 15 ≤ Service_Years(Employee) ∧ Service_Years(Employee) < 30 ∧ Employee = Employee : 02} + sum{ : 45 ≤ Age(Employee) ∧ Age(Employee) < 60 ∧ Service_Years(Employee) < 30 ∧ Employee = Employee : 02}
0 ≤ Vacation_Days(Huey) ≤ 100
0 ≤ Vacation_Days(Dewey) ≤ 100
0 ≤ Vacation_Days(Louie) ≤ 100
0 ≤ Vacation_Days(Donald) ≤ 100
0 ≤ Age(Huey) ≤ 100
0 ≤ Age(Dewey) ≤ 100
0 ≤ Age(Louie) ≤ 100
0 ≤ Age(Donald) ≤ 100
0 ≤ Service_Years(Huey) ≤ 100
0 ≤ Service_Years(Dewey) ≤ 100
0 ≤ Service_Years(Louie) ≤ 100
0 ≤ Service_Years(Donald) ≤ 100

-- GUILines ------------------------------------
Vacation_Days(Huey)
Vacation_Days(Dewey)
Vacation_Days(Louie)
Vacation_Days(Donald)
∀Employee[Employee_t] : Vacation_Days(Employee) = sum{ : Employee = Employee : 22} + sum{ : Age(Employee) < 18 ∧ Employee = Employee : 05} + sum{ : Age(Employee) ≥ 60 ∧ Employee = Employee : 05} + sum{ : 18 ≤ Age(Employee) ∧ Age(Employee) < 60 ∧ Service_Years(Employee) ≥ 30 ∧ Employee = Employee : 05} + sum{ : Service_Years(Employee) ≥ 30 ∧ Employee = Employee : 03} + sum{ : Age(Employee) < 60 ∧ Service_Years(Employee) < 30 ∧ Employee = Employee : 03} + sum{ : Age(Employee) < 45 ∧ 15 ≤ Service_Years(Employee) ∧ Service_Years(Employee) < 30 ∧ Employee = Employee : 02} + sum{ : 45 ≤ Age(Employee) ∧ Age(Employee) < 60 ∧ Service_Years(Employee) < 30 ∧ Employee = Employee : 02}
0 ≤ Vacation_Days(Huey) ≤ 100
0 ≤ Vacation_Days(Dewey) ≤ 100
0 ≤ Vacation_Days(Louie) ≤ 100
0 ≤ Vacation_Days(Donald) ≤ 100
0 ≤ Age(Huey) ≤ 100
0 ≤ Age(Dewey) ≤ 100
0 ≤ Age(Louie) ≤ 100
0 ≤ Age(Donald) ≤ 100
0 ≤ Service_Years(Huey) ≤ 100
0 ≤ Service_Years(Dewey) ≤ 100
0 ≤ Service_Years(Louie) ≤ 100
0 ≤ Service_Years(Donald) ≤ 100

-- case -------------------------------------
Type:        
  
Definitions: 
  
Universals:  
  Vacation_Days(Huey) -> 30
  Vacation_Days(Dewey) -> 30
  Vacation_Days(Louie) -> 27
  Vacation_Days(Donald) -> 27
  ∀Employee[Employee_t] : Vacation_Days(Employee) = sum{ : Employee = Employee : 22} + sum{ : Age(Employee) < 18 ∧ Employee = Employee : 05} + sum{ : Age(Employee) ≥ 60 ∧ Employee = Employee : 05} + sum{ : 18 ≤ Age(Employee) ∧ Age(Employee) < 60 ∧ Service_Years(Employee) ≥ 30 ∧ Employee = Employee : 05} + sum{ : Service_Years(Employee) ≥ 30 ∧ Employee = Employee : 03} + sum{ : Age(Employee) < 60 ∧ Service_Years(Employee) < 30 ∧ Employee = Employee : 03} + sum{ : Age(Employee) < 45 ∧ 15 ≤ Service_Years(Employee) ∧ Service_Years(Employee) < 30 ∧ Employee = Employee : 02} + sum{ : 45 ≤ Age(Employee) ∧ Age(Employee) < 60 ∧ Service_Years(Employee) < 30 ∧ Employee = Employee : 02}
  0 ≤ Vacation_Days(Huey) ≤ 100
  0 ≤ Vacation_Days(Dewey) ≤ 100
  0 ≤ Vacation_Days(Louie) ≤ 100
  0 ≤ Vacation_Days(Donald) ≤ 100
  0 ≤ Age(Huey) ≤ 100
  0 ≤ Age(Dewey) ≤ 100
  0 ≤ Age(Louie) ≤ 100
  0 ≤ Age(Donald) ≤ 100
  0 ≤ Service_Years(Huey) ≤ 100
  0 ≤ Service_Years(Dewey) ≤ 100
  0 ≤ Service_Years(Louie) ≤ 100
  0 ≤ Service_Years(Donald) ≤ 100
Consequences:
  
Simplified:  
  ∀ : true
  0 ≤ 30 ≤ 100
  0 ≤ 30 ≤ 100
  0 ≤ 27 ≤ 100
  0 ≤ 27 ≤ 100
Irrelevant:  
  0 ≤ Age(Huey) ≤ 100
  0 ≤ Age(Dewey) ≤ 100
  0 ≤ Age(Louie) ≤ 100
  0 ≤ Age(Donald) ≤ 100
  0 ≤ Service_Years(Huey) ≤ 100
  0 ≤ Service_Years(Dewey) ≤ 100
  0 ≤ Service_Years(Louie) ≤ 100
  0 ≤ Service_Years(Donald) ≤ 100
Co-constraints:
  


-- meta -------------------------------------
{'symbols': [{'idpname': 'Vacation_Days',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'Vacation_Days': {'Vacation_Days(Dewey)': {'environmental': False,
                                            'normal': True,
                                            'reading': 'Vacation_Days(Dewey)',
                                            'relevant': True,
                                            'status': 'UNIVERSAL',
                                            'typ': 'Int',
                                            'value': '30',
                                            'values': ['0',
                                                       '1',
                                                       '2',
                                                       '3',
                                                       '4',
                                                       '5',
                                                       '6',
                                                       '7',
                                                       '8',
                                                       '9',
                                                       '10',
                                                       '11',
                                                       '12',
                                                       '13',
                                                       '14',
                                                       '15',
                                                       '16',
                                                       '17',
                                                       '18',
                                                       '19',
                                                       '20',
                                                       '21',
                                                       '22',
                                                       '23',
                                                       '24',
                                                       '25',
                                                       '26',
                                                       '27',
                                                       '28',
                                                       '29',
                                                       '30',
                                                       '31',
                                                       '32',
                                                       '33',
                                                       '34',
                                                       '35',
                                                       '36',
                                                       '37',
                                                       '38',
                                                       '39',
                                                       '40',
                                                       '41',
                                                       '42',
                                                       '43',
                                                       '44',
                                                       '45',
                                                       '46',
                                                       '47',
                                                       '48',
                                                       '49',
                                                       '50',
                                                       '51',
                                                       '52',
                                                       '53',
                                                       '54',
                                                       '55',
                                                       '56',
                                                       '57',
                                                       '58',
                                                       '59',
                                                       '60',
                                                       '61',
                                                       '62',
                                                       '63',
                                                       '64',
                                                       '65',
                                                       '66',
                                                       '67',
                                                       '68',
                                                       '69',
                                                       '70',
                                                       '71',
                                                       '72',
                                                       '73',
                                                       '74',
                                                       '75',
                                                       '76',
                                                       '77',
                                                       '78',
                                                       '79',
                                                       '80',
                                                       '81',
                                                       '82',
                                                       '83',
                                                       '84',
                                                       '85',
                                                       '86',
                                                       '87',
                                                       '88',
                                                       '89',
                                                       '90',
                                                       '91',
                                                       '92',
                                                       '93',
                                                       '94',
                                                       '95',
                                                       '96',
                                                       '97',
                                                       '98',
                                                       '99',
                                                       '100']},
                   'Vacation_Days(Donald)': {'environmental': False,
                                             'normal': True,
                                             'reading': 'Vacation_Days(Donald)',
                                             'relevant': True,
                                             'status': 'UNIVERSAL',
                                             'typ': 'Int',
                                             'value': '27',
                                             'values': ['0',
                                                        '1',
                                                        '2',
                                                        '3',
                                                        '4',
                                                        '5',
                                                        '6',
                                                        '7',
                                                        '8',
                                                        '9',
                                                        '10',
                                                        '11',
                                                        '12',
                                                        '13',
                                                        '14',
                                                        '15',
                                                        '16',
                                                        '17',
                                                        '18',
                                                        '19',
                                                        '20',
                                                        '21',
                                                        '22',
                                                        '23',
                                                        '24',
                                                        '25',
                                                        '26',
                                                        '27',
                                                        '28',
                                                        '29',
                                                        '30',
                                                        '31',
                                                        '32',
                                                        '33',
                                                        '34',
                                                        '35',
                                                        '36',
                                                        '37',
                                                        '38',
                                                        '39',
                                                        '40',
                                                        '41',
                                                        '42',
                                                        '43',
                                                        '44',
                                                        '45',
                                                        '46',
                                                        '47',
                                                        '48',
                                                        '49',
                                                        '50',
                                                        '51',
                                                        '52',
                                                        '53',
                                                        '54',
                                                        '55',
                                                        '56',
                                                        '57',
                                                        '58',
                                                        '59',
                                                        '60',
                                                        '61',
                                                        '62',
                                                        '63',
                                                        '64',
                                                        '65',
                                                        '66',
                                                        '67',
                                                        '68',
                                                        '69',
                                                        '70',
                                                        '71',
                                                        '72',
                                                        '73',
                                                        '74',
                                                        '75',
                                                        '76',
                                                        '77',
                                                        '78',
                                                        '79',
                                                        '80',
                                                        '81',
                                                        '82',
                                                        '83',
                                                        '84',
                                                        '85',
                                                        '86',
                                                        '87',
                                                        '88',
                                                        '89',
                                                        '90',
                                                        '91',
                                                        '92',
                                                        '93',
                                                        '94',
                                                        '95',
                                                        '96',
                                                        '97',
                                                        '98',
                                                        '99',
                                                        '100']},
                   'Vacation_Days(Huey)': {'environmental': False,
                                           'normal': True,
                                           'reading': 'Vacation_Days(Huey)',
                                           'relevant': True,
                                           'status': 'UNIVERSAL',
                                           'typ': 'Int',
                                           'value': '30',
                                           'values': ['0',
                                                      '1',
                                                      '2',
                                                      '3',
                                                      '4',
                                                      '5',
                                                      '6',
                                                      '7',
                                                      '8',
                                                      '9',
                                                      '10',
                                                      '11',
                                                      '12',
                                                      '13',
                                                      '14',
                                                      '15',
                                                      '16',
                                                      '17',
                                                      '18',
                                                      '19',
                                                      '20',
                                                      '21',
                                                      '22',
                                                      '23',
                                                      '24',
                                                      '25',
                                                      '26',
                                                      '27',
                                                      '28',
                                                      '29',
                                                      '30',
                                                      '31',
                                                      '32',
                                                      '33',
                                                      '34',
                                                      '35',
                                                      '36',
                                                      '37',
                                                      '38',
                                                      '39',
                                                      '40',
                                                      '41',
                                                      '42',
                                                      '43',
                                                      '44',
                                                      '45',
                                                      '46',
                                                      '47',
                                                      '48',
                                                      '49',
                                                      '50',
                                                      '51',
                                                      '52',
                                                      '53',
                                                      '54',
                                                      '55',
                                                      '56',
                                                      '57',
                                                      '58',
                                                      '59',
                                                      '60',
                                                      '61',
                                                      '62',
                                                      '63',
                                                      '64',
                                                      '65',
                                                      '66',
                                                      '67',
                                                      '68',
                                                      '69',
                                                      '70',
                                                      '71',
                                                      '72',
                                                      '73',
                                                      '74',
                                                      '75',
                                                      '76',
                                                      '77',
                                                      '78',
                                                      '79',
                                                      '80',
                                                      '81',
                                                      '82',
                                                      '83',
                                                      '84',
                                                      '85',
                                                      '86',
                                                      '87',
                                                      '88',
                                                      '89',
                                                      '90',
                                                      '91',
                                                      '92',
                                                      '93',
                                                      '94',
                                                      '95',
                                                      '96',
                                                      '97',
                                                      '98',
                                                      '99',
                                                      '100']},
                   'Vacation_Days(Louie)': {'environmental': False,
                                            'normal': True,
                                            'reading': 'Vacation_Days(Louie)',
                                            'relevant': True,
                                            'status': 'UNIVERSAL',
                                            'typ': 'Int',
                                            'value': '27',
                                            'values': ['0',
                                                       '1',
                                                       '2',
                                                       '3',
                                                       '4',
                                                       '5',
                                                       '6',
                                                       '7',
                                                       '8',
                                                       '9',
                                                       '10',
                                                       '11',
                                                       '12',
                                                       '13',
                                                       '14',
                                                       '15',
                                                       '16',
                                                       '17',
                                                       '18',
                                                       '19',
                                                       '20',
                                                       '21',
                                                       '22',
                                                       '23',
                                                       '24',
                                                       '25',
                                                       '26',
                                                       '27',
                                                       '28',
                                                       '29',
                                                       '30',
                                                       '31',
                                                       '32',
                                                       '33',
                                                       '34',
                                                       '35',
                                                       '36',
                                                       '37',
                                                       '38',
                                                       '39',
                                                       '40',
                                                       '41',
                                                       '42',
                                                       '43',
                                                       '44',
                                                       '45',
                                                       '46',
                                                       '47',
                                                       '48',
                                                       '49',
                                                       '50',
                                                       '51',
                                                       '52',
                                                       '53',
                                                       '54',
                                                       '55',
                                                       '56',
                                                       '57',
                                                       '58',
                                                       '59',
                                                       '60',
                                                       '61',
                                                       '62',
                                                       '63',
                                                       '64',
                                                       '65',
                                                       '66',
                                                       '67',
                                                       '68',
                                                       '69',
                                                       '70',
                                                       '71',
                                                       '72',
                                                       '73',
                                                       '74',
                                                       '75',
                                                       '76',
                                                       '77',
                                                       '78',
                                                       '79',
                                                       '80',
                                                       '81',
                                                       '82',
                                                       '83',
                                                       '84',
                                                       '85',
                                                       '86',
                                                       '87',
                                                       '88',
                                                       '89',
                                                       '90',
                                                       '91',
                                                       '92',
                                                       '93',
                                                       '94',
                                                       '95',
                                                       '96',
                                                       '97',
                                                       '98',
                                                       '99',
                                                       '100']},
                   '__rank': 1,
                   '∀Employee[Employee_t] : Vacation_Days(Employee) = sum{ : Employee = Employee : 22} + sum{ : Age(Employee) < 18 ∧ Employee = Employee : 05} + sum{ : Age(Employee) ≥ 60 ∧ Employee = Employee : 05} + sum{ : 18 ≤ Age(Employee) ∧ Age(Employee) < 60 ∧ Service_Years(Employee) ≥ 30 ∧ Employee = Employee : 05} + sum{ : Service_Years(Employee) ≥ 30 ∧ Employee = Employee : 03} + sum{ : Age(Employee) < 60 ∧ Service_Years(Employee) < 30 ∧ Employee = Employee : 03} + sum{ : Age(Employee) < 45 ∧ 15 ≤ Service_Years(Employee) ∧ Service_Years(Employee) < 30 ∧ Employee = Employee : 02} + sum{ : 45 ≤ Age(Employee) ∧ Age(Employee) < 60 ∧ Service_Years(Employee) < 30 ∧ Employee = Employee : 02}': {'environmental': False,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 'normal': False,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 'reading': '∀Employee[Employee_t] '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            ': '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'Vacation_Days(Employee) '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '= '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'sum{ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            ': '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'Employee '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '= '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'Employee '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            ': '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '22} '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '+ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'sum{ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            ': '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'Age(Employee) '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '< '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '18 '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '∧ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'Employee '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '= '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'Employee '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            ': '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '05} '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '+ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'sum{ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            ': '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'Age(Employee) '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '≥ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '60 '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '∧ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'Employee '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '= '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'Employee '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            ': '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '05} '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '+ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'sum{ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            ': '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '18 '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '≤ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'Age(Employee) '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '∧ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'Age(Employee) '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '< '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '60 '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '∧ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'Service_Years(Employee) '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '≥ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '30 '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '∧ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'Employee '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '= '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'Employee '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            ': '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '05} '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '+ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'sum{ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            ': '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'Service_Years(Employee) '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '≥ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '30 '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '∧ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'Employee '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '= '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'Employee '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            ': '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '03} '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '+ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'sum{ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            ': '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'Age(Employee) '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '< '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '60 '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '∧ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'Service_Years(Employee) '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '< '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '30 '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '∧ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'Employee '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '= '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'Employee '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            ': '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '03} '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '+ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'sum{ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            ': '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'Age(Employee) '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '< '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '45 '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '∧ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '15 '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '≤ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'Service_Years(Employee) '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '∧ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'Service_Years(Employee) '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '< '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '30 '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '∧ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'Employee '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '= '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'Employee '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            ': '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '02} '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '+ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'sum{ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            ': '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '45 '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '≤ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'Age(Employee) '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '∧ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'Age(Employee) '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '< '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '60 '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '∧ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'Service_Years(Employee) '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '< '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '30 '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '∧ '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'Employee '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '= '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'Employee '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            ': '
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '02}',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 'relevant': True,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 'status': 'UNIVERSAL',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 'typ': 'Bool',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 'value': True}}}
