
-- original ---------------------------------
vocabulary environment {
type location := {Flemish_Region, Walloon_Region, Brussels_Region}

type real_Estate_Type := {Residential, Residential_Building_Land, Other_Real_Estate}

type destination := {As_Family_Dwelling, For_Resale, Community_Purpose, Social_Housing, Social_Renting, Other_House, No_House}
type buyerType := {Natural_Person, Legal_Person, Mixed}

type calculationBase := {190, 200, 210, 220, 225}
type baseLimit := {200, 220}
//type DiscountType := {56, 48, 0}

type date := {2015..2025}

type agreementDwellingForSocialRenting := {Less_Than_9_years, More_than_9_Or_9_years}

type transaction := {Public_Sale, Out_Hand, Public_Sale_Community}



type municipality := {other_Municipal, Aalst, Antwerpen, Boom, Brugge, Dendermonde, Genk, Gent, Hasselt, Kortrijk, Leuven, Mechelen, Oostende, Roeselare, SintNiklaas, Turnhout, Vilvoorde, Affligem, Asse, Beersel, Bever, Dilbeek, Drogenbos, Galmaarden, Gooik, Grimbergen, Halle, Herne, Hoeilaart, Kampenhout, KapelleopdenBos, Kraainem, Lennik, Liedekerke, Linkebeek, Londerzeel, Machelen, Meise, Merchtem, Opwijk, Overijse, Pepingen, Roosdaal, SintGenesiusRode, SintPietersLeeuw, Steenokkerzeel, Ternat, Wemmel, WezembeekOppem, Zaventem, Zemst, Bertem, Huldenberg, Kortenberg, Tervuren}

type resale := {Less_Than_Three, Three_Or_More}


type seller := {Vlaams_Woningfonds, Gelijksoortige_Rechtspersoon_EER, Mpy_Erkend_Door_VMSW, Vlaamse_Mpy_Voor_Sociaal_Wonen, ErkendeSocialeHuisvestingsMpy}


////////////////////////

Region : ()→location
Municipality : ()→municipality
Type_Of_Real_Estate : ()→real_Estate_Type
Seller : ()→seller
Buyer : ()→buyerType
Use : ()→destination

Domicile_Established:() → Bool
First_Ownership:() → Bool
Monument:() → Bool

Resale : ()→resale
Transaction_Type : ()→transaction
Duration_Of_Agreement : ()→agreementDwellingForSocialRenting

Core_City:() → Bool

//SocialSeller
Mortgage_Loan_Allowance:() → Bool
Clean_Purchase:() → Bool
Causal_Connection:() → Bool


Energy_Renovation_Planned:() → Bool

//SocialRentingAgreement
Heritage_Investment:() → Bool
Heritage_Plan:() → Bool
//AdditionalConditions

Professional_Declaration_Filed:() → Bool
Guarantee_Satisfied:() → Bool
Additional_Security_Required:() → Bool
Additional_Security_Satisfied:() → Bool

//TaxableBase : ()→calculationBase
//PermittedBase : ()→baseLimit

Additional_Terms:() → Bool


Start_Dt_Dwelling_For_Social_Rent : ()→date

Certification_Date : ()→date

Term_Energy_Renovation : ()→date
Certification_Date_Sale : ()→date
//DomicileDate : ()→date

//IsDiscount: ()→DiscountType
Professional_Buyer:() → Bool
}

vocabulary decision {
    extern vocabulary environment

    type registration_Type := {Family_Dwelling, Social_Dwelling, Social_Purpose, Exchange_Unbuilt_Ground, Professional_Purchase, Energy_Efficient_Dwelling, Heritage, Dwelling_For_Social_Renting, Other}
    type tax_Rate := {1, 2, 4, 7, 6, 10, 12}

    Registration_Type : ()→registration_Type
    Tax : ()→tax_Rate
}

theory environment:environment {
    Professional_Buyer() =>
        Professional_Declaration_Filed()
        & Guarantee_Satisfied()
        & (Additional_Security_Required() & Additional_Security_Satisfied()
        | ~ Additional_Security_Required())
        & Resale() = Three_Or_More.
}

