
-- original ---------------------------------
vocabulary environment {
type location constructed from {Flemish_Region, Walloon_Region, Brussels_Region}

type real_Estate_Type constructed from {Residential, Residential_Building_Land, Other_Real_Estate}

type destination constructed from {As_Family_Dwelling, For_Resale, Community_Purpose, Social_Housing, Social_Renting, Other_House, No_House}
type buyerType constructed from {Natural_Person, Legal_Person, Mixed}

type calculationBase = {190; 200; 210; 220; 225}
type baseLimit = {200; 220}
//type DiscountType = {56; 48; 0}

type date = {2015..2025}

type agreementDwellingForSocialRenting constructed from {Less_Than_9_years, More_than_9_Or_9_years}

type transaction constructed from {Public_Sale, Out_Hand, Public_Sale_Community}



type municipality constructed from {other_Municipal, Aalst, Antwerpen, Boom, Brugge, Dendermonde, Genk, Gent, Hasselt, Kortrijk, Leuven, Mechelen, Oostende, Roeselare, SintNiklaas, Turnhout, Vilvoorde, Affligem, Asse, Beersel, Bever, Dilbeek, Drogenbos, Galmaarden, Gooik, Grimbergen, Halle, Herne, Hoeilaart, Kampenhout, KapelleopdenBos, Kraainem, Lennik, Liedekerke, Linkebeek, Londerzeel, Machelen, Meise, Merchtem, Opwijk, Overijse, Pepingen, Roosdaal, SintGenesiusRode, SintPietersLeeuw, Steenokkerzeel, Ternat, Wemmel, WezembeekOppem, Zaventem, Zemst, Bertem, Huldenberg, Kortenberg, Tervuren}

type resale constructed from {Less_Than_Three, Three_Or_More}


type seller constructed from {Vlaams_Woningfonds, Gelijksoortige_Rechtspersoon_EER, Mpy_Erkend_Door_VMSW, Vlaamse_Mpy_Voor_Sociaal_Wonen, ErkendeSocialeHuisvestingsMpy}


////////////////////////

Region : location
Municipality : municipality
Type_Of_Real_Estate : real_Estate_Type
Seller : seller
Buyer : buyerType
Use : destination

Domicile_Established
First_Ownership
Monument

Resale : resale
Transaction_Type : transaction
Duration_Of_Agreement : agreementDwellingForSocialRenting

Core_City

//SocialSeller
Mortgage_Loan_Allowance
Clean_Purchase
Causal_Connection


Energy_Renovation_Planned

//SocialRentingAgreement
Heritage_Investment
Heritage_Plan
//AdditionalConditions

Professional_Declaration_Filed
Guarantee_Satisfied
Additional_Security_Required
Additional_Security_Satisfied

//TaxableBase : calculationBase
//PermittedBase : baseLimit

Additional_Terms


Start_Dt_Dwelling_For_Social_Rent : date

Certification_Date : date

Term_Energy_Renovation : date
Certification_Date_Sale : date
//DomicileDate : date

//IsDiscount: DiscountType
Professional_Buyer
}

vocabulary decision {
type registration_Type constructed from {Family_Dwelling, Social_Dwelling, Social_Purpose, Exchange_Unbuilt_Ground, Professional_Purchase, Energy_Efficient_Dwelling, Heritage, Dwelling_For_Social_Renting, Other}
type tax_Rate = {1; 2; 4; 7; 6; 10; 12}

Registration_Type : registration_Type
Tax : tax_Rate
}

