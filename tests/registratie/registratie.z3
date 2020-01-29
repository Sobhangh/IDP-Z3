
-- theory
(Tax == 1) ==
And(Registration_Type == Heritage, Region == Flemish_Region)

(Tax == 2) ==
And(Registration_Type == Social_Dwelling,
    Region == Flemish_Region)

(Tax == 4) ==
And(Registration_Type == Professional_Purchase,
    Region == Flemish_Region)

(Tax == 6) ==
And(Or(Registration_Type == Energy_Efficient_Dwelling,
       Registration_Type == Social_Purpose,
       Registration_Type == Exchange_Unbuilt_Ground),
    Region == Flemish_Region)

(Tax == 7) ==
And(Or(Registration_Type == Family_Dwelling,
       Registration_Type == Dwelling_For_Social_Renting),
    Region == Flemish_Region)

(Tax == 10) ==
And(Region == Flemish_Region, Registration_Type == Other)

(Tax == 12) ==
Or(Region == Brussels_Region, Region == Walloon_Region)

(Registration_Type == Family_Dwelling) ==
And(Type_Of_Real_Estate == Residential,
    Buyer == Natural_Person,
    Domicile_Established,
    Clean_Purchase,
    Or(First_Ownership, Causal_Connection),
    Or(Not(Energy_Renovation_Planned),
       Not(Term_Energy_Renovation == 5 + Certification_Date)))

(Registration_Type == Social_Dwelling) ==
And(Buyer == Natural_Person,
    Type_Of_Real_Estate == Residential,
    Use == Social_Housing,
    Or(Seller == Vlaamse_Mpy_Voor_Sociaal_Wonen,
       Seller == ErkendeSocialeHuisvestingsMpy),
    Mortgage_Loan_Allowance)

(Registration_Type == Energy_Efficient_Dwelling) ==
And(Type_Of_Real_Estate == Residential,
    Buyer == Natural_Person,
    Domicile_Established,
    Clean_Purchase,
    Or(First_Ownership, Causal_Connection),
    Energy_Renovation_Planned,
    Term_Energy_Renovation == 5 + Certification_Date)

(Registration_Type == Dwelling_For_Social_Renting) ==
And(Type_Of_Real_Estate == Residential,
    Use == Social_Renting,
    Start_Dt_Dwelling_For_Social_Rent ==
    3 + Certification_Date,
    Duration_Of_Agreement == Less_Than_9_years)

(Registration_Type == Heritage) ==
And(Type_Of_Real_Estate == Residential,
    Monument,
    Use == As_Family_Dwelling,
    Heritage_Investment,
    Heritage_Plan,
    Additional_Terms)

(Registration_Type == Professional_Purchase) ==
And(Professional_Buyer,
    Not(Transaction_Type == Public_Sale),
    Use == For_Resale,
    Certification_Date_Sale == 8 + Certification_Date)

(Registration_Type == Social_Purpose) ==
And(Or(Seller == Mpy_Erkend_Door_VMSW,
       Seller == Vlaams_Woningfonds,
       Seller == Gelijksoortige_Rechtspersoon_EER),
    Use == Community_Purpose)

(Registration_Type == Exchange_Unbuilt_Ground) ==
And(Additional_Terms, Not(Monument))

(Registration_Type == Other) ==
And(Not(Registration_Type == Family_Dwelling),
    Not(Registration_Type == Social_Dwelling),
    Not(Registration_Type == Energy_Efficient_Dwelling),
    Not(Registration_Type == Dwelling_For_Social_Renting),
    Not(Registration_Type == Heritage),
    Not(Registration_Type == Professional_Purchase),
    Not(Registration_Type == Social_Purpose),
    Not(Registration_Type == Exchange_Unbuilt_Ground))

Or(Not(Municipality == other_Municipal), Not(Core_City))

Or(Not(Not(Municipality == other_Municipal)), Core_City)

Professional_Buyer ==
And(Professional_Declaration_Filed,
    Guarantee_Satisfied,
    Or(And(Additional_Security_Required,
           Additional_Security_Satisfied),
       Not(Additional_Security_Required)),
    Resale == Three_Or_More)

And(Start_Dt_Dwelling_For_Social_Rent >= 2015,
    Start_Dt_Dwelling_For_Social_Rent <= 2025)

And(Certification_Date >= 2015, Certification_Date <= 2025)

Or(Tax == 1,
   Tax == 2,
   Tax == 4,
   Tax == 7,
   Tax == 6,
   Tax == 10,
   Tax == 12)

And(Term_Energy_Renovation >= 2015,
    Term_Energy_Renovation <= 2025)

And(Certification_Date_Sale >= 2015,
    Certification_Date_Sale <= 2025)