theory decision:decision {

     // Tax

[Registration rate for heritage in Flemish Region is 1%.](
Tax() = 1 =>
    Registration_Type() = Heritage
    & Region() = Flemish_Region
).

Tax() = 2 => // correct amount is 1; 5
    Registration_Type() = Social_Dwelling
    & Region() = Flemish_Region
.

Tax() = 4 =>
    Registration_Type() = Professional_Purchase
    & Region() = Flemish_Region
.

[The tax rate is 6% for social purpose sales in the Flemish Region.]
(Tax() = 6 =>
    (Registration_Type() = Energy_Efficient_Dwelling
    | Registration_Type() = Social_Purpose
    | Registration_Type() = Exchange_Unbuilt_Ground)
    & Region() = Flemish_Region
).

Tax() = 7 =>
    (Registration_Type() = Family_Dwelling
    | Registration_Type() = Dwelling_For_Social_Renting)
    & Region() = Flemish_Region
.

Tax() = 10 =>
    Region() = Flemish_Region
    & Registration_Type() = Other
.

[The tax rate is 12% only in Brussels and Wallonia](
Tax() = 12 =>
    Region() = Brussels_Region
    | Region() = Walloon_Region
).

//? x[Int]: Tax = x.

// registration types currently only defined for Flanders.
// When a choice is made for walonia or brussels, types can still be entered with a view to expandability


Registration_Type() = Family_Dwelling =>
    Type_Of_Real_Estate() = Residential
    & Buyer() = Natural_Person
    & Domicile_Established()
    & Clean_Purchase()
    & (First_Ownership() | Causal_Connection())
    & (~ Energy_Renovation_Planned() | Term_Energy_Renovation() ~= Certification_Date() + 5)
.

Registration_Type() = Social_Dwelling =>
    Buyer() = Natural_Person
    & Type_Of_Real_Estate() = Residential
    & Use() = Social_Housing
    & (Seller ()= Vlaamse_Mpy_Voor_Sociaal_Wonen | Seller() = ErkendeSocialeHuisvestingsMpy)
    & Mortgage_Loan_Allowance()
.

Registration_Type() = Energy_Efficient_Dwelling =>
    Type_Of_Real_Estate() = Residential
    & Buyer() = Natural_Person
    & Domicile_Established()
    & Clean_Purchase()
    & (First_Ownership() | Causal_Connection())
    & Energy_Renovation_Planned()
    & Term_Energy_Renovation() = Certification_Date() + 5
.

Registration_Type() = Dwelling_For_Social_Renting =>
    Type_Of_Real_Estate() = Residential
    & Use() = Social_Renting
    & Start_Dt_Dwelling_For_Social_Rent() = Certification_Date() + 3
    & Duration_Of_Agreement() = Less_Than_9_years
.

[An Heritage is a residential monument in an heritage plan (with additional terms), used as family dwelling]
(Registration_Type() = Heritage =>
    Type_Of_Real_Estate() = Residential
    & Monument()
    & Use() = As_Family_Dwelling
    & Heritage_Investment()
    & Heritage_Plan()
    & Additional_Terms())
.

Registration_Type() = Professional_Purchase =>
    Professional_Buyer()
    & Transaction_Type()  ~= Public_Sale
    & Use() = For_Resale
    & Certification_Date_Sale() = Certification_Date() + 8
.

[A sale by the Vlaams Woning Fonds for community purpose is for social purpose.](
Registration_Type() = Social_Purpose =>
    (Seller() = Mpy_Erkend_Door_VMSW
    | Seller() = Vlaams_Woningfonds
    | Seller() = Gelijksoortige_Rechtspersoon_EER)
    & Use() = Community_Purpose
).

Registration_Type() = Exchange_Unbuilt_Ground =>
    Additional_Terms()
    & ~Monument().

Registration_Type() = Other =>     // @EXPLAIN: Registration_Type cannot be Other
    Registration_Type() ~= Family_Dwelling
    & Registration_Type() ~= Social_Dwelling
    & Registration_Type() ~= Energy_Efficient_Dwelling
    & Registration_Type() ~= Dwelling_For_Social_Renting
    & Registration_Type() ~= Heritage
    & Registration_Type() ~= Professional_Purchase
    & Registration_Type() ~= Social_Purpose
    & Registration_Type() ~= Exchange_Unbuilt_Ground
.


//? x[registration_Type]: Registration_Type = x.


}