theory {

     // Tax

[Registration rate for heritage in Flemish Region is 1%.](
Tax = 1 =>
    Registration_Type = Heritage
    & Region = Flemish_Region
).

Tax = 2 => // correct amount is 1; 5
    Registration_Type = Social_Dwelling
    & Region = Flemish_Region
.

Tax = 4 =>
    Registration_Type = Professional_Purchase
    & Region = Flemish_Region
.

[The tax rate is 6% for social purpose sales in the Flemish Region.]
(Tax = 6 =>
    (Registration_Type = Energy_Efficient_Dwelling
    | Registration_Type = Social_Purpose
    | Registration_Type = Exchange_Unbuilt_Ground)
    & Region = Flemish_Region
).

Tax = 7 =>
    (Registration_Type = Family_Dwelling
    | Registration_Type = Dwelling_For_Social_Renting)
    & Region = Flemish_Region
.

Tax = 10 =>
    Region = Flemish_Region
    & Registration_Type = Other
.

[The tax rate is 12% only in Brussels and Wallonia](
Tax = 12 =>
    Region = Brussels_Region
    | Region = Walloon_Region
).

//? x[int]: Tax = x.

// registration types currently only defined for Flanders.
// When a choice is made for walonia or brussels, types can still be entered with a view to expandability


Registration_Type = Family_Dwelling =>
    Type_Of_Real_Estate = Residential
    & Buyer = Natural_Person
    & Domicile_Established
    & Clean_Purchase
    & (First_Ownership | Causal_Connection)
    & (~ Energy_Renovation_Planned | Term_Energy_Renovation ~= Certification_Date + 5)
.

Registration_Type = Social_Dwelling =>     
    Buyer = Natural_Person
    & Type_Of_Real_Estate = Residential
    & Use = Social_Housing
    & (Seller = Vlaamse_Mpy_Voor_Sociaal_Wonen | Seller = ErkendeSocialeHuisvestingsMpy)
    & Mortgage_Loan_Allowance
.

Registration_Type = Energy_Efficient_Dwelling =>
    Type_Of_Real_Estate = Residential
    & Buyer = Natural_Person
    & Domicile_Established
    & Clean_Purchase
    & (First_Ownership | Causal_Connection)
    & Energy_Renovation_Planned
    & Term_Energy_Renovation = Certification_Date + 5
.

Registration_Type = Dwelling_For_Social_Renting =>
    Type_Of_Real_Estate = Residential
    & Use = Social_Renting
    & Start_Dt_Dwelling_For_Social_Rent = Certification_Date + 3
    & Duration_Of_Agreement = Less_Than_9_years
.

[An Heritage is a residential monument in an heritage plan (with additional terms), used as family dwelling]
(Registration_Type = Heritage =>
    Type_Of_Real_Estate = Residential
    & Monument
    & Use = As_Family_Dwelling
    & Heritage_Investment
    & Heritage_Plan
    & Additional_Terms)
.

Registration_Type = Professional_Purchase => 
    Professional_Buyer
    & Transaction_Type  ~= Public_Sale
    & Use = For_Resale
    & Certification_Date_Sale = Certification_Date + 8
.

[A sale by the Vlaams Woning Fonds for community purpose is for social purpose.](
Registration_Type = Social_Purpose =>     
    (Seller = Mpy_Erkend_Door_VMSW
    | Seller = Vlaams_Woningfonds
    | Seller = Gelijksoortige_Rechtspersoon_EER)
    & Use = Community_Purpose
).

Registration_Type = Exchange_Unbuilt_Ground => 
    Additional_Terms
    & ~Monument.

Registration_Type = Other =>     // @EXPLAIN: Registration_Type cannot be Other
    Registration_Type ~= Family_Dwelling
    & Registration_Type ~= Social_Dwelling
    & Registration_Type ~= Energy_Efficient_Dwelling
    & Registration_Type ~= Dwelling_For_Social_Renting
    & Registration_Type ~= Heritage
    & Registration_Type ~= Professional_Purchase
    & Registration_Type ~= Social_Purpose
    & Registration_Type ~= Exchange_Unbuilt_Ground
.


//? x[registration_Type]: Registration_Type = x.




    
{ Professional_Buyer <-
    Professional_Declaration_Filed
    & Guarantee_Satisfied
    & (Additional_Security_Required & Additional_Security_Satisfied
    | ~ Additional_Security_Required)
    & Resale = Three_Or_More
.}
~Professional_Declaration_Filed.
}

goal Tax
view normal
-- vocabulary -------------------------------

-- theory -----------------------------------
Or(Not(Tax == 1),
   And(Registration_Type == Heritage,
       Region == Flemish_Region))

Or(Not(Tax == 2),
   And(Registration_Type == Social_Dwelling,
       Region == Flemish_Region))

Or(Not(Tax == 4),
   And(Registration_Type == Professional_Purchase,
       Region == Flemish_Region))

Or(Not(Tax == 6),
   And(Or(Registration_Type == Energy_Efficient_Dwelling,
          Registration_Type == Social_Purpose,
          Registration_Type == Exchange_Unbuilt_Ground),
       Region == Flemish_Region))

Or(Not(Tax == 7),
   And(Or(Registration_Type == Family_Dwelling,
          Registration_Type == Dwelling_For_Social_Renting),
       Region == Flemish_Region))

Or(Not(Tax == 10),
   And(Region == Flemish_Region, Registration_Type == Other))

Or(Not(Tax == 12),
   Or(Region == Brussels_Region, Region == Walloon_Region))

Or(Not(Registration_Type == Family_Dwelling),
   And(Type_Of_Real_Estate == Residential,
       Buyer == Natural_Person,
       Domicile_Established,
       Clean_Purchase,
       Or(First_Ownership, Causal_Connection),
       Or(Not(Energy_Renovation_Planned),
          Not(Term_Energy_Renovation ==
              5 + Certification_Date))))

Or(Not(Registration_Type == Social_Dwelling),
   And(Buyer == Natural_Person,
       Type_Of_Real_Estate == Residential,
       Use == Social_Housing,
       Or(Seller == Vlaamse_Mpy_Voor_Sociaal_Wonen,
          Seller == ErkendeSocialeHuisvestingsMpy),
       Mortgage_Loan_Allowance))