-- atoms
Region
Municipality
Type_Of_Real_Estate
Seller
Buyer
Use
Domicile_Established
First_Ownership
Monument
Resale
Transaction_Type
Duration_Of_Agreement
Core_City
Mortgage_Loan_Allowance
Clean_Purchase
Causal_Connection
Energy_Renovation_Planned
Heritage_Investment
Heritage_Plan
Professional_Declaration_Filed
Guarantee_Satisfied
Additional_Security_Required
Additional_Security_Satisfied
Additional_Terms
Start_Dt_Dwelling_For_Social_Rent
Certification_Date
Tax
Term_Energy_Renovation
Certification_Date_Sale
Registration_Type
Professional_Buyer
Tax = 1
Registration_Type = Heritage
Region = Flemish_Region
Tax = 2
Registration_Type = Social_Dwelling
Tax = 4
Registration_Type = Professional_Purchase
Tax = 6
Registration_Type = Energy_Efficient_Dwelling
Registration_Type = Social_Purpose
Registration_Type = Exchange_Unbuilt_Ground
Tax = 7
Registration_Type = Family_Dwelling
Registration_Type = Dwelling_For_Social_Renting
Tax = 10
Registration_Type = Other
Tax = 12
Region = Brussels_Region
Region = Walloon_Region
Type_Of_Real_Estate = Residential
Buyer = Natural_Person
Term_Energy_Renovation = (Certification_Date + 5)
Use = Social_Housing
Seller = Vlaamse_Mpy_Voor_Sociaal_Wonen
Seller = ErkendeSocialeHuisvestingsMpy
Use = Social_Renting
Start_Dt_Dwelling_For_Social_Rent = (Certification_Date + 3)
Duration_Of_Agreement = Less_Than_9_years
Use = As_Family_Dwelling
Transaction_Type = Public_Sale
Use = For_Resale
Certification_Date_Sale = (Certification_Date + 8)
Seller = Mpy_Erkend_Door_VMSW
Seller = Vlaams_Woningfonds
Seller = Gelijksoortige_Rechtspersoon_EER
Use = Community_Purpose
Municipality = other_Municipal
Resale = Three_Or_More

-- case
Type:        
  
Definitions: 
  
Universals:  
  
Consequences:
  
Simplified:  
  ((Tax = 1) ⇔ ((Registration_Type = Heritage) ∧ (Region = Flemish_Region)))
  (Tax = 2) ⇔ ((Registration_Type = Social_Dwelling) ∧ (Region = Flemish_Region))
  (Tax = 4) ⇔ ((Registration_Type = Professional_Purchase) ∧ (Region = Flemish_Region))
  ((Tax = 6) ⇔ (((Registration_Type = Energy_Efficient_Dwelling) ∨ (Registration_Type = Social_Purpose) ∨ (Registration_Type = Exchange_Unbuilt_Ground)) ∧ (Region = Flemish_Region)))
  (Tax = 7) ⇔ (((Registration_Type = Family_Dwelling) ∨ (Registration_Type = Dwelling_For_Social_Renting)) ∧ (Region = Flemish_Region))
  (Tax = 10) ⇔ ((Region = Flemish_Region) ∧ (Registration_Type = Other))
  ((Tax = 12) ⇔ ((Region = Brussels_Region) ∨ (Region = Walloon_Region)))
  (Registration_Type = Family_Dwelling) ⇔ ((Type_Of_Real_Estate = Residential) ∧ (Buyer = Natural_Person) ∧ Domicile_Established ∧ Clean_Purchase ∧ (First_Ownership ∨ Causal_Connection) ∧ ((~(Energy_Renovation_Planned)) ∨ (~(Term_Energy_Renovation = (5 + Certification_Date)))))
  (Registration_Type = Social_Dwelling) ⇔ ((Buyer = Natural_Person) ∧ (Type_Of_Real_Estate = Residential) ∧ (Use = Social_Housing) ∧ ((Seller = Vlaamse_Mpy_Voor_Sociaal_Wonen) ∨ (Seller = ErkendeSocialeHuisvestingsMpy)) ∧ Mortgage_Loan_Allowance)
  (Registration_Type = Energy_Efficient_Dwelling) ⇔ ((Type_Of_Real_Estate = Residential) ∧ (Buyer = Natural_Person) ∧ Domicile_Established ∧ Clean_Purchase ∧ (First_Ownership ∨ Causal_Connection) ∧ Energy_Renovation_Planned ∧ (Term_Energy_Renovation = (5 + Certification_Date)))
  (Registration_Type = Dwelling_For_Social_Renting) ⇔ ((Type_Of_Real_Estate = Residential) ∧ (Use = Social_Renting) ∧ (Start_Dt_Dwelling_For_Social_Rent = (3 + Certification_Date)) ∧ (Duration_Of_Agreement = Less_Than_9_years))
  ((Registration_Type = Heritage) ⇔ ((Type_Of_Real_Estate = Residential) ∧ Monument ∧ (Use = As_Family_Dwelling) ∧ Heritage_Investment ∧ Heritage_Plan ∧ Additional_Terms))
  (Registration_Type = Professional_Purchase) ⇔ (Professional_Buyer ∧ (~(Transaction_Type = Public_Sale)) ∧ (Use = For_Resale) ∧ (Certification_Date_Sale = (8 + Certification_Date)))
  ((Registration_Type = Social_Purpose) ⇔ (((Seller = Mpy_Erkend_Door_VMSW) ∨ (Seller = Vlaams_Woningfonds) ∨ (Seller = Gelijksoortige_Rechtspersoon_EER)) ∧ (Use = Community_Purpose)))
  (Registration_Type = Exchange_Unbuilt_Ground) ⇔ (Additional_Terms ∧ (~(Monument)))
  (Registration_Type = Other) ⇔ ((~(Registration_Type = Family_Dwelling)) ∧ (~(Registration_Type = Social_Dwelling)) ∧ (~(Registration_Type = Energy_Efficient_Dwelling)) ∧ (~(Registration_Type = Dwelling_For_Social_Renting)) ∧ (~(Registration_Type = Heritage)) ∧ (~(Registration_Type = Professional_Purchase)) ∧ (~(Registration_Type = Social_Purpose)) ∧ (~(Registration_Type = Exchange_Unbuilt_Ground)))
  (Municipality = other_Municipal) ⇒ (~(Core_City))
  (~(Municipality = other_Municipal)) ⇒ Core_City
  Professional_Buyer ⇔ (Professional_Declaration_Filed ∧ Guarantee_Satisfied ∧ ((Additional_Security_Required ∧ Additional_Security_Satisfied) ∨ (~(Additional_Security_Required))) ∧ (Resale = Three_Or_More))
  2015 ≤ Start_Dt_Dwelling_For_Social_Rent ≤ 2025
  2015 ≤ Certification_Date ≤ 2025
  (1 = Tax) ∨ (2 = Tax) ∨ (4 = Tax) ∨ (7 = Tax) ∨ (6 = Tax) ∨ (10 = Tax) ∨ (12 = Tax)
  2015 ≤ Term_Energy_Renovation ≤ 2025
  2015 ≤ Certification_Date_Sale ≤ 2025