display {
    goal_symbol:={`Tax}.
    expand := {`Tax}.
    view() = normal.
}
-- meta -------------------------------------
{'manualPropagation': False,
 'manualRelevance': False,
 'optionalPropagation': False,
 'optionalRelevance': False,
 'symbols': [{'environmental': True,
              'idpname': 'Region',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': True,
              'idpname': 'Municipality',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': True,
              'idpname': 'Type_Of_Real_Estate',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': True,
              'idpname': 'Seller',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': True,
              'idpname': 'Buyer',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': True,
              'idpname': 'Use',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': True,
              'idpname': 'Domicile_Established',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': True,
              'idpname': 'First_Ownership',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': True,
              'idpname': 'Monument',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': True,
              'idpname': 'Resale',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': True,
              'idpname': 'Transaction_Type',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': True,
              'idpname': 'Duration_Of_Agreement',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': True,
              'idpname': 'Core_City',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': True,
              'idpname': 'Mortgage_Loan_Allowance',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': True,
              'idpname': 'Clean_Purchase',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': True,
              'idpname': 'Causal_Connection',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': True,
              'idpname': 'Energy_Renovation_Planned',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': True,
              'idpname': 'Heritage_Investment',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': True,
              'idpname': 'Heritage_Plan',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': True,
              'idpname': 'Professional_Declaration_Filed',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': True,
              'idpname': 'Guarantee_Satisfied',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': True,
              'idpname': 'Additional_Security_Required',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': True,
              'idpname': 'Additional_Security_Satisfied',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': True,
              'idpname': 'Additional_Terms',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': True,
              'idpname': 'Start_Dt_Dwelling_For_Social_Rent',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': True,
              'idpname': 'Certification_Date',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': True,
              'idpname': 'Term_Energy_Renovation',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': True,
              'idpname': 'Certification_Date_Sale',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': True,
              'idpname': 'Professional_Buyer',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Registration_Type',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Tax',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': True},
 'Additional_Security_Required': {'Additional_Security_Required()': {'environmental': True,
                                                                     'is_assignment': False,
                                                                     'normal': True,
                                                                     'reading': 'Additional_Security_Required',
                                                                     'relevant': True,
                                                                     'status': 'UNKNOWN',
                                                                     'typ': 'Bool'}},
 'Additional_Security_Satisfied': {'Additional_Security_Satisfied()': {'environmental': True,
                                                                       'is_assignment': False,
                                                                       'normal': True,
                                                                       'reading': 'Additional_Security_Satisfied',
                                                                       'relevant': True,
                                                                       'status': 'UNKNOWN',
                                                                       'typ': 'Bool'}},
 'Additional_Terms': {'Additional_Terms()': {'environmental': True,
                                             'is_assignment': False,
                                             'normal': True,
                                             'reading': 'Additional_Terms',
                                             'relevant': True,
                                             'status': 'UNKNOWN',
                                             'typ': 'Bool'}},
 'Buyer': {'Buyer()': {'environmental': True,
                       'is_assignment': True,
                       'normal': True,
                       'reading': 'Buyer',
                       'relevant': True,
                       'status': 'UNKNOWN',
                       'typ': 'buyerType',
                       'value': '',
                       'values': ['Natural_Person', 'Legal_Person', 'Mixed']},
           'Buyer() = Natural_Person': {'environmental': True,
                                        'is_assignment': True,
                                        'normal': False,
                                        'reading': 'Buyer = Natural_Person',
                                        'relevant': True,
                                        'status': 'UNKNOWN',
                                        'typ': 'Bool'}},
 'Causal_Connection': {'Causal_Connection()': {'environmental': True,
                                               'is_assignment': False,
                                               'normal': True,
                                               'reading': 'Causal_Connection',
                                               'relevant': True,
                                               'status': 'UNKNOWN',
                                               'typ': 'Bool'}},
 'Certification_Date': {'Certification_Date()': {'environmental': True,
                                                 'is_assignment': True,
                                                 'normal': True,
                                                 'reading': 'Certification_Date',
                                                 'relevant': True,
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
 'Certification_Date_Sale': {'Certification_Date_Sale()': {'environmental': True,
                                                           'is_assignment': True,
                                                           'normal': True,
                                                           'reading': 'Certification_Date_Sale',
                                                           'relevant': True,
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
                             'Certification_Date_Sale() = Certification_Date() + 8': {'environmental': True,
                                                                                      'is_assignment': False,
                                                                                      'normal': False,
                                                                                      'reading': 'Certification_Date_Sale '
                                                                                                 '= Certification_Date '
                                                                                                 '+ 8',
                                                                                      'relevant': True,
                                                                                      'status': 'UNKNOWN',
                                                                                      'typ': 'Bool'}},
 'Clean_Purchase': {'Clean_Purchase()': {'environmental': True,
                                         'is_assignment': False,
                                         'normal': True,
                                         'reading': 'Clean_Purchase',
                                         'relevant': True,
                                         'status': 'UNKNOWN',
                                         'typ': 'Bool'}},
 'Core_City': {'Core_City()': {'environmental': True,
                               'is_assignment': False,
                               'normal': True,
                               'reading': 'Core_City',
                               'relevant': False,
                               'status': 'UNKNOWN',
                               'typ': 'Bool'}},
 'Domicile_Established': {'Domicile_Established()': {'environmental': True,
                                                     'is_assignment': False,
                                                     'normal': True,
                                                     'reading': 'Domicile_Established',
                                                     'relevant': True,
                                                     'status': 'UNKNOWN',
                                                     'typ': 'Bool'}},
 'Duration_Of_Agreement': {'Duration_Of_Agreement()': {'environmental': True,
                                                       'is_assignment': True,
                                                       'normal': True,
                                                       'reading': 'Duration_Of_Agreement',
                                                       'relevant': True,
                                                       'status': 'UNKNOWN',
                                                       'typ': 'agreementDwellingForSocialRenting',
                                                       'value': '',
                                                       'values': ['Less_Than_9_years', 'More_than_9_Or_9_years']},
                           'Duration_Of_Agreement() = Less_Than_9_years': {'environmental': True,
                                                                           'is_assignment': True,
                                                                           'normal': False,
                                                                           'reading': 'Duration_Of_Agreement = '
                                                                                      'Less_Than_9_years',
                                                                           'relevant': True,
                                                                           'status': 'UNKNOWN',
                                                                           'typ': 'Bool'}},
 'Energy_Renovation_Planned': {'Energy_Renovation_Planned()': {'environmental': True,
                                                               'is_assignment': False,
                                                               'normal': True,
                                                               'reading': 'Energy_Renovation_Planned',
                                                               'relevant': True,
                                                               'status': 'UNKNOWN',
                                                               'typ': 'Bool'}},
 'First_Ownership': {'First_Ownership()': {'environmental': True,
                                           'is_assignment': False,
                                           'normal': True,
                                           'reading': 'First_Ownership',
                                           'relevant': True,
                                           'status': 'UNKNOWN',
                                           'typ': 'Bool'}},
 'Guarantee_Satisfied': {'Guarantee_Satisfied()': {'environmental': True,
                                                   'is_assignment': False,
                                                   'normal': True,
                                                   'reading': 'Guarantee_Satisfied',
                                                   'relevant': True,
                                                   'status': 'UNKNOWN',
                                                   'typ': 'Bool'}},
 'Heritage_Investment': {'Heritage_Investment()': {'environmental': True,
                                                   'is_assignment': False,
                                                   'normal': True,
                                                   'reading': 'Heritage_Investment',
                                                   'relevant': True,
                                                   'status': 'UNKNOWN',
                                                   'typ': 'Bool'}},
 'Heritage_Plan': {'Heritage_Plan()': {'environmental': True,
                                       'is_assignment': False,
                                       'normal': True,
                                       'reading': 'Heritage_Plan',
                                       'relevant': True,
                                       'status': 'UNKNOWN',
                                       'typ': 'Bool'}},
 'Monument': {'Monument()': {'environmental': True,
                             'is_assignment': False,
                             'normal': True,
                             'reading': 'Monument',
                             'relevant': True,
                             'status': 'UNKNOWN',
                             'typ': 'Bool'}},
 'Mortgage_Loan_Allowance': {'Mortgage_Loan_Allowance()': {'environmental': True,
                                                           'is_assignment': False,
                                                           'normal': True,
                                                           'reading': 'Mortgage_Loan_Allowance',
                                                           'relevant': True,
                                                           'status': 'UNKNOWN',
                                                           'typ': 'Bool'}},
 'Municipality': {'Municipality()': {'environmental': True,
                                     'is_assignment': True,
                                     'normal': True,
                                     'reading': 'Municipality',
                                     'relevant': False,
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
                                                'Tervuren']}},
 'Professional_Buyer': {'Professional_Buyer()': {'environmental': True,
                                                 'is_assignment': False,
                                                 'normal': True,
                                                 'reading': 'Professional_Buyer',
                                                 'relevant': True,
                                                 'status': 'UNKNOWN',
                                                 'typ': 'Bool'}},
 'Professional_Declaration_Filed': {'Professional_Declaration_Filed()': {'environmental': True,
                                                                         'is_assignment': False,
                                                                         'normal': True,
                                                                         'reading': 'Professional_Declaration_Filed',
                                                                         'relevant': True,
                                                                         'status': 'UNKNOWN',
                                                                         'typ': 'Bool'}},
 'Region': {'Region()': {'environmental': True,
                         'is_assignment': True,
                         'normal': True,
                         'reading': 'Region',
                         'relevant': True,
                         'status': 'UNKNOWN',
                         'typ': 'location',
                         'value': '',
                         'values': ['Flemish_Region', 'Walloon_Region', 'Brussels_Region']},
            'Region() = Brussels_Region': {'environmental': True,
                                           'is_assignment': True,
                                           'normal': False,
                                           'reading': 'Region = Brussels_Region',
                                           'relevant': True,
                                           'status': 'UNKNOWN',
                                           'typ': 'Bool'},
            'Region() = Flemish_Region': {'environmental': True,
                                          'is_assignment': True,
                                          'normal': False,
                                          'reading': 'Region = Flemish_Region',
                                          'relevant': True,
                                          'status': 'UNKNOWN',
                                          'typ': 'Bool'},
            'Region() = Walloon_Region': {'environmental': True,
                                          'is_assignment': True,
                                          'normal': False,
                                          'reading': 'Region = Walloon_Region',
                                          'relevant': True,
                                          'status': 'UNKNOWN',
                                          'typ': 'Bool'}},
 'Registration_Type': {'Registration_Type()': {'environmental': False,
                                               'is_assignment': True,
                                               'normal': True,
                                               'reading': 'Registration_Type',
                                               'relevant': True,
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
                       'Registration_Type() = Dwelling_For_Social_Renting': {'environmental': False,
                                                                             'is_assignment': True,
                                                                             'normal': False,
                                                                             'reading': 'Registration_Type = '
                                                                                        'Dwelling_For_Social_Renting',
                                                                             'relevant': True,
                                                                             'status': 'UNKNOWN',
                                                                             'typ': 'Bool'},
                       'Registration_Type() = Energy_Efficient_Dwelling': {'environmental': False,
                                                                           'is_assignment': True,
                                                                           'normal': False,
                                                                           'reading': 'Registration_Type = '
                                                                                      'Energy_Efficient_Dwelling',
                                                                           'relevant': True,
                                                                           'status': 'UNKNOWN',
                                                                           'typ': 'Bool'},
                       'Registration_Type() = Exchange_Unbuilt_Ground': {'environmental': False,
                                                                         'is_assignment': True,
                                                                         'normal': False,
                                                                         'reading': 'Registration_Type = '
                                                                                    'Exchange_Unbuilt_Ground',
                                                                         'relevant': True,
                                                                         'status': 'UNKNOWN',
                                                                         'typ': 'Bool'},
                       'Registration_Type() = Family_Dwelling': {'environmental': False,
                                                                 'is_assignment': True,
                                                                 'normal': False,
                                                                 'reading': 'Registration_Type = Family_Dwelling',
                                                                 'relevant': True,
                                                                 'status': 'UNKNOWN',
                                                                 'typ': 'Bool'},
                       'Registration_Type() = Heritage': {'environmental': False,
                                                          'is_assignment': True,
                                                          'normal': False,
                                                          'reading': 'Registration_Type = Heritage',
                                                          'relevant': True,
                                                          'status': 'UNKNOWN',
                                                          'typ': 'Bool'},
                       'Registration_Type() = Other': {'environmental': False,
                                                       'is_assignment': True,
                                                       'normal': False,
                                                       'reading': 'Registration_Type = Other',
                                                       'relevant': True,
                                                       'status': 'UNKNOWN',
                                                       'typ': 'Bool'},
                       'Registration_Type() = Professional_Purchase': {'environmental': False,
                                                                       'is_assignment': True,
                                                                       'normal': False,
                                                                       'reading': 'Registration_Type = '
                                                                                  'Professional_Purchase',
                                                                       'relevant': True,
                                                                       'status': 'UNKNOWN',
                                                                       'typ': 'Bool'},
                       'Registration_Type() = Social_Dwelling': {'environmental': False,
                                                                 'is_assignment': True,
                                                                 'normal': False,
                                                                 'reading': 'Registration_Type = Social_Dwelling',
                                                                 'relevant': True,
                                                                 'status': 'UNKNOWN',
                                                                 'typ': 'Bool'},
                       'Registration_Type() = Social_Purpose': {'environmental': False,
                                                                'is_assignment': True,
                                                                'normal': False,
                                                                'reading': 'Registration_Type = Social_Purpose',
                                                                'relevant': True,
                                                                'status': 'UNKNOWN',
                                                                'typ': 'Bool'}},
 'Resale': {'Resale()': {'environmental': True,
                         'is_assignment': True,
                         'normal': True,
                         'reading': 'Resale',
                         'relevant': True,
                         'status': 'UNKNOWN',
                         'typ': 'resale',
                         'value': '',
                         'values': ['Less_Than_Three', 'Three_Or_More']},
            'Resale() = Three_Or_More': {'environmental': True,
                                         'is_assignment': True,
                                         'normal': False,
                                         'reading': 'Resale = Three_Or_More',
                                         'relevant': True,
                                         'status': 'UNKNOWN',
                                         'typ': 'Bool'}},
 'Seller': {'Seller()': {'environmental': True,
                         'is_assignment': True,
                         'normal': True,
                         'reading': 'Seller',
                         'relevant': True,
                         'status': 'UNKNOWN',
                         'typ': 'seller',
                         'value': '',
                         'values': ['Vlaams_Woningfonds',
                                    'Gelijksoortige_Rechtspersoon_EER',
                                    'Mpy_Erkend_Door_VMSW',
                                    'Vlaamse_Mpy_Voor_Sociaal_Wonen',
                                    'ErkendeSocialeHuisvestingsMpy']},
            'Seller() = ErkendeSocialeHuisvestingsMpy': {'environmental': True,
                                                         'is_assignment': True,
                                                         'normal': False,
                                                         'reading': 'Seller = ErkendeSocialeHuisvestingsMpy',
                                                         'relevant': True,
                                                         'status': 'UNKNOWN',
                                                         'typ': 'Bool'},
            'Seller() = Gelijksoortige_Rechtspersoon_EER': {'environmental': True,
                                                            'is_assignment': True,
                                                            'normal': False,
                                                            'reading': 'Seller = Gelijksoortige_Rechtspersoon_EER',
                                                            'relevant': True,
                                                            'status': 'UNKNOWN',
                                                            'typ': 'Bool'},
            'Seller() = Mpy_Erkend_Door_VMSW': {'environmental': True,
                                                'is_assignment': True,
                                                'normal': False,
                                                'reading': 'Seller = Mpy_Erkend_Door_VMSW',
                                                'relevant': True,
                                                'status': 'UNKNOWN',
                                                'typ': 'Bool'},
            'Seller() = Vlaams_Woningfonds': {'environmental': True,
                                              'is_assignment': True,
                                              'normal': False,
                                              'reading': 'Seller = Vlaams_Woningfonds',
                                              'relevant': True,
                                              'status': 'UNKNOWN',
                                              'typ': 'Bool'},
            'Seller() = Vlaamse_Mpy_Voor_Sociaal_Wonen': {'environmental': True,
                                                          'is_assignment': True,
                                                          'normal': False,
                                                          'reading': 'Seller = Vlaamse_Mpy_Voor_Sociaal_Wonen',
                                                          'relevant': True,
                                                          'status': 'UNKNOWN',
                                                          'typ': 'Bool'}},
 'Start_Dt_Dwelling_For_Social_Rent': {'Start_Dt_Dwelling_For_Social_Rent()': {'environmental': True,
                                                                               'is_assignment': True,
                                                                               'normal': True,
                                                                               'reading': 'Start_Dt_Dwelling_For_Social_Rent',
                                                                               'relevant': True,
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
                                       'Start_Dt_Dwelling_For_Social_Rent() = Certification_Date() + 3': {'environmental': True,
                                                                                                          'is_assignment': False,
                                                                                                          'normal': False,
                                                                                                          'reading': 'Start_Dt_Dwelling_For_Social_Rent '
                                                                                                                     '= '
                                                                                                                     'Certification_Date '
                                                                                                                     '+ '
                                                                                                                     '3',
                                                                                                          'relevant': True,
                                                                                                          'status': 'UNKNOWN',
                                                                                                          'typ': 'Bool'}},
 'Tax': {'Tax()': {'environmental': False,
                   'is_assignment': True,
                   'normal': True,
                   'reading': 'Tax',
                   'relevant': True,
                   'status': 'UNKNOWN',
                   'typ': 'Int',
                   'value': '',
                   'values': ['1', '2', '4', '7', '6', '10', '12']},
         'Tax() = 1': {'environmental': False,
                       'is_assignment': True,
                       'normal': False,
                       'reading': 'Tax = 1',
                       'relevant': True,
                       'status': 'UNKNOWN',
                       'typ': 'Bool'},
         'Tax() = 10': {'environmental': False,
                        'is_assignment': True,
                        'normal': False,
                        'reading': 'Tax = 10',
                        'relevant': True,
                        'status': 'UNKNOWN',
                        'typ': 'Bool'},
         'Tax() = 12': {'environmental': False,
                        'is_assignment': True,
                        'normal': False,
                        'reading': 'Tax = 12',
                        'relevant': True,
                        'status': 'UNKNOWN',
                        'typ': 'Bool'},
         'Tax() = 2': {'environmental': False,
                       'is_assignment': True,
                       'normal': False,
                       'reading': 'Tax = 2',
                       'relevant': True,
                       'status': 'UNKNOWN',
                       'typ': 'Bool'},
         'Tax() = 4': {'environmental': False,
                       'is_assignment': True,
                       'normal': False,
                       'reading': 'Tax = 4',
                       'relevant': True,
                       'status': 'UNKNOWN',
                       'typ': 'Bool'},
         'Tax() = 6': {'environmental': False,
                       'is_assignment': True,
                       'normal': False,
                       'reading': 'Tax = 6',
                       'relevant': True,
                       'status': 'UNKNOWN',
                       'typ': 'Bool'},
         'Tax() = 7': {'environmental': False,
                       'is_assignment': True,
                       'normal': False,
                       'reading': 'Tax = 7',
                       'relevant': True,
                       'status': 'UNKNOWN',
                       'typ': 'Bool'}},
 'Term_Energy_Renovation': {'Term_Energy_Renovation()': {'environmental': True,
                                                         'is_assignment': True,
                                                         'normal': True,
                                                         'reading': 'Term_Energy_Renovation',
                                                         'relevant': True,
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
                            'Term_Energy_Renovation() = Certification_Date() + 5': {'environmental': True,
                                                                                    'is_assignment': False,
                                                                                    'normal': False,
                                                                                    'reading': 'Term_Energy_Renovation '
                                                                                               '= Certification_Date + '
                                                                                               '5',
                                                                                    'relevant': True,
                                                                                    'status': 'UNKNOWN',
                                                                                    'typ': 'Bool'}},
 'Transaction_Type': {'Transaction_Type()': {'environmental': True,
                                             'is_assignment': True,
                                             'normal': True,
                                             'reading': 'Transaction_Type',
                                             'relevant': True,
                                             'status': 'UNKNOWN',
                                             'typ': 'transaction',
                                             'value': '',
                                             'values': ['Public_Sale', 'Out_Hand', 'Public_Sale_Community']},
                      'Transaction_Type() = Public_Sale': {'environmental': True,
                                                           'is_assignment': True,
                                                           'normal': False,
                                                           'reading': 'Transaction_Type = Public_Sale',
                                                           'relevant': True,
                                                           'status': 'UNKNOWN',
                                                           'typ': 'Bool'}},
 'Type_Of_Real_Estate': {'Type_Of_Real_Estate()': {'environmental': True,
                                                   'is_assignment': True,
                                                   'normal': True,
                                                   'reading': 'Type_Of_Real_Estate',
                                                   'relevant': True,
                                                   'status': 'UNKNOWN',
                                                   'typ': 'real_Estate_Type',
                                                   'value': '',
                                                   'values': ['Residential',
                                                              'Residential_Building_Land',
                                                              'Other_Real_Estate']},
                         'Type_Of_Real_Estate() = Residential': {'environmental': True,
                                                                 'is_assignment': True,
                                                                 'normal': False,
                                                                 'reading': 'Type_Of_Real_Estate = Residential',
                                                                 'relevant': True,
                                                                 'status': 'UNKNOWN',
                                                                 'typ': 'Bool'}},
 'Use': {'Use()': {'environmental': True,
                   'is_assignment': True,
                   'normal': True,
                   'reading': 'Use',
                   'relevant': True,
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
         'Use() = As_Family_Dwelling': {'environmental': True,
                                        'is_assignment': True,
                                        'normal': False,
                                        'reading': 'Use = As_Family_Dwelling',
                                        'relevant': True,
                                        'status': 'UNKNOWN',
                                        'typ': 'Bool'},
         'Use() = Community_Purpose': {'environmental': True,
                                       'is_assignment': True,
                                       'normal': False,
                                       'reading': 'Use = Community_Purpose',
                                       'relevant': True,
                                       'status': 'UNKNOWN',
                                       'typ': 'Bool'},
         'Use() = For_Resale': {'environmental': True,
                                'is_assignment': True,
                                'normal': False,
                                'reading': 'Use = For_Resale',
                                'relevant': True,
                                'status': 'UNKNOWN',
                                'typ': 'Bool'},
         'Use() = Social_Housing': {'environmental': True,
                                    'is_assignment': True,
                                    'normal': False,
                                    'reading': 'Use = Social_Housing',
                                    'relevant': True,
                                    'status': 'UNKNOWN',
                                    'typ': 'Bool'},
         'Use() = Social_Renting': {'environmental': True,
                                    'is_assignment': True,
                                    'normal': False,
                                    'reading': 'Use = Social_Renting',
                                    'relevant': True,
                                    'status': 'UNKNOWN',
                                    'typ': 'Bool'}}}