Or(Not(Registration_Type == Energy_Efficient_Dwelling),
   And(Type_Of_Real_Estate == Residential,
       Buyer == Natural_Person,
       Domicile_Established,
       Clean_Purchase,
       Or(First_Ownership, Causal_Connection),
       Energy_Renovation_Planned,
       Term_Energy_Renovation == 5 + Certification_Date))

Or(Not(Registration_Type == Dwelling_For_Social_Renting),
   And(Type_Of_Real_Estate == Residential,
       Use == Social_Renting,
       Start_Dt_Dwelling_For_Social_Rent ==
       3 + Certification_Date,
       Duration_Of_Agreement == Less_Than_9_years))

Or(Not(Registration_Type == Heritage),
   And(Type_Of_Real_Estate == Residential,
       Monument,
       Use == As_Family_Dwelling,
       Heritage_Investment,
       Heritage_Plan,
       Additional_Terms))

Or(Not(Registration_Type == Professional_Purchase),
   And(Professional_Buyer,
       Not(Transaction_Type == Public_Sale),
       Use == For_Resale,
       Certification_Date_Sale == 8 + Certification_Date))

Or(Not(Registration_Type == Social_Purpose),
   And(Or(Seller == Mpy_Erkend_Door_VMSW,
          Seller == Vlaams_Woningfonds,
          Seller == Gelijksoortige_Rechtspersoon_EER),
       Use == Community_Purpose))

Or(Not(Registration_Type == Exchange_Unbuilt_Ground),
   And(Additional_Terms, Not(Monument)))

Or(Not(Registration_Type == Other),
   And(Not(Registration_Type == Family_Dwelling),
       Not(Registration_Type == Social_Dwelling),
       Not(Registration_Type == Energy_Efficient_Dwelling),
       Not(Registration_Type == Dwelling_For_Social_Renting),
       Not(Registration_Type == Heritage),
       Not(Registration_Type == Professional_Purchase),
       Not(Registration_Type == Social_Purpose),
       Not(Registration_Type == Exchange_Unbuilt_Ground)))

Not(Professional_Declaration_Filed)

And(Start_Dt_Dwelling_For_Social_Rent >= 2015,
    Start_Dt_Dwelling_For_Social_Rent <= 2025)

And(Certification_Date >= 2015, Certification_Date <= 2025)

And(Term_Energy_Renovation >= 2015,
    Term_Energy_Renovation <= 2025)

And(Certification_Date_Sale >= 2015,
    Certification_Date_Sale <= 2025)

Or(Tax == 1,
   Tax == 2,
   Tax == 4,
   Tax == 7,
   Tax == 6,
   Tax == 10,
   Tax == 12)

Professional_Buyer ==
And(Professional_Declaration_Filed,
    Guarantee_Satisfied,
    Or(And(Additional_Security_Required,
           Additional_Security_Satisfied),
       Not(Additional_Security_Required)),
    Resale == Three_Or_More)

-- subtences ------------------------------------
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
Domicile_Established
Clean_Purchase
First_Ownership
Causal_Connection
Energy_Renovation_Planned
Term_Energy_Renovation = (Certification_Date + 5)
Use = Social_Housing
Seller = Vlaamse_Mpy_Voor_Sociaal_Wonen
Seller = ErkendeSocialeHuisvestingsMpy
Mortgage_Loan_Allowance
Use = Social_Renting
Start_Dt_Dwelling_For_Social_Rent = (Certification_Date + 3)
Duration_Of_Agreement = Less_Than_9_years
Monument
Use = As_Family_Dwelling
Heritage_Investment
Heritage_Plan
Additional_Terms
Professional_Buyer
Professional_Declaration_Filed
Guarantee_Satisfied
Additional_Security_Required
Additional_Security_Satisfied
Resale = Three_Or_More
Transaction_Type = Public_Sale
Use = For_Resale
Certification_Date_Sale = (Certification_Date + 8)
Seller = Mpy_Erkend_Door_VMSW
Seller = Vlaams_Woningfonds
Seller = Gelijksoortige_Rechtspersoon_EER
Use = Community_Purpose

-- GUILines ------------------------------------
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
Term_Energy_Renovation
Certification_Date_Sale
Professional_Buyer
Registration_Type
Tax
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
Resale = Three_Or_More
Transaction_Type = Public_Sale
Use = For_Resale
Certification_Date_Sale = (Certification_Date + 8)
Seller = Mpy_Erkend_Door_VMSW
Seller = Vlaams_Woningfonds
Seller = Gelijksoortige_Rechtspersoon_EER
Use = Community_Purpose

-- case -------------------------------------
Type:        
  