Irrelevant:  
  


-- propagation
{'Additional_Security_Required': {'Additional_Security_Required': {'cf': False,
                                                                   'ct': False,
                                                                   'environmental': False,
                                                                   'irrelevant': False,
                                                                   'normal': True,
                                                                   'reading': 'Additional_Security_Required',
                                                                   'status': 'UNKNOWN',
                                                                   'typ': 'Bool'}},
 'Additional_Security_Satisfied': {'Additional_Security_Satisfied': {'cf': False,
                                                                     'ct': False,
                                                                     'environmental': False,
                                                                     'irrelevant': False,
                                                                     'normal': True,
                                                                     'reading': 'Additional_Security_Satisfied',
                                                                     'status': 'UNKNOWN',
                                                                     'typ': 'Bool'}},
 'Additional_Terms': {'Additional_Terms': {'cf': False,
                                           'ct': False,
                                           'environmental': False,
                                           'irrelevant': False,
                                           'normal': True,
                                           'reading': 'Additional_Terms',
                                           'status': 'UNKNOWN',
                                           'typ': 'Bool'}},
 'Buyer': {'Buyer': {'environmental': False,
                     'irrelevant': False,
                     'normal': True,
                     'reading': 'Buyer',
                     'status': 'UNKNOWN',
                     'typ': 'buyerType',
                     'value': '',
                     'values': ['Natural_Person', 'Legal_Person', 'Mixed']},
           'Buyer = Natural_Person': {'cf': False,
                                      'ct': False,
                                      'environmental': False,
                                      'irrelevant': False,
                                      'normal': False,
                                      'reading': 'Buyer = Natural_Person',
                                      'status': 'UNKNOWN',
                                      'typ': 'Bool'}},
 'Causal_Connection': {'Causal_Connection': {'cf': False,
                                             'ct': False,
                                             'environmental': False,
                                             'irrelevant': False,
                                             'normal': True,
                                             'reading': 'Causal_Connection',
                                             'status': 'UNKNOWN',
                                             'typ': 'Bool'}},
 'Certification_Date': {'Certification_Date': {'environmental': False,
                                               'irrelevant': False,
                                               'normal': True,
                                               'reading': 'Certification_Date',
                                               'status': 'UNKNOWN',
                                               'typ': 'Int',
                                               'value': '',
                                               'values': ['2015',
                                                          '2016',
                                                          '2017',
                                                          '2018',
                                                          '2019',
                                                          '2020',
                                                          '2021',
                                                          '2022',
                                                          '2023',
                                                          '2024',
                                                          '2025']}},
 'Certification_Date_Sale': {'Certification_Date_Sale': {'environmental': False,
                                                         'irrelevant': False,
                                                         'normal': True,
                                                         'reading': 'Certification_Date_Sale',
                                                         'status': 'UNKNOWN',
                                                         'typ': 'Int',
                                                         'value': '',
                                                         'values': ['2015',
                                                                    '2016',
                                                                    '2017',
                                                                    '2018',
                                                                    '2019',
                                                                    '2020',
                                                                    '2021',
                                                                    '2022',
                                                                    '2023',
                                                                    '2024',
                                                                    '2025']},
                             'Certification_Date_Sale = (Certification_Date + 8)': {'cf': False,
                                                                                    'ct': False,
                                                                                    'environmental': False,
                                                                                    'irrelevant': False,
                                                                                    'normal': False,
                                                                                    'reading': 'Certification_Date_Sale '
                                                                                               '= (Certification_Date '
                                                                                               '+ 8)',
                                                                                    'status': 'UNKNOWN',
                                                                                    'typ': 'Bool'}},
 'Clean_Purchase': {'Clean_Purchase': {'cf': False,
                                       'ct': False,
                                       'environmental': False,
                                       'irrelevant': False,
                                       'normal': True,
                                       'reading': 'Clean_Purchase',
                                       'status': 'UNKNOWN',
                                       'typ': 'Bool'}},
 'Core_City': {'Core_City': {'cf': False,
                             'ct': False,
                             'environmental': False,
                             'irrelevant': False,
                             'normal': True,
                             'reading': 'Core_City',
                             'status': 'UNKNOWN',
                             'typ': 'Bool'}},
 'Domicile_Established': {'Domicile_Established': {'cf': False,
                                                   'ct': False,
                                                   'environmental': False,
                                                   'irrelevant': False,
                                                   'normal': True,
                                                   'reading': 'Domicile_Established',
                                                   'status': 'UNKNOWN',
                                                   'typ': 'Bool'}},
 'Duration_Of_Agreement': {'Duration_Of_Agreement': {'environmental': False,
                                                     'irrelevant': False,
                                                     'normal': True,
                                                     'reading': 'Duration_Of_Agreement',
                                                     'status': 'UNKNOWN',
                                                     'typ': 'agreementDwellingForSocialRenting',
                                                     'value': '',
                                                     'values': ['Less_Than_9_years', 'More_than_9_Or_9_years']},
                           'Duration_Of_Agreement = Less_Than_9_years': {'cf': False,
                                                                         'ct': False,
                                                                         'environmental': False,
                                                                         'irrelevant': False,
                                                                         'normal': False,
                                                                         'reading': 'Duration_Of_Agreement = '
                                                                                    'Less_Than_9_years',
                                                                         'status': 'UNKNOWN',
                                                                         'typ': 'Bool'}},
 'Energy_Renovation_Planned': {'Energy_Renovation_Planned': {'cf': False,
                                                             'ct': False,
                                                             'environmental': False,
                                                             'irrelevant': False,
                                                             'normal': True,
                                                             'reading': 'Energy_Renovation_Planned',
                                                             'status': 'UNKNOWN',
                                                             'typ': 'Bool'}},
 'First_Ownership': {'First_Ownership': {'cf': False,
                                         'ct': False,
                                         'environmental': False,
                                         'irrelevant': False,
                                         'normal': True,
                                         'reading': 'First_Ownership',
                                         'status': 'UNKNOWN',
                                         'typ': 'Bool'}},
 'Guarantee_Satisfied': {'Guarantee_Satisfied': {'cf': False,
                                                 'ct': False,
                                                 'environmental': False,
                                                 'irrelevant': False,
                                                 'normal': True,
                                                 'reading': 'Guarantee_Satisfied',
                                                 'status': 'UNKNOWN',
                                                 'typ': 'Bool'}},
 'Heritage_Investment': {'Heritage_Investment': {'cf': False,
                                                 'ct': False,
                                                 'environmental': False,
                                                 'irrelevant': False,
                                                 'normal': True,
                                                 'reading': 'Heritage_Investment',
                                                 'status': 'UNKNOWN',
                                                 'typ': 'Bool'}},
 'Heritage_Plan': {'Heritage_Plan': {'cf': False,
                                     'ct': False,
                                     'environmental': False,
                                     'irrelevant': False,
                                     'normal': True,
                                     'reading': 'Heritage_Plan',
                                     'status': 'UNKNOWN',
                                     'typ': 'Bool'}},
 'Monument': {'Monument': {'cf': False,
                           'ct': False,
                           'environmental': False,
                           'irrelevant': False,
                           'normal': True,
                           'reading': 'Monument',
                           'status': 'UNKNOWN',
                           'typ': 'Bool'}},
 'Mortgage_Loan_Allowance': {'Mortgage_Loan_Allowance': {'cf': False,
                                                         'ct': False,
                                                         'environmental': False,
                                                         'irrelevant': False,
                                                         'normal': True,
                                                         'reading': 'Mortgage_Loan_Allowance',
                                                         'status': 'UNKNOWN',
                                                         'typ': 'Bool'}},
 'Municipality': {'Municipality': {'environmental': False,
                                   'irrelevant': False,
                                   'normal': True,
                                   'reading': 'Municipality',
                                   'status': 'UNKNOWN',
                                   'typ': 'municipality',
                                   'value': '',
                                   'values': ['other_Municipal',
                                              'Aalst',
                                              'Antwerpen',
                                              'Boom',
                                              'Brugge',
                                              'Dendermonde',
                                              'Genk',
                                              'Gent',
                                              'Hasselt',
                                              'Kortrijk',
                                              'Leuven',
                                              'Mechelen',
                                              'Oostende',
                                              'Roeselare',
                                              'SintNiklaas',
                                              'Turnhout',
                                              'Vilvoorde',
                                              'Affligem',
                                              'Asse',
                                              'Beersel',
                                              'Bever',
                                              'Dilbeek',
                                              'Drogenbos',
                                              'Galmaarden',
                                              'Gooik',
                                              'Grimbergen',
                                              'Halle',
                                              'Herne',
                                              'Hoeilaart',
                                              'Kampenhout',
                                              'KapelleopdenBos',
                                              'Kraainem',
                                              'Lennik',
                                              'Liedekerke',
                                              'Linkebeek',
                                              'Londerzeel',
                                              'Machelen',
                                              'Meise',
                                              'Merchtem',
                                              'Opwijk',
                                              'Overijse',
                                              'Pepingen',
                                              'Roosdaal',
                                              'SintGenesiusRode',
                                              'SintPietersLeeuw',
                                              'Steenokkerzeel',
                                              'Ternat',
                                              'Wemmel',
                                              'WezembeekOppem',
                                              'Zaventem',
                                              'Zemst',
                                              'Bertem',
                                              'Huldenberg',
                                              'Kortenberg',
                                              'Tervuren']},
                  'Municipality = other_Municipal': {'cf': False,
                                                     'ct': False,
                                                     'environmental': False,
                                                     'irrelevant': False,
                                                     'normal': False,
                                                     'reading': 'Municipality = other_Municipal',
                                                     'status': 'UNKNOWN',
                                                     'typ': 'Bool'}},
 'Professional_Buyer': {'Professional_Buyer': {'cf': False,
                                               'ct': False,
                                               'environmental': False,
                                               'irrelevant': False,
                                               'normal': True,
                                               'reading': 'Professional_Buyer',
                                               'status': 'UNKNOWN',
                                               'typ': 'Bool'}},
 'Professional_Declaration_Filed': {'Professional_Declaration_Filed': {'cf': False,
                                                                       'ct': False,
                                                                       'environmental': False,
                                                                       'irrelevant': False,
                                                                       'normal': True,
                                                                       'reading': 'Professional_Declaration_Filed',
                                                                       'status': 'UNKNOWN',
                                                                       'typ': 'Bool'}},
 'Region': {'Region': {'environmental': False,
                       'irrelevant': False,
                       'normal': True,
                       'reading': 'Region',
                       'status': 'UNKNOWN',
                       'typ': 'location',
                       'value': '',
                       'values': ['Flemish_Region', 'Walloon_Region', 'Brussels_Region']},
            'Region = Brussels_Region': {'cf': False,
                                         'ct': False,
                                         'environmental': False,
                                         'irrelevant': False,
                                         'normal': False,
                                         'reading': 'Region = Brussels_Region',
                                         'status': 'UNKNOWN',
                                         'typ': 'Bool'},
            'Region = Flemish_Region': {'cf': False,
                                        'ct': False,
                                        'environmental': False,
                                        'irrelevant': False,
                                        'normal': False,
                                        'reading': 'Region = Flemish_Region',
                                        'status': 'UNKNOWN',
                                        'typ': 'Bool'},
            'Region = Walloon_Region': {'cf': False,
                                        'ct': False,
                                        'environmental': False,
                                        'irrelevant': False,
                                        'normal': False,
                                        'reading': 'Region = Walloon_Region',
                                        'status': 'UNKNOWN',
                                        'typ': 'Bool'}},
 'Registration_Type': {'Registration_Type': {'environmental': False,
                                             'irrelevant': False,
                                             'normal': True,
                                             'reading': 'Registration_Type',
                                             'status': 'UNKNOWN',
                                             'typ': 'registration_Type',
                                             'value': '',
                                             'values': ['Family_Dwelling',
                                                        'Social_Dwelling',
                                                        'Social_Purpose',
                                                        'Exchange_Unbuilt_Ground',
                                                        'Professional_Purchase',
                                                        'Energy_Efficient_Dwelling',
                                                        'Heritage',
                                                        'Dwelling_For_Social_Renting',
                                                        'Other']},
                       'Registration_Type = Dwelling_For_Social_Renting': {'cf': False,
                                                                           'ct': False,
                                                                           'environmental': False,
                                                                           'irrelevant': False,
                                                                           'normal': False,
                                                                           'reading': 'Registration_Type = '
                                                                                      'Dwelling_For_Social_Renting',
                                                                           'status': 'UNKNOWN',
                                                                           'typ': 'Bool'},
                       'Registration_Type = Energy_Efficient_Dwelling': {'cf': False,
                                                                         'ct': False,
                                                                         'environmental': False,
                                                                         'irrelevant': False,
                                                                         'normal': False,
                                                                         'reading': 'Registration_Type = '
                                                                                    'Energy_Efficient_Dwelling',
                                                                         'status': 'UNKNOWN',
                                                                         'typ': 'Bool'},
                       'Registration_Type = Exchange_Unbuilt_Ground': {'cf': False,
                                                                       'ct': False,
                                                                       'environmental': False,
                                                                       'irrelevant': False,
                                                                       'normal': False,
                                                                       'reading': 'Registration_Type = '
                                                                                  'Exchange_Unbuilt_Ground',
                                                                       'status': 'UNKNOWN',
                                                                       'typ': 'Bool'},
                       'Registration_Type = Family_Dwelling': {'cf': False,
                                                               'ct': False,
                                                               'environmental': False,
                                                               'irrelevant': False,
                                                               'normal': False,
                                                               'reading': 'Registration_Type = Family_Dwelling',
                                                               'status': 'UNKNOWN',
                                                               'typ': 'Bool'},
                       'Registration_Type = Heritage': {'cf': False,
                                                        'ct': False,
                                                        'environmental': False,
                                                        'irrelevant': False,
                                                        'normal': False,
                                                        'reading': 'Registration_Type = Heritage',
                                                        'status': 'UNKNOWN',
                                                        'typ': 'Bool'},
                       'Registration_Type = Other': {'cf': False,
                                                     'ct': False,
                                                     'environmental': False,
                                                     'irrelevant': False,
                                                     'normal': False,
                                                     'reading': 'Registration_Type = Other',
                                                     'status': 'UNKNOWN',
                                                     'typ': 'Bool'},
                       'Registration_Type = Professional_Purchase': {'cf': False,
                                                                     'ct': False,
                                                                     'environmental': False,
                                                                     'irrelevant': False,
                                                                     'normal': False,
                                                                     'reading': 'Registration_Type = '
                                                                                'Professional_Purchase',
                                                                     'status': 'UNKNOWN',
                                                                     'typ': 'Bool'},
                       'Registration_Type = Social_Dwelling': {'cf': False,
                                                               'ct': False,
                                                               'environmental': False,
                                                               'irrelevant': False,
                                                               'normal': False,
                                                               'reading': 'Registration_Type = Social_Dwelling',
                                                               'status': 'UNKNOWN',
                                                               'typ': 'Bool'},
                       'Registration_Type = Social_Purpose': {'cf': False,
                                                              'ct': False,
                                                              'environmental': False,
                                                              'irrelevant': False,
                                                              'normal': False,
                                                              'reading': 'Registration_Type = Social_Purpose',
                                                              'status': 'UNKNOWN',
                                                              'typ': 'Bool'}},
 'Resale': {'Resale': {'environmental': False,
                       'irrelevant': False,
                       'normal': True,
                       'reading': 'Resale',
                       'status': 'UNKNOWN',
                       'typ': 'resale',
                       'value': '',
                       'values': ['Less_Than_Three', 'Three_Or_More']},
            'Resale = Three_Or_More': {'cf': False,
                                       'ct': False,
                                       'environmental': False,
                                       'irrelevant': False,
                                       'normal': False,
                                       'reading': 'Resale = Three_Or_More',
                                       'status': 'UNKNOWN',
                                       'typ': 'Bool'}},
 'Seller': {'Seller': {'environmental': False,
                       'irrelevant': False,
                       'normal': True,
                       'reading': 'Seller',
                       'status': 'UNKNOWN',
                       'typ': 'seller',
                       'value': '',
                       'values': ['Vlaams_Woningfonds',
                                  'Gelijksoortige_Rechtspersoon_EER',
                                  'Mpy_Erkend_Door_VMSW',
                                  'Vlaamse_Mpy_Voor_Sociaal_Wonen',
                                  'ErkendeSocialeHuisvestingsMpy']},
            'Seller = ErkendeSocialeHuisvestingsMpy': {'cf': False,
                                                       'ct': False,
                                                       'environmental': False,
                                                       'irrelevant': False,
                                                       'normal': False,
                                                       'reading': 'Seller = ErkendeSocialeHuisvestingsMpy',
                                                       'status': 'UNKNOWN',
                                                       'typ': 'Bool'},
            'Seller = Gelijksoortige_Rechtspersoon_EER': {'cf': False,
                                                          'ct': False,
                                                          'environmental': False,
                                                          'irrelevant': False,
                                                          'normal': False,
                                                          'reading': 'Seller = Gelijksoortige_Rechtspersoon_EER',
                                                          'status': 'UNKNOWN',
                                                          'typ': 'Bool'},
            'Seller = Mpy_Erkend_Door_VMSW': {'cf': False,
                                              'ct': False,
                                              'environmental': False,
                                              'irrelevant': False,
                                              'normal': False,
                                              'reading': 'Seller = Mpy_Erkend_Door_VMSW',
                                              'status': 'UNKNOWN',
                                              'typ': 'Bool'},
            'Seller = Vlaams_Woningfonds': {'cf': False,
                                            'ct': False,
                                            'environmental': False,
                                            'irrelevant': False,
                                            'normal': False,
                                            'reading': 'Seller = Vlaams_Woningfonds',
                                            'status': 'UNKNOWN',
                                            'typ': 'Bool'},
            'Seller = Vlaamse_Mpy_Voor_Sociaal_Wonen': {'cf': False,
                                                        'ct': False,
                                                        'environmental': False,
                                                        'irrelevant': False,
                                                        'normal': False,
                                                        'reading': 'Seller = Vlaamse_Mpy_Voor_Sociaal_Wonen',
                                                        'status': 'UNKNOWN',
                                                        'typ': 'Bool'}},
 'Start_Dt_Dwelling_For_Social_Rent': {'Start_Dt_Dwelling_For_Social_Rent': {'environmental': False,
                                                                             'irrelevant': False,
                                                                             'normal': True,
                                                                             'reading': 'Start_Dt_Dwelling_For_Social_Rent',
                                                                             'status': 'UNKNOWN',
                                                                             'typ': 'Int',
                                                                             'value': '',
                                                                             'values': ['2015',
                                                                                        '2016',
                                                                                        '2017',
                                                                                        '2018',
                                                                                        '2019',
                                                                                        '2020',
                                                                                        '2021',
                                                                                        '2022',
                                                                                        '2023',
                                                                                        '2024',
                                                                                        '2025']},
                                       'Start_Dt_Dwelling_For_Social_Rent = (Certification_Date + 3)': {'cf': False,
                                                                                                        'ct': False,
                                                                                                        'environmental': False,
                                                                                                        'irrelevant': False,
                                                                                                        'normal': False,
                                                                                                        'reading': 'Start_Dt_Dwelling_For_Social_Rent '
                                                                                                                   '= '
                                                                                                                   '(Certification_Date '
                                                                                                                   '+ '
                                                                                                                   '3)',
                                                                                                        'status': 'UNKNOWN',
                                                                                                        'typ': 'Bool'}},
 'Tax': {'Tax': {'environmental': False,
                 'irrelevant': False,
                 'normal': True,
                 'reading': 'Tax',
                 'status': 'UNKNOWN',
                 'typ': 'Int',
                 'value': '',
                 'values': ['1', '2', '4', '7', '6', '10', '12']},
         'Tax = 1': {'cf': False,
                     'ct': False,
                     'environmental': False,
                     'irrelevant': False,
                     'normal': False,
                     'reading': 'Tax = 1',
                     'status': 'UNKNOWN',
                     'typ': 'Bool'},
         'Tax = 10': {'cf': False,
                      'ct': False,
                      'environmental': False,
                      'irrelevant': False,
                      'normal': False,
                      'reading': 'Tax = 10',
                      'status': 'UNKNOWN',
                      'typ': 'Bool'},
         'Tax = 12': {'cf': False,
                      'ct': False,
                      'environmental': False,
                      'irrelevant': False,
                      'normal': False,
                      'reading': 'Tax = 12',
                      'status': 'UNKNOWN',
                      'typ': 'Bool'},
         'Tax = 2': {'cf': False,
                     'ct': False,
                     'environmental': False,
                     'irrelevant': False,
                     'normal': False,
                     'reading': 'Tax = 2',
                     'status': 'UNKNOWN',
                     'typ': 'Bool'},
         'Tax = 4': {'cf': False,
                     'ct': False,
                     'environmental': False,
                     'irrelevant': False,
                     'normal': False,
                     'reading': 'Tax = 4',
                     'status': 'UNKNOWN',
                     'typ': 'Bool'},
         'Tax = 6': {'cf': False,
                     'ct': False,
                     'environmental': False,
                     'irrelevant': False,
                     'normal': False,
                     'reading': 'Tax = 6',
                     'status': 'UNKNOWN',
                     'typ': 'Bool'},
         'Tax = 7': {'cf': False,
                     'ct': False,
                     'environmental': False,
                     'irrelevant': False,
                     'normal': False,
                     'reading': 'Tax = 7',
                     'status': 'UNKNOWN',
                     'typ': 'Bool'}},
 'Term_Energy_Renovation': {'Term_Energy_Renovation': {'environmental': False,
                                                       'irrelevant': False,
                                                       'normal': True,
                                                       'reading': 'Term_Energy_Renovation',
                                                       'status': 'UNKNOWN',
                                                       'typ': 'Int',
                                                       'value': '',
                                                       'values': ['2015',
                                                                  '2016',
                                                                  '2017',
                                                                  '2018',
                                                                  '2019',
                                                                  '2020',
                                                                  '2021',
                                                                  '2022',
                                                                  '2023',
                                                                  '2024',
                                                                  '2025']},
                            'Term_Energy_Renovation = (Certification_Date + 5)': {'cf': False,
                                                                                  'ct': False,
                                                                                  'environmental': False,
                                                                                  'irrelevant': False,
                                                                                  'normal': False,
                                                                                  'reading': 'Term_Energy_Renovation = '
                                                                                             '(Certification_Date + 5)',
                                                                                  'status': 'UNKNOWN',
                                                                                  'typ': 'Bool'}},
 'Transaction_Type': {'Transaction_Type': {'environmental': False,
                                           'irrelevant': False,
                                           'normal': True,
                                           'reading': 'Transaction_Type',
                                           'status': 'UNKNOWN',
                                           'typ': 'transaction',
                                           'value': '',
                                           'values': ['Public_Sale', 'Out_Hand', 'Public_Sale_Community']},
                      'Transaction_Type = Public_Sale': {'cf': False,
                                                         'ct': False,
                                                         'environmental': False,
                                                         'irrelevant': False,
                                                         'normal': False,
                                                         'reading': 'Transaction_Type = Public_Sale',
                                                         'status': 'UNKNOWN',
                                                         'typ': 'Bool'}},
 'Type_Of_Real_Estate': {'Type_Of_Real_Estate': {'environmental': False,
                                                 'irrelevant': False,
                                                 'normal': True,
                                                 'reading': 'Type_Of_Real_Estate',
                                                 'status': 'UNKNOWN',
                                                 'typ': 'real_Estate_Type',
                                                 'value': '',
                                                 'values': ['Residential',
                                                            'Residential_Building_Land',
                                                            'Other_Real_Estate']},
                         'Type_Of_Real_Estate = Residential': {'cf': False,
                                                               'ct': False,
                                                               'environmental': False,
                                                               'irrelevant': False,
                                                               'normal': False,
                                                               'reading': 'Type_Of_Real_Estate = Residential',
                                                               'status': 'UNKNOWN',
                                                               'typ': 'Bool'}},
 'Use': {'Use': {'environmental': False,
                 'irrelevant': False,
                 'normal': True,
                 'reading': 'Use',
                 'status': 'UNKNOWN',
                 'typ': 'destination',
                 'value': '',
                 'values': ['As_Family_Dwelling',
                            'For_Resale',
                            'Community_Purpose',
                            'Social_Housing',
                            'Social_Renting',
                            'Other_House',
                            'No_House']},
         'Use = As_Family_Dwelling': {'cf': False,
                                      'ct': False,
                                      'environmental': False,
                                      'irrelevant': False,
                                      'normal': False,
                                      'reading': 'Use = As_Family_Dwelling',
                                      'status': 'UNKNOWN',
                                      'typ': 'Bool'},
         'Use = Community_Purpose': {'cf': False,
                                     'ct': False,
                                     'environmental': False,
                                     'irrelevant': False,
                                     'normal': False,
                                     'reading': 'Use = Community_Purpose',
                                     'status': 'UNKNOWN',
                                     'typ': 'Bool'},
         'Use = For_Resale': {'cf': False,
                              'ct': False,
                              'environmental': False,
                              'irrelevant': False,
                              'normal': False,
                              'reading': 'Use = For_Resale',
                              'status': 'UNKNOWN',
                              'typ': 'Bool'},
         'Use = Social_Housing': {'cf': False,
                                  'ct': False,
                                  'environmental': False,
                                  'irrelevant': False,
                                  'normal': False,
                                  'reading': 'Use = Social_Housing',
                                  'status': 'UNKNOWN',
                                  'typ': 'Bool'},
         'Use = Social_Renting': {'cf': False,
                                  'ct': False,
                                  'environmental': False,
                                  'irrelevant': False,
                                  'normal': False,
                                  'reading': 'Use = Social_Renting',
                                  'status': 'UNKNOWN',
                                  'typ': 'Bool'}}}