Definitions: 
  Rule:∀[][]: Professional_Buyer() ⇔Professional_Declaration_Filed ∧ Guarantee_Satisfied ∧ ((Additional_Security_Required ∧ Additional_Security_Satisfied) ∨ (~(Additional_Security_Required))) ∧ (Resale = Three_Or_More)
Universals:  
  ~Professional_Declaration_Filed
Consequences:
  ~Tax = 4
  ~Registration_Type = Professional_Purchase
  ~Professional_Buyer
Simplified:  
  ((Tax = 1) ⇒ ((Registration_Type = Heritage) ∧ (Region = Flemish_Region)))
  (Tax = 2) ⇒ ((Registration_Type = Social_Dwelling) ∧ (Region = Flemish_Region))
  ((Tax = 6) ⇒ (((Registration_Type = Energy_Efficient_Dwelling) ∨ (Registration_Type = Social_Purpose) ∨ (Registration_Type = Exchange_Unbuilt_Ground)) ∧ (Region = Flemish_Region)))
  (Tax = 7) ⇒ (((Registration_Type = Family_Dwelling) ∨ (Registration_Type = Dwelling_For_Social_Renting)) ∧ (Region = Flemish_Region))
  (Tax = 10) ⇒ ((Region = Flemish_Region) ∧ (Registration_Type = Other))
  ((Tax = 12) ⇒ ((Region = Brussels_Region) ∨ (Region = Walloon_Region)))
  (Registration_Type = Family_Dwelling) ⇒ ((Type_Of_Real_Estate = Residential) ∧ (Buyer = Natural_Person) ∧ Domicile_Established ∧ Clean_Purchase ∧ (First_Ownership ∨ Causal_Connection) ∧ ((~(Energy_Renovation_Planned)) ∨ (~(Term_Energy_Renovation = (5 + Certification_Date)))))
  (Registration_Type = Social_Dwelling) ⇒ ((Buyer = Natural_Person) ∧ (Type_Of_Real_Estate = Residential) ∧ (Use = Social_Housing) ∧ ((Seller = Vlaamse_Mpy_Voor_Sociaal_Wonen) ∨ (Seller = ErkendeSocialeHuisvestingsMpy)) ∧ Mortgage_Loan_Allowance)
  (Registration_Type = Energy_Efficient_Dwelling) ⇒ ((Type_Of_Real_Estate = Residential) ∧ (Buyer = Natural_Person) ∧ Domicile_Established ∧ Clean_Purchase ∧ (First_Ownership ∨ Causal_Connection) ∧ Energy_Renovation_Planned ∧ (Term_Energy_Renovation = (5 + Certification_Date)))
  (Registration_Type = Dwelling_For_Social_Renting) ⇒ ((Type_Of_Real_Estate = Residential) ∧ (Use = Social_Renting) ∧ (Start_Dt_Dwelling_For_Social_Rent = (3 + Certification_Date)) ∧ (Duration_Of_Agreement = Less_Than_9_years))
  ((Registration_Type = Heritage) ⇒ ((Type_Of_Real_Estate = Residential) ∧ Monument ∧ (Use = As_Family_Dwelling) ∧ Heritage_Investment ∧ Heritage_Plan ∧ Additional_Terms))
  ((Registration_Type = Social_Purpose) ⇒ (((Seller = Mpy_Erkend_Door_VMSW) ∨ (Seller = Vlaams_Woningfonds) ∨ (Seller = Gelijksoortige_Rechtspersoon_EER)) ∧ (Use = Community_Purpose)))
  (Registration_Type = Exchange_Unbuilt_Ground) ⇒ (Additional_Terms ∧ (~(Monument)))
  (Registration_Type = Other) ⇒ ((~(Registration_Type = Family_Dwelling)) ∧ (~(Registration_Type = Social_Dwelling)) ∧ (~(Registration_Type = Energy_Efficient_Dwelling)) ∧ (~(Registration_Type = Dwelling_For_Social_Renting)) ∧ (~(Registration_Type = Heritage)) ∧ (~(Registration_Type = Social_Purpose)) ∧ (~(Registration_Type = Exchange_Unbuilt_Ground)))
  2015 ≤ Start_Dt_Dwelling_For_Social_Rent ≤ 2025
  2015 ≤ Certification_Date ≤ 2025
  2015 ≤ Term_Energy_Renovation ≤ 2025
  (Tax = 1) ∨ (Tax = 2) ∨ (Tax = 7) ∨ (Tax = 6) ∨ (Tax = 10) ∨ (Tax = 12)
Irrelevant:  
  ~Guarantee_Satisfied
  ~Additional_Security_Required
  ~Additional_Security_Satisfied
  ~Resale = Three_Or_More
  ~Transaction_Type = Public_Sale
  ~Use = For_Resale
  ~Certification_Date_Sale = (Certification_Date + 8)


-- meta -------------------------------------
{'symbols': [{'idpname': 'Region', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'normal'},
             {'idpname': 'Type_Of_Real_Estate',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'idpname': 'Seller', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'normal'},
             {'idpname': 'Buyer', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'normal'},
             {'idpname': 'Use', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'normal'},
             {'idpname': 'Domicile_Established',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'idpname': 'First_Ownership',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'idpname': 'Monument', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'normal'},
             {'idpname': 'Resale', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'normal'},
             {'idpname': 'Transaction_Type',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'idpname': 'Duration_Of_Agreement',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'idpname': 'Mortgage_Loan_Allowance',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'idpname': 'Clean_Purchase',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'idpname': 'Causal_Connection',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'idpname': 'Energy_Renovation_Planned',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'idpname': 'Heritage_Investment',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'idpname': 'Heritage_Plan',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'idpname': 'Professional_Declaration_Filed',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'idpname': 'Guarantee_Satisfied',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'idpname': 'Additional_Security_Required',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'idpname': 'Additional_Security_Satisfied',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'idpname': 'Additional_Terms',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'idpname': 'Start_Dt_Dwelling_For_Social_Rent',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'idpname': 'Certification_Date',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'idpname': 'Term_Energy_Renovation',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'idpname': 'Certification_Date_Sale',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'idpname': 'Professional_Buyer',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'idpname': 'Registration_Type',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'idpname': 'Tax', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': True},
 'Additional_Security_Required': {'Additional_Security_Required': {'environmental': True,
                                                                   'normal': True,
                                                                   'reading': 'Additional_Security_Required',
                                                                   'relevant': False,
                                                                   'status': 'UNKNOWN',
                                                                   'typ': 'Bool'}},
 'Additional_Security_Satisfied': {'Additional_Security_Satisfied': {'environmental': True,
                                                                     'normal': True,
                                                                     'reading': 'Additional_Security_Satisfied',
                                                                     'relevant': False,
                                                                     'status': 'UNKNOWN',
                                                                     'typ': 'Bool'}},
 'Additional_Terms': {'Additional_Terms': {'environmental': True,
                                           'normal': True,
                                           'reading': 'Additional_Terms',
                                           'relevant': True,
                                           'status': 'UNKNOWN',
                                           'typ': 'Bool'}},
 'Buyer': {'Buyer': {'environmental': True,
                     'normal': True,
                     'reading': 'Buyer',
                     'relevant': True,
                     'status': 'UNKNOWN',
                     'typ': 'buyerType',
                     'value': '',
                     'values': ['Natural_Person', 'Legal_Person', 'Mixed']},
           'Buyer = Natural_Person': {'environmental': True,
                                      'normal': False,
                                      'reading': 'Buyer = Natural_Person',
                                      'relevant': True,
                                      'status': 'UNKNOWN',
                                      'typ': 'Bool'}},
 'Causal_Connection': {'Causal_Connection': {'environmental': True,
                                             'normal': True,
                                             'reading': 'Causal_Connection',
                                             'relevant': True,
                                             'status': 'UNKNOWN',
                                             'typ': 'Bool'}},
 'Certification_Date': {'Certification_Date': {'environmental': True,
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
 'Certification_Date_Sale': {'Certification_Date_Sale': {'environmental': True,
                                                         'normal': True,
                                                         'reading': 'Certification_Date_Sale',
                                                         'relevant': False,
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
                             'Certification_Date_Sale = (Certification_Date + 8)': {'environmental': True,
                                                                                    'normal': False,
                                                                                    'reading': 'Certification_Date_Sale '
                                                                                               '= (Certification_Date '
                                                                                               '+ 8)',
                                                                                    'relevant': False,
                                                                                    'status': 'UNKNOWN',
                                                                                    'typ': 'Bool'}},
 'Clean_Purchase': {'Clean_Purchase': {'environmental': True,
                                       'normal': True,
                                       'reading': 'Clean_Purchase',
                                       'relevant': True,
                                       'status': 'UNKNOWN',
                                       'typ': 'Bool'}},
 'Core_City': {'Core_City': {'environmental': True,
                             'normal': True,
                             'reading': 'Core_City',
                             'relevant': False,
                             'status': 'UNKNOWN',
                             'typ': 'Bool'}},
 'Domicile_Established': {'Domicile_Established': {'environmental': True,
                                                   'normal': True,
                                                   'reading': 'Domicile_Established',
                                                   'relevant': True,
                                                   'status': 'UNKNOWN',
                                                   'typ': 'Bool'}},
 'Duration_Of_Agreement': {'Duration_Of_Agreement': {'environmental': True,
                                                     'normal': True,
                                                     'reading': 'Duration_Of_Agreement',
                                                     'relevant': True,
                                                     'status': 'UNKNOWN',
                                                     'typ': 'agreementDwellingForSocialRenting',
                                                     'value': '',
                                                     'values': ['Less_Than_9_years', 'More_than_9_Or_9_years']},
                           'Duration_Of_Agreement = Less_Than_9_years': {'environmental': True,
                                                                         'normal': False,
                                                                         'reading': 'Duration_Of_Agreement = '
                                                                                    'Less_Than_9_years',
                                                                         'relevant': True,
                                                                         'status': 'UNKNOWN',
                                                                         'typ': 'Bool'}},
 'Energy_Renovation_Planned': {'Energy_Renovation_Planned': {'environmental': True,
                                                             'normal': True,
                                                             'reading': 'Energy_Renovation_Planned',
                                                             'relevant': True,
                                                             'status': 'UNKNOWN',
                                                             'typ': 'Bool'}},
 'First_Ownership': {'First_Ownership': {'environmental': True,
                                         'normal': True,
                                         'reading': 'First_Ownership',
                                         'relevant': True,
                                         'status': 'UNKNOWN',
                                         'typ': 'Bool'}},
 'Guarantee_Satisfied': {'Guarantee_Satisfied': {'environmental': True,
                                                 'normal': True,
                                                 'reading': 'Guarantee_Satisfied',
                                                 'relevant': False,
                                                 'status': 'UNKNOWN',
                                                 'typ': 'Bool'}},
 'Heritage_Investment': {'Heritage_Investment': {'environmental': True,
                                                 'normal': True,
                                                 'reading': 'Heritage_Investment',
                                                 'relevant': True,
                                                 'status': 'UNKNOWN',
                                                 'typ': 'Bool'}},
 'Heritage_Plan': {'Heritage_Plan': {'environmental': True,
                                     'normal': True,
                                     'reading': 'Heritage_Plan',
                                     'relevant': True,
                                     'status': 'UNKNOWN',
                                     'typ': 'Bool'}},
 'Monument': {'Monument': {'environmental': True,
                           'normal': True,
                           'reading': 'Monument',
                           'relevant': True,
                           'status': 'UNKNOWN',
                           'typ': 'Bool'}},
 'Mortgage_Loan_Allowance': {'Mortgage_Loan_Allowance': {'environmental': True,
                                                         'normal': True,
                                                         'reading': 'Mortgage_Loan_Allowance',
                                                         'relevant': True,
                                                         'status': 'UNKNOWN',
                                                         'typ': 'Bool'}},
 'Municipality': {'Municipality': {'environmental': True,
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
 'Professional_Buyer': {'Professional_Buyer': {'environmental': True,
                                               'normal': True,
                                               'reading': 'Professional_Buyer',
                                               'relevant': True,
                                               'status': 'ENV_CONSQ',
                                               'typ': 'Bool',
                                               'value': False}},
 'Professional_Declaration_Filed': {'Professional_Declaration_Filed': {'environmental': True,
                                                                       'normal': True,
                                                                       'reading': 'Professional_Declaration_Filed',
                                                                       'relevant': True,
                                                                       'status': 'UNIVERSAL',
                                                                       'typ': 'Bool',
                                                                       'value': False}},
 'Region': {'Region': {'environmental': True,
                       'normal': True,
                       'reading': 'Region',
                       'relevant': True,
                       'status': 'UNKNOWN',
                       'typ': 'location',
                       'value': '',
                       'values': ['Flemish_Region', 'Walloon_Region', 'Brussels_Region']},
            'Region = Brussels_Region': {'environmental': True,
                                         'normal': False,
                                         'reading': 'Region = Brussels_Region',
                                         'relevant': True,
                                         'status': 'UNKNOWN',
                                         'typ': 'Bool'},
            'Region = Flemish_Region': {'environmental': True,
                                        'normal': False,
                                        'reading': 'Region = Flemish_Region',
                                        'relevant': True,
                                        'status': 'UNKNOWN',
                                        'typ': 'Bool'},
            'Region = Walloon_Region': {'environmental': True,
                                        'normal': False,
                                        'reading': 'Region = Walloon_Region',
                                        'relevant': True,
                                        'status': 'UNKNOWN',
                                        'typ': 'Bool'}},
 'Registration_Type': {'Registration_Type': {'environmental': False,
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
                       'Registration_Type = Dwelling_For_Social_Renting': {'environmental': False,
                                                                           'normal': False,
                                                                           'reading': 'Registration_Type = '
                                                                                      'Dwelling_For_Social_Renting',
                                                                           'relevant': True,
                                                                           'status': 'UNKNOWN',
                                                                           'typ': 'Bool'},
                       'Registration_Type = Energy_Efficient_Dwelling': {'environmental': False,
                                                                         'normal': False,
                                                                         'reading': 'Registration_Type = '
                                                                                    'Energy_Efficient_Dwelling',
                                                                         'relevant': True,
                                                                         'status': 'UNKNOWN',
                                                                         'typ': 'Bool'},
                       'Registration_Type = Exchange_Unbuilt_Ground': {'environmental': False,
                                                                       'normal': False,
                                                                       'reading': 'Registration_Type = '
                                                                                  'Exchange_Unbuilt_Ground',
                                                                       'relevant': True,
                                                                       'status': 'UNKNOWN',
                                                                       'typ': 'Bool'},
                       'Registration_Type = Family_Dwelling': {'environmental': False,
                                                               'normal': False,
                                                               'reading': 'Registration_Type = Family_Dwelling',
                                                               'relevant': True,
                                                               'status': 'UNKNOWN',
                                                               'typ': 'Bool'},
                       'Registration_Type = Heritage': {'environmental': False,
                                                        'normal': False,
                                                        'reading': 'Registration_Type = Heritage',
                                                        'relevant': True,
                                                        'status': 'UNKNOWN',
                                                        'typ': 'Bool'},
                       'Registration_Type = Other': {'environmental': False,
                                                     'normal': False,
                                                     'reading': 'Registration_Type = Other',
                                                     'relevant': True,
                                                     'status': 'UNKNOWN',
                                                     'typ': 'Bool'},
                       'Registration_Type = Professional_Purchase': {'environmental': False,
                                                                     'normal': False,
                                                                     'reading': 'Registration_Type = '
                                                                                'Professional_Purchase',
                                                                     'relevant': True,
                                                                     'status': 'CONSEQUENCE',
                                                                     'typ': 'Bool',
                                                                     'value': False},
                       'Registration_Type = Social_Dwelling': {'environmental': False,
                                                               'normal': False,
                                                               'reading': 'Registration_Type = Social_Dwelling',
                                                               'relevant': True,
                                                               'status': 'UNKNOWN',
                                                               'typ': 'Bool'},
                       'Registration_Type = Social_Purpose': {'environmental': False,
                                                              'normal': False,
                                                              'reading': 'Registration_Type = Social_Purpose',
                                                              'relevant': True,
                                                              'status': 'UNKNOWN',
                                                              'typ': 'Bool'}},
 'Resale': {'Resale': {'environmental': True,
                       'normal': True,
                       'reading': 'Resale',
                       'relevant': False,
                       'status': 'UNKNOWN',
                       'typ': 'resale',
                       'value': '',
                       'values': ['Less_Than_Three', 'Three_Or_More']},
            'Resale = Three_Or_More': {'environmental': True,
                                       'normal': False,
                                       'reading': 'Resale = Three_Or_More',
                                       'relevant': False,
                                       'status': 'UNKNOWN',
                                       'typ': 'Bool'}},
 'Seller': {'Seller': {'environmental': True,
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
            'Seller = ErkendeSocialeHuisvestingsMpy': {'environmental': True,
                                                       'normal': False,
                                                       'reading': 'Seller = ErkendeSocialeHuisvestingsMpy',
                                                       'relevant': True,
                                                       'status': 'UNKNOWN',
                                                       'typ': 'Bool'},
            'Seller = Gelijksoortige_Rechtspersoon_EER': {'environmental': True,
                                                          'normal': False,
                                                          'reading': 'Seller = Gelijksoortige_Rechtspersoon_EER',
                                                          'relevant': True,
                                                          'status': 'UNKNOWN',
                                                          'typ': 'Bool'},
            'Seller = Mpy_Erkend_Door_VMSW': {'environmental': True,
                                              'normal': False,
                                              'reading': 'Seller = Mpy_Erkend_Door_VMSW',
                                              'relevant': True,
                                              'status': 'UNKNOWN',
                                              'typ': 'Bool'},
            'Seller = Vlaams_Woningfonds': {'environmental': True,
                                            'normal': False,
                                            'reading': 'Seller = Vlaams_Woningfonds',
                                            'relevant': True,
                                            'status': 'UNKNOWN',
                                            'typ': 'Bool'},
            'Seller = Vlaamse_Mpy_Voor_Sociaal_Wonen': {'environmental': True,
                                                        'normal': False,
                                                        'reading': 'Seller = Vlaamse_Mpy_Voor_Sociaal_Wonen',
                                                        'relevant': True,
                                                        'status': 'UNKNOWN',
                                                        'typ': 'Bool'}},
 'Start_Dt_Dwelling_For_Social_Rent': {'Start_Dt_Dwelling_For_Social_Rent': {'environmental': True,
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
                                       'Start_Dt_Dwelling_For_Social_Rent = (Certification_Date + 3)': {'environmental': True,
                                                                                                        'normal': False,
                                                                                                        'reading': 'Start_Dt_Dwelling_For_Social_Rent '
                                                                                                                   '= '
                                                                                                                   '(Certification_Date '
                                                                                                                   '+ '
                                                                                                                   '3)',
                                                                                                        'relevant': True,
                                                                                                        'status': 'UNKNOWN',
                                                                                                        'typ': 'Bool'}},
 'Tax': {'Tax': {'environmental': False,
                 'normal': True,
                 'reading': 'Tax',
                 'relevant': True,
                 'status': 'UNKNOWN',
                 'typ': 'Int',
                 'value': '',
                 'values': ['1', '2', '4', '7', '6', '10', '12']},
         'Tax = 1': {'environmental': False,
                     'normal': False,
                     'reading': 'Tax = 1',
                     'relevant': True,
                     'status': 'UNKNOWN',
                     'typ': 'Bool'},
         'Tax = 10': {'environmental': False,
                      'normal': False,
                      'reading': 'Tax = 10',
                      'relevant': True,
                      'status': 'UNKNOWN',
                      'typ': 'Bool'},
         'Tax = 12': {'environmental': False,
                      'normal': False,
                      'reading': 'Tax = 12',
                      'relevant': True,
                      'status': 'UNKNOWN',
                      'typ': 'Bool'},
         'Tax = 2': {'environmental': False,
                     'normal': False,
                     'reading': 'Tax = 2',
                     'relevant': True,
                     'status': 'UNKNOWN',
                     'typ': 'Bool'},
         'Tax = 4': {'environmental': False,
                     'normal': False,
                     'reading': 'Tax = 4',
                     'relevant': True,
                     'status': 'CONSEQUENCE',
                     'typ': 'Bool',
                     'value': False},
         'Tax = 6': {'environmental': False,
                     'normal': False,
                     'reading': 'Tax = 6',
                     'relevant': True,
                     'status': 'UNKNOWN',
                     'typ': 'Bool'},
         'Tax = 7': {'environmental': False,
                     'normal': False,
                     'reading': 'Tax = 7',
                     'relevant': True,
                     'status': 'UNKNOWN',
                     'typ': 'Bool'}},
 'Term_Energy_Renovation': {'Term_Energy_Renovation': {'environmental': True,
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
                            'Term_Energy_Renovation = (Certification_Date + 5)': {'environmental': True,
                                                                                  'normal': False,
                                                                                  'reading': 'Term_Energy_Renovation = '
                                                                                             '(Certification_Date + 5)',
                                                                                  'relevant': True,
                                                                                  'status': 'UNKNOWN',
                                                                                  'typ': 'Bool'}},
 'Transaction_Type': {'Transaction_Type': {'environmental': True,
                                           'normal': True,
                                           'reading': 'Transaction_Type',
                                           'relevant': False,
                                           'status': 'UNKNOWN',
                                           'typ': 'transaction',
                                           'value': '',
                                           'values': ['Public_Sale', 'Out_Hand', 'Public_Sale_Community']},
                      'Transaction_Type = Public_Sale': {'environmental': True,
                                                         'normal': False,
                                                         'reading': 'Transaction_Type = Public_Sale',
                                                         'relevant': False,
                                                         'status': 'UNKNOWN',
                                                         'typ': 'Bool'}},
 'Type_Of_Real_Estate': {'Type_Of_Real_Estate': {'environmental': True,
                                                 'normal': True,
                                                 'reading': 'Type_Of_Real_Estate',
                                                 'relevant': True,
                                                 'status': 'UNKNOWN',
                                                 'typ': 'real_Estate_Type',
                                                 'value': '',
                                                 'values': ['Residential',
                                                            'Residential_Building_Land',
                                                            'Other_Real_Estate']},
                         'Type_Of_Real_Estate = Residential': {'environmental': True,
                                                               'normal': False,
                                                               'reading': 'Type_Of_Real_Estate = Residential',
                                                               'relevant': True,
                                                               'status': 'UNKNOWN',
                                                               'typ': 'Bool'}},
 'Use': {'Use': {'environmental': True,
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
         'Use = As_Family_Dwelling': {'environmental': True,
                                      'normal': False,
                                      'reading': 'Use = As_Family_Dwelling',
                                      'relevant': True,
                                      'status': 'UNKNOWN',
                                      'typ': 'Bool'},
         'Use = Community_Purpose': {'environmental': True,
                                     'normal': False,
                                     'reading': 'Use = Community_Purpose',
                                     'relevant': True,
                                     'status': 'UNKNOWN',
                                     'typ': 'Bool'},
         'Use = For_Resale': {'environmental': True,
                              'normal': False,
                              'reading': 'Use = For_Resale',
                              'relevant': False,
                              'status': 'UNKNOWN',
                              'typ': 'Bool'},
         'Use = Social_Housing': {'environmental': True,
                                  'normal': False,
                                  'reading': 'Use = Social_Housing',
                                  'relevant': True,
                                  'status': 'UNKNOWN',
                                  'typ': 'Bool'},
         'Use = Social_Renting': {'environmental': True,
                                  'normal': False,
                                  'reading': 'Use = Social_Renting',
                                  'relevant': True,
                                  'status': 'UNKNOWN',
                                  'typ': 'Bool'}}}
