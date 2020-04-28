
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




    
Professional_Buyer =>
    Professional_Declaration_Filed
    & Guarantee_Satisfied
    & (Additional_Security_Required & Additional_Security_Satisfied
    | ~ Additional_Security_Required)
    & Resale = Three_Or_More
.

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

Or(Not(Professional_Buyer),
   And(Professional_Declaration_Filed,
       Guarantee_Satisfied,
       Or(And(Additional_Security_Required,
              Additional_Security_Satisfied),
          Not(Additional_Security_Required)),
       Resale == Three_Or_More))

Or(Tax == 1,
   Tax == 2,
   Tax == 4,
   Tax == 7,
   Tax == 6,
   Tax == 10,
   Tax == 12)

Or(Region == Flemish_Region,
   Region == Walloon_Region,
   Region == Brussels_Region)

Or(Municipality == other_Municipal,
   Municipality == Aalst,
   Municipality == Antwerpen,
   Municipality == Boom,
   Municipality == Brugge,
   Municipality == Dendermonde,
   Municipality == Genk,
   Municipality == Gent,
   Municipality == Hasselt,
   Municipality == Kortrijk,
   Municipality == Leuven,
   Municipality == Mechelen,
   Municipality == Oostende,
   Municipality == Roeselare,
   Municipality == SintNiklaas,
   Municipality == Turnhout,
   Municipality == Vilvoorde,
   Municipality == Affligem,
   Municipality == Asse,
   Municipality == Beersel,
   Municipality == Bever,
   Municipality == Dilbeek,
   Municipality == Drogenbos,
   Municipality == Galmaarden,
   Municipality == Gooik,
   Municipality == Grimbergen,
   Municipality == Halle,
   Municipality == Herne,
   Municipality == Hoeilaart,
   Municipality == Kampenhout,
   Municipality == KapelleopdenBos,
   Municipality == Kraainem,
   Municipality == Lennik,
   Municipality == Liedekerke,
   Municipality == Linkebeek,
   Municipality == Londerzeel,
   Municipality == Machelen,
   Municipality == Meise,
   Municipality == Merchtem,
   Municipality == Opwijk,
   Municipality == Overijse,
   Municipality == Pepingen,
   Municipality == Roosdaal,
   Municipality == SintGenesiusRode,
   Municipality == SintPietersLeeuw,
   Municipality == Steenokkerzeel,
   Municipality == Ternat,
   Municipality == Wemmel,
   Municipality == WezembeekOppem,
   Municipality == Zaventem,
   Municipality == Zemst,
   Municipality == Bertem,
   Municipality == Huldenberg,
   Municipality == Kortenberg,
   Municipality == Tervuren)

Or(Type_Of_Real_Estate == Residential,
   Type_Of_Real_Estate == Residential_Building_Land,
   Type_Of_Real_Estate == Other_Real_Estate)

Or(Seller == Vlaams_Woningfonds,
   Seller == Gelijksoortige_Rechtspersoon_EER,
   Seller == Mpy_Erkend_Door_VMSW,
   Seller == Vlaamse_Mpy_Voor_Sociaal_Wonen,
   Seller == ErkendeSocialeHuisvestingsMpy)

Or(Buyer == Natural_Person,
   Buyer == Legal_Person,
   Buyer == Mixed)

Or(Use == As_Family_Dwelling,
   Use == For_Resale,
   Use == Community_Purpose,
   Use == Social_Housing,
   Use == Social_Renting,
   Use == Other_House,
   Use == No_House)

Or(Resale == Less_Than_Three, Resale == Three_Or_More)

Or(Transaction_Type == Public_Sale,
   Transaction_Type == Out_Hand,
   Transaction_Type == Public_Sale_Community)

Or(Duration_Of_Agreement == Less_Than_9_years,
   Duration_Of_Agreement == More_than_9_Or_9_years)

Or(Start_Dt_Dwelling_For_Social_Rent == 2015,
   Start_Dt_Dwelling_For_Social_Rent == 2016,
   Start_Dt_Dwelling_For_Social_Rent == 2017,
   Start_Dt_Dwelling_For_Social_Rent == 2018,
   Start_Dt_Dwelling_For_Social_Rent == 2019,
   Start_Dt_Dwelling_For_Social_Rent == 2020,
   Start_Dt_Dwelling_For_Social_Rent == 2021,
   Start_Dt_Dwelling_For_Social_Rent == 2022,
   Start_Dt_Dwelling_For_Social_Rent == 2023,
   Start_Dt_Dwelling_For_Social_Rent == 2024,
   Start_Dt_Dwelling_For_Social_Rent == 2025)

Or(Certification_Date == 2015,
   Certification_Date == 2016,
   Certification_Date == 2017,
   Certification_Date == 2018,
   Certification_Date == 2019,
   Certification_Date == 2020,
   Certification_Date == 2021,
   Certification_Date == 2022,
   Certification_Date == 2023,
   Certification_Date == 2024,
   Certification_Date == 2025)

Or(Term_Energy_Renovation == 2015,
   Term_Energy_Renovation == 2016,
   Term_Energy_Renovation == 2017,
   Term_Energy_Renovation == 2018,
   Term_Energy_Renovation == 2019,
   Term_Energy_Renovation == 2020,
   Term_Energy_Renovation == 2021,
   Term_Energy_Renovation == 2022,
   Term_Energy_Renovation == 2023,
   Term_Energy_Renovation == 2024,
   Term_Energy_Renovation == 2025)

Or(Certification_Date_Sale == 2015,
   Certification_Date_Sale == 2016,
   Certification_Date_Sale == 2017,
   Certification_Date_Sale == 2018,
   Certification_Date_Sale == 2019,
   Certification_Date_Sale == 2020,
   Certification_Date_Sale == 2021,
   Certification_Date_Sale == 2022,
   Certification_Date_Sale == 2023,
   Certification_Date_Sale == 2024,
   Certification_Date_Sale == 2025)

Or(Registration_Type == Family_Dwelling,
   Registration_Type == Social_Dwelling,
   Registration_Type == Social_Purpose,
   Registration_Type == Exchange_Unbuilt_Ground,
   Registration_Type == Professional_Purchase,
   Registration_Type == Energy_Efficient_Dwelling,
   Registration_Type == Heritage,
   Registration_Type == Dwelling_For_Social_Renting,
   Registration_Type == Other)

Or(Tax == 1,
   Tax == 2,
   Tax == 4,
   Tax == 7,
   Tax == 6,
   Tax == 10,
   Tax == 12)

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
Transaction_Type = Public_Sale
Use = For_Resale
Certification_Date_Sale = (Certification_Date + 8)
Seller = Mpy_Erkend_Door_VMSW
Seller = Vlaams_Woningfonds
Seller = Gelijksoortige_Rechtspersoon_EER
Use = Community_Purpose
Professional_Declaration_Filed
Guarantee_Satisfied
Additional_Security_Required
Additional_Security_Satisfied
Resale = Three_Or_More
Municipality = other_Municipal
Municipality = Aalst
Municipality = Antwerpen
Municipality = Boom
Municipality = Brugge
Municipality = Dendermonde
Municipality = Genk
Municipality = Gent
Municipality = Hasselt
Municipality = Kortrijk
Municipality = Leuven
Municipality = Mechelen
Municipality = Oostende
Municipality = Roeselare
Municipality = SintNiklaas
Municipality = Turnhout
Municipality = Vilvoorde
Municipality = Affligem
Municipality = Asse
Municipality = Beersel
Municipality = Bever
Municipality = Dilbeek
Municipality = Drogenbos
Municipality = Galmaarden
Municipality = Gooik
Municipality = Grimbergen
Municipality = Halle
Municipality = Herne
Municipality = Hoeilaart
Municipality = Kampenhout
Municipality = KapelleopdenBos
Municipality = Kraainem
Municipality = Lennik
Municipality = Liedekerke
Municipality = Linkebeek
Municipality = Londerzeel
Municipality = Machelen
Municipality = Meise
Municipality = Merchtem
Municipality = Opwijk
Municipality = Overijse
Municipality = Pepingen
Municipality = Roosdaal
Municipality = SintGenesiusRode
Municipality = SintPietersLeeuw
Municipality = Steenokkerzeel
Municipality = Ternat
Municipality = Wemmel
Municipality = WezembeekOppem
Municipality = Zaventem
Municipality = Zemst
Municipality = Bertem
Municipality = Huldenberg
Municipality = Kortenberg
Municipality = Tervuren
Type_Of_Real_Estate = Residential_Building_Land
Type_Of_Real_Estate = Other_Real_Estate
Buyer = Legal_Person
Buyer = Mixed
Use = Other_House
Use = No_House
Resale = Less_Than_Three
Transaction_Type = Out_Hand
Transaction_Type = Public_Sale_Community
Duration_Of_Agreement = More_than_9_Or_9_years
Start_Dt_Dwelling_For_Social_Rent = 2015
Start_Dt_Dwelling_For_Social_Rent = 2016
Start_Dt_Dwelling_For_Social_Rent = 2017
Start_Dt_Dwelling_For_Social_Rent = 2018
Start_Dt_Dwelling_For_Social_Rent = 2019
Start_Dt_Dwelling_For_Social_Rent = 2020
Start_Dt_Dwelling_For_Social_Rent = 2021
Start_Dt_Dwelling_For_Social_Rent = 2022
Start_Dt_Dwelling_For_Social_Rent = 2023
Start_Dt_Dwelling_For_Social_Rent = 2024
Start_Dt_Dwelling_For_Social_Rent = 2025
Certification_Date = 2015
Certification_Date = 2016
Certification_Date = 2017
Certification_Date = 2018
Certification_Date = 2019
Certification_Date = 2020
Certification_Date = 2021
Certification_Date = 2022
Certification_Date = 2023
Certification_Date = 2024
Certification_Date = 2025
Term_Energy_Renovation = 2015
Term_Energy_Renovation = 2016
Term_Energy_Renovation = 2017
Term_Energy_Renovation = 2018
Term_Energy_Renovation = 2019
Term_Energy_Renovation = 2020
Term_Energy_Renovation = 2021
Term_Energy_Renovation = 2022
Term_Energy_Renovation = 2023
Term_Energy_Renovation = 2024
Term_Energy_Renovation = 2025
Certification_Date_Sale = 2015
Certification_Date_Sale = 2016
Certification_Date_Sale = 2017
Certification_Date_Sale = 2018
Certification_Date_Sale = 2019
Certification_Date_Sale = 2020
Certification_Date_Sale = 2021
Certification_Date_Sale = 2022
Certification_Date_Sale = 2023
Certification_Date_Sale = 2024
Certification_Date_Sale = 2025

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
Transaction_Type = Public_Sale
Use = For_Resale
Certification_Date_Sale = (Certification_Date + 8)
Seller = Mpy_Erkend_Door_VMSW
Seller = Vlaams_Woningfonds
Seller = Gelijksoortige_Rechtspersoon_EER
Use = Community_Purpose
Resale = Three_Or_More
Municipality = other_Municipal
Municipality = Aalst
Municipality = Antwerpen
Municipality = Boom
Municipality = Brugge
Municipality = Dendermonde
Municipality = Genk
Municipality = Gent
Municipality = Hasselt
Municipality = Kortrijk
Municipality = Leuven
Municipality = Mechelen
Municipality = Oostende
Municipality = Roeselare
Municipality = SintNiklaas
Municipality = Turnhout
Municipality = Vilvoorde
Municipality = Affligem
Municipality = Asse
Municipality = Beersel
Municipality = Bever
Municipality = Dilbeek
Municipality = Drogenbos
Municipality = Galmaarden
Municipality = Gooik
Municipality = Grimbergen
Municipality = Halle
Municipality = Herne
Municipality = Hoeilaart
Municipality = Kampenhout
Municipality = KapelleopdenBos
Municipality = Kraainem
Municipality = Lennik
Municipality = Liedekerke
Municipality = Linkebeek
Municipality = Londerzeel
Municipality = Machelen
Municipality = Meise
Municipality = Merchtem
Municipality = Opwijk
Municipality = Overijse
Municipality = Pepingen
Municipality = Roosdaal
Municipality = SintGenesiusRode
Municipality = SintPietersLeeuw
Municipality = Steenokkerzeel
Municipality = Ternat
Municipality = Wemmel
Municipality = WezembeekOppem
Municipality = Zaventem
Municipality = Zemst
Municipality = Bertem
Municipality = Huldenberg
Municipality = Kortenberg
Municipality = Tervuren
Type_Of_Real_Estate = Residential_Building_Land
Type_Of_Real_Estate = Other_Real_Estate
Buyer = Legal_Person
Buyer = Mixed
Use = Other_House
Use = No_House
Resale = Less_Than_Three
Transaction_Type = Out_Hand
Transaction_Type = Public_Sale_Community
Duration_Of_Agreement = More_than_9_Or_9_years
Start_Dt_Dwelling_For_Social_Rent = 2015
Start_Dt_Dwelling_For_Social_Rent = 2016
Start_Dt_Dwelling_For_Social_Rent = 2017
Start_Dt_Dwelling_For_Social_Rent = 2018
Start_Dt_Dwelling_For_Social_Rent = 2019
Start_Dt_Dwelling_For_Social_Rent = 2020
Start_Dt_Dwelling_For_Social_Rent = 2021
Start_Dt_Dwelling_For_Social_Rent = 2022
Start_Dt_Dwelling_For_Social_Rent = 2023
Start_Dt_Dwelling_For_Social_Rent = 2024
Start_Dt_Dwelling_For_Social_Rent = 2025
Certification_Date = 2015
Certification_Date = 2016
Certification_Date = 2017
Certification_Date = 2018
Certification_Date = 2019
Certification_Date = 2020
Certification_Date = 2021
Certification_Date = 2022
Certification_Date = 2023
Certification_Date = 2024
Certification_Date = 2025
Term_Energy_Renovation = 2015
Term_Energy_Renovation = 2016
Term_Energy_Renovation = 2017
Term_Energy_Renovation = 2018
Term_Energy_Renovation = 2019
Term_Energy_Renovation = 2020
Term_Energy_Renovation = 2021
Term_Energy_Renovation = 2022
Term_Energy_Renovation = 2023
Term_Energy_Renovation = 2024
Term_Energy_Renovation = 2025
Certification_Date_Sale = 2015
Certification_Date_Sale = 2016
Certification_Date_Sale = 2017
Certification_Date_Sale = 2018
Certification_Date_Sale = 2019
Certification_Date_Sale = 2020
Certification_Date_Sale = 2021
Certification_Date_Sale = 2022
Certification_Date_Sale = 2023
Certification_Date_Sale = 2024
Certification_Date_Sale = 2025

-- case -------------------------------------
Type:        
  
Definitions: 
  
Universals:  
  
Consequences:
  
Simplified:  
  ((Tax = 1) ⇒ ((Registration_Type = Heritage) ∧ (Region = Flemish_Region)))
  (Tax = 2) ⇒ ((Registration_Type = Social_Dwelling) ∧ (Region = Flemish_Region))
  (Tax = 4) ⇒ ((Registration_Type = Professional_Purchase) ∧ (Region = Flemish_Region))
  ((Tax = 6) ⇒ (((Registration_Type = Energy_Efficient_Dwelling) ∨ (Registration_Type = Social_Purpose) ∨ (Registration_Type = Exchange_Unbuilt_Ground)) ∧ (Region = Flemish_Region)))
  (Tax = 7) ⇒ (((Registration_Type = Family_Dwelling) ∨ (Registration_Type = Dwelling_For_Social_Renting)) ∧ (Region = Flemish_Region))
  (Tax = 10) ⇒ ((Region = Flemish_Region) ∧ (Registration_Type = Other))
  ((Tax = 12) ⇒ ((Region = Brussels_Region) ∨ (Region = Walloon_Region)))
  (Registration_Type = Family_Dwelling) ⇒ ((Type_Of_Real_Estate = Residential) ∧ (Buyer = Natural_Person) ∧ Domicile_Established ∧ Clean_Purchase ∧ (First_Ownership ∨ Causal_Connection) ∧ ((~(Energy_Renovation_Planned)) ∨ (~(Term_Energy_Renovation = (5 + Certification_Date)))))
  (Registration_Type = Social_Dwelling) ⇒ ((Buyer = Natural_Person) ∧ (Type_Of_Real_Estate = Residential) ∧ (Use = Social_Housing) ∧ ((Seller = Vlaamse_Mpy_Voor_Sociaal_Wonen) ∨ (Seller = ErkendeSocialeHuisvestingsMpy)) ∧ Mortgage_Loan_Allowance)
  (Registration_Type = Energy_Efficient_Dwelling) ⇒ ((Type_Of_Real_Estate = Residential) ∧ (Buyer = Natural_Person) ∧ Domicile_Established ∧ Clean_Purchase ∧ (First_Ownership ∨ Causal_Connection) ∧ Energy_Renovation_Planned ∧ (Term_Energy_Renovation = (5 + Certification_Date)))
  (Registration_Type = Dwelling_For_Social_Renting) ⇒ ((Type_Of_Real_Estate = Residential) ∧ (Use = Social_Renting) ∧ (Start_Dt_Dwelling_For_Social_Rent = (3 + Certification_Date)) ∧ (Duration_Of_Agreement = Less_Than_9_years))
  ((Registration_Type = Heritage) ⇒ ((Type_Of_Real_Estate = Residential) ∧ Monument ∧ (Use = As_Family_Dwelling) ∧ Heritage_Investment ∧ Heritage_Plan ∧ Additional_Terms))
  (Registration_Type = Professional_Purchase) ⇒ (Professional_Buyer ∧ (~(Transaction_Type = Public_Sale)) ∧ (Use = For_Resale) ∧ (Certification_Date_Sale = (8 + Certification_Date)))
  ((Registration_Type = Social_Purpose) ⇒ (((Seller = Mpy_Erkend_Door_VMSW) ∨ (Seller = Vlaams_Woningfonds) ∨ (Seller = Gelijksoortige_Rechtspersoon_EER)) ∧ (Use = Community_Purpose)))
  (Registration_Type = Exchange_Unbuilt_Ground) ⇒ (Additional_Terms ∧ (~(Monument)))
  (Registration_Type = Other) ⇒ ((~(Registration_Type = Family_Dwelling)) ∧ (~(Registration_Type = Social_Dwelling)) ∧ (~(Registration_Type = Energy_Efficient_Dwelling)) ∧ (~(Registration_Type = Dwelling_For_Social_Renting)) ∧ (~(Registration_Type = Heritage)) ∧ (~(Registration_Type = Professional_Purchase)) ∧ (~(Registration_Type = Social_Purpose)) ∧ (~(Registration_Type = Exchange_Unbuilt_Ground)))
  Professional_Buyer ⇒ (Professional_Declaration_Filed ∧ Guarantee_Satisfied ∧ ((Additional_Security_Required ∧ Additional_Security_Satisfied) ∨ (~(Additional_Security_Required))) ∧ (Resale = Three_Or_More))
  (Tax = 1) ∨ (Tax = 2) ∨ (Tax = 4) ∨ (Tax = 7) ∨ (Tax = 6) ∨ (Tax = 10) ∨ (Tax = 12)
  (Region = Flemish_Region) ∨ (Region = Walloon_Region) ∨ (Region = Brussels_Region)
  (Type_Of_Real_Estate = Residential) ∨ (Type_Of_Real_Estate = Residential_Building_Land) ∨ (Type_Of_Real_Estate = Other_Real_Estate)
  (Seller = Vlaams_Woningfonds) ∨ (Seller = Gelijksoortige_Rechtspersoon_EER) ∨ (Seller = Mpy_Erkend_Door_VMSW) ∨ (Seller = Vlaamse_Mpy_Voor_Sociaal_Wonen) ∨ (Seller = ErkendeSocialeHuisvestingsMpy)
  (Buyer = Natural_Person) ∨ (Buyer = Legal_Person) ∨ (Buyer = Mixed)
  (Use = As_Family_Dwelling) ∨ (Use = For_Resale) ∨ (Use = Community_Purpose) ∨ (Use = Social_Housing) ∨ (Use = Social_Renting) ∨ (Use = Other_House) ∨ (Use = No_House)
  (Resale = Less_Than_Three) ∨ (Resale = Three_Or_More)
  (Transaction_Type = Public_Sale) ∨ (Transaction_Type = Out_Hand) ∨ (Transaction_Type = Public_Sale_Community)
  (Duration_Of_Agreement = Less_Than_9_years) ∨ (Duration_Of_Agreement = More_than_9_Or_9_years)
  (Start_Dt_Dwelling_For_Social_Rent = 2015) ∨ (Start_Dt_Dwelling_For_Social_Rent = 2016) ∨ (Start_Dt_Dwelling_For_Social_Rent = 2017) ∨ (Start_Dt_Dwelling_For_Social_Rent = 2018) ∨ (Start_Dt_Dwelling_For_Social_Rent = 2019) ∨ (Start_Dt_Dwelling_For_Social_Rent = 2020) ∨ (Start_Dt_Dwelling_For_Social_Rent = 2021) ∨ (Start_Dt_Dwelling_For_Social_Rent = 2022) ∨ (Start_Dt_Dwelling_For_Social_Rent = 2023) ∨ (Start_Dt_Dwelling_For_Social_Rent = 2024) ∨ (Start_Dt_Dwelling_For_Social_Rent = 2025)
  (Certification_Date = 2015) ∨ (Certification_Date = 2016) ∨ (Certification_Date = 2017) ∨ (Certification_Date = 2018) ∨ (Certification_Date = 2019) ∨ (Certification_Date = 2020) ∨ (Certification_Date = 2021) ∨ (Certification_Date = 2022) ∨ (Certification_Date = 2023) ∨ (Certification_Date = 2024) ∨ (Certification_Date = 2025)
  (Term_Energy_Renovation = 2015) ∨ (Term_Energy_Renovation = 2016) ∨ (Term_Energy_Renovation = 2017) ∨ (Term_Energy_Renovation = 2018) ∨ (Term_Energy_Renovation = 2019) ∨ (Term_Energy_Renovation = 2020) ∨ (Term_Energy_Renovation = 2021) ∨ (Term_Energy_Renovation = 2022) ∨ (Term_Energy_Renovation = 2023) ∨ (Term_Energy_Renovation = 2024) ∨ (Term_Energy_Renovation = 2025)
  (Certification_Date_Sale = 2015) ∨ (Certification_Date_Sale = 2016) ∨ (Certification_Date_Sale = 2017) ∨ (Certification_Date_Sale = 2018) ∨ (Certification_Date_Sale = 2019) ∨ (Certification_Date_Sale = 2020) ∨ (Certification_Date_Sale = 2021) ∨ (Certification_Date_Sale = 2022) ∨ (Certification_Date_Sale = 2023) ∨ (Certification_Date_Sale = 2024) ∨ (Certification_Date_Sale = 2025)
  (Registration_Type = Family_Dwelling) ∨ (Registration_Type = Social_Dwelling) ∨ (Registration_Type = Social_Purpose) ∨ (Registration_Type = Exchange_Unbuilt_Ground) ∨ (Registration_Type = Professional_Purchase) ∨ (Registration_Type = Energy_Efficient_Dwelling) ∨ (Registration_Type = Heritage) ∨ (Registration_Type = Dwelling_For_Social_Renting) ∨ (Registration_Type = Other)
  (Tax = 1) ∨ (Tax = 2) ∨ (Tax = 4) ∨ (Tax = 7) ∨ (Tax = 6) ∨ (Tax = 10) ∨ (Tax = 12)
Irrelevant:  
  ? Municipality = other_Municipal
  ? Municipality = Aalst
  ? Municipality = Antwerpen
  ? Municipality = Boom
  ? Municipality = Brugge
  ? Municipality = Dendermonde
  ? Municipality = Genk
  ? Municipality = Gent
  ? Municipality = Hasselt
  ? Municipality = Kortrijk
  ? Municipality = Leuven
  ? Municipality = Mechelen
  ? Municipality = Oostende
  ? Municipality = Roeselare
  ? Municipality = SintNiklaas
  ? Municipality = Turnhout
  ? Municipality = Vilvoorde
  ? Municipality = Affligem
  ? Municipality = Asse
  ? Municipality = Beersel
  ? Municipality = Bever
  ? Municipality = Dilbeek
  ? Municipality = Drogenbos
  ? Municipality = Galmaarden
  ? Municipality = Gooik
  ? Municipality = Grimbergen
  ? Municipality = Halle
  ? Municipality = Herne
  ? Municipality = Hoeilaart
  ? Municipality = Kampenhout
  ? Municipality = KapelleopdenBos
  ? Municipality = Kraainem
  ? Municipality = Lennik
  ? Municipality = Liedekerke
  ? Municipality = Linkebeek
  ? Municipality = Londerzeel
  ? Municipality = Machelen
  ? Municipality = Meise
  ? Municipality = Merchtem
  ? Municipality = Opwijk
  ? Municipality = Overijse
  ? Municipality = Pepingen
  ? Municipality = Roosdaal
  ? Municipality = SintGenesiusRode
  ? Municipality = SintPietersLeeuw
  ? Municipality = Steenokkerzeel
  ? Municipality = Ternat
  ? Municipality = Wemmel
  ? Municipality = WezembeekOppem
  ? Municipality = Zaventem
  ? Municipality = Zemst
  ? Municipality = Bertem
  ? Municipality = Huldenberg
  ? Municipality = Kortenberg
  ? Municipality = Tervuren
  ? Municipality
  ? Core_City


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
                                                                   'relevant': True,
                                                                   'status': 'UNKNOWN',
                                                                   'typ': 'Bool'}},
 'Additional_Security_Satisfied': {'Additional_Security_Satisfied': {'environmental': True,
                                                                     'normal': True,
                                                                     'reading': 'Additional_Security_Satisfied',
                                                                     'relevant': True,
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
           'Buyer = Legal_Person': {'environmental': True,
                                    'normal': False,
                                    'reading': 'Buyer = Legal_Person',
                                    'relevant': True,
                                    'status': 'UNKNOWN',
                                    'typ': 'Bool'},
           'Buyer = Mixed': {'environmental': True,
                             'normal': False,
                             'reading': 'Buyer = Mixed',
                             'relevant': True,
                             'status': 'UNKNOWN',
                             'typ': 'Bool'},
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
                                                          '2025']},
                        'Certification_Date = 2015': {'environmental': True,
                                                      'normal': False,
                                                      'reading': 'Certification_Date = 2015',
                                                      'relevant': True,
                                                      'status': 'UNKNOWN',
                                                      'typ': 'Bool'},
                        'Certification_Date = 2016': {'environmental': True,
                                                      'normal': False,
                                                      'reading': 'Certification_Date = 2016',
                                                      'relevant': True,
                                                      'status': 'UNKNOWN',
                                                      'typ': 'Bool'},
                        'Certification_Date = 2017': {'environmental': True,
                                                      'normal': False,
                                                      'reading': 'Certification_Date = 2017',
                                                      'relevant': True,
                                                      'status': 'UNKNOWN',
                                                      'typ': 'Bool'},
                        'Certification_Date = 2018': {'environmental': True,
                                                      'normal': False,
                                                      'reading': 'Certification_Date = 2018',
                                                      'relevant': True,
                                                      'status': 'UNKNOWN',
                                                      'typ': 'Bool'},
                        'Certification_Date = 2019': {'environmental': True,
                                                      'normal': False,
                                                      'reading': 'Certification_Date = 2019',
                                                      'relevant': True,
                                                      'status': 'UNKNOWN',
                                                      'typ': 'Bool'},
                        'Certification_Date = 2020': {'environmental': True,
                                                      'normal': False,
                                                      'reading': 'Certification_Date = 2020',
                                                      'relevant': True,
                                                      'status': 'UNKNOWN',
                                                      'typ': 'Bool'},
                        'Certification_Date = 2021': {'environmental': True,
                                                      'normal': False,
                                                      'reading': 'Certification_Date = 2021',
                                                      'relevant': True,
                                                      'status': 'UNKNOWN',
                                                      'typ': 'Bool'},
                        'Certification_Date = 2022': {'environmental': True,
                                                      'normal': False,
                                                      'reading': 'Certification_Date = 2022',
                                                      'relevant': True,
                                                      'status': 'UNKNOWN',
                                                      'typ': 'Bool'},
                        'Certification_Date = 2023': {'environmental': True,
                                                      'normal': False,
                                                      'reading': 'Certification_Date = 2023',
                                                      'relevant': True,
                                                      'status': 'UNKNOWN',
                                                      'typ': 'Bool'},
                        'Certification_Date = 2024': {'environmental': True,
                                                      'normal': False,
                                                      'reading': 'Certification_Date = 2024',
                                                      'relevant': True,
                                                      'status': 'UNKNOWN',
                                                      'typ': 'Bool'},
                        'Certification_Date = 2025': {'environmental': True,
                                                      'normal': False,
                                                      'reading': 'Certification_Date = 2025',
                                                      'relevant': True,
                                                      'status': 'UNKNOWN',
                                                      'typ': 'Bool'}},
 'Certification_Date_Sale': {'Certification_Date_Sale': {'environmental': True,
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
                             'Certification_Date_Sale = (Certification_Date + 8)': {'environmental': True,
                                                                                    'normal': False,
                                                                                    'reading': 'Certification_Date_Sale '
                                                                                               '= (Certification_Date '
                                                                                               '+ 8)',
                                                                                    'relevant': True,
                                                                                    'status': 'UNKNOWN',
                                                                                    'typ': 'Bool'},
                             'Certification_Date_Sale = 2015': {'environmental': True,
                                                                'normal': False,
                                                                'reading': 'Certification_Date_Sale = 2015',
                                                                'relevant': True,
                                                                'status': 'UNKNOWN',
                                                                'typ': 'Bool'},
                             'Certification_Date_Sale = 2016': {'environmental': True,
                                                                'normal': False,
                                                                'reading': 'Certification_Date_Sale = 2016',
                                                                'relevant': True,
                                                                'status': 'UNKNOWN',
                                                                'typ': 'Bool'},
                             'Certification_Date_Sale = 2017': {'environmental': True,
                                                                'normal': False,
                                                                'reading': 'Certification_Date_Sale = 2017',
                                                                'relevant': True,
                                                                'status': 'UNKNOWN',
                                                                'typ': 'Bool'},
                             'Certification_Date_Sale = 2018': {'environmental': True,
                                                                'normal': False,
                                                                'reading': 'Certification_Date_Sale = 2018',
                                                                'relevant': True,
                                                                'status': 'UNKNOWN',
                                                                'typ': 'Bool'},
                             'Certification_Date_Sale = 2019': {'environmental': True,
                                                                'normal': False,
                                                                'reading': 'Certification_Date_Sale = 2019',
                                                                'relevant': True,
                                                                'status': 'UNKNOWN',
                                                                'typ': 'Bool'},
                             'Certification_Date_Sale = 2020': {'environmental': True,
                                                                'normal': False,
                                                                'reading': 'Certification_Date_Sale = 2020',
                                                                'relevant': True,
                                                                'status': 'UNKNOWN',
                                                                'typ': 'Bool'},
                             'Certification_Date_Sale = 2021': {'environmental': True,
                                                                'normal': False,
                                                                'reading': 'Certification_Date_Sale = 2021',
                                                                'relevant': True,
                                                                'status': 'UNKNOWN',
                                                                'typ': 'Bool'},
                             'Certification_Date_Sale = 2022': {'environmental': True,
                                                                'normal': False,
                                                                'reading': 'Certification_Date_Sale = 2022',
                                                                'relevant': True,
                                                                'status': 'UNKNOWN',
                                                                'typ': 'Bool'},
                             'Certification_Date_Sale = 2023': {'environmental': True,
                                                                'normal': False,
                                                                'reading': 'Certification_Date_Sale = 2023',
                                                                'relevant': True,
                                                                'status': 'UNKNOWN',
                                                                'typ': 'Bool'},
                             'Certification_Date_Sale = 2024': {'environmental': True,
                                                                'normal': False,
                                                                'reading': 'Certification_Date_Sale = 2024',
                                                                'relevant': True,
                                                                'status': 'UNKNOWN',
                                                                'typ': 'Bool'},
                             'Certification_Date_Sale = 2025': {'environmental': True,
                                                                'normal': False,
                                                                'reading': 'Certification_Date_Sale = 2025',
                                                                'relevant': True,
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
                                                                         'typ': 'Bool'},
                           'Duration_Of_Agreement = More_than_9_Or_9_years': {'environmental': True,
                                                                              'normal': False,
                                                                              'reading': 'Duration_Of_Agreement = '
                                                                                         'More_than_9_Or_9_years',
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
                                                 'relevant': True,
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
                                              'Tervuren']},
                  'Municipality = Aalst': {'environmental': True,
                                           'normal': False,
                                           'reading': 'Municipality = Aalst',
                                           'relevant': False,
                                           'status': 'UNKNOWN',
                                           'typ': 'Bool'},
                  'Municipality = Affligem': {'environmental': True,
                                              'normal': False,
                                              'reading': 'Municipality = Affligem',
                                              'relevant': False,
                                              'status': 'UNKNOWN',
                                              'typ': 'Bool'},
                  'Municipality = Antwerpen': {'environmental': True,
                                               'normal': False,
                                               'reading': 'Municipality = Antwerpen',
                                               'relevant': False,
                                               'status': 'UNKNOWN',
                                               'typ': 'Bool'},
                  'Municipality = Asse': {'environmental': True,
                                          'normal': False,
                                          'reading': 'Municipality = Asse',
                                          'relevant': False,
                                          'status': 'UNKNOWN',
                                          'typ': 'Bool'},
                  'Municipality = Beersel': {'environmental': True,
                                             'normal': False,
                                             'reading': 'Municipality = Beersel',
                                             'relevant': False,
                                             'status': 'UNKNOWN',
                                             'typ': 'Bool'},
                  'Municipality = Bertem': {'environmental': True,
                                            'normal': False,
                                            'reading': 'Municipality = Bertem',
                                            'relevant': False,
                                            'status': 'UNKNOWN',
                                            'typ': 'Bool'},
                  'Municipality = Bever': {'environmental': True,
                                           'normal': False,
                                           'reading': 'Municipality = Bever',
                                           'relevant': False,
                                           'status': 'UNKNOWN',
                                           'typ': 'Bool'},
                  'Municipality = Boom': {'environmental': True,
                                          'normal': False,
                                          'reading': 'Municipality = Boom',
                                          'relevant': False,
                                          'status': 'UNKNOWN',
                                          'typ': 'Bool'},
                  'Municipality = Brugge': {'environmental': True,
                                            'normal': False,
                                            'reading': 'Municipality = Brugge',
                                            'relevant': False,
                                            'status': 'UNKNOWN',
                                            'typ': 'Bool'},
                  'Municipality = Dendermonde': {'environmental': True,
                                                 'normal': False,
                                                 'reading': 'Municipality = Dendermonde',
                                                 'relevant': False,
                                                 'status': 'UNKNOWN',
                                                 'typ': 'Bool'},
                  'Municipality = Dilbeek': {'environmental': True,
                                             'normal': False,
                                             'reading': 'Municipality = Dilbeek',
                                             'relevant': False,
                                             'status': 'UNKNOWN',
                                             'typ': 'Bool'},
                  'Municipality = Drogenbos': {'environmental': True,
                                               'normal': False,
                                               'reading': 'Municipality = Drogenbos',
                                               'relevant': False,
                                               'status': 'UNKNOWN',
                                               'typ': 'Bool'},
                  'Municipality = Galmaarden': {'environmental': True,
                                                'normal': False,
                                                'reading': 'Municipality = Galmaarden',
                                                'relevant': False,
                                                'status': 'UNKNOWN',
                                                'typ': 'Bool'},
                  'Municipality = Genk': {'environmental': True,
                                          'normal': False,
                                          'reading': 'Municipality = Genk',
                                          'relevant': False,
                                          'status': 'UNKNOWN',
                                          'typ': 'Bool'},
                  'Municipality = Gent': {'environmental': True,
                                          'normal': False,
                                          'reading': 'Municipality = Gent',
                                          'relevant': False,
                                          'status': 'UNKNOWN',
                                          'typ': 'Bool'},
                  'Municipality = Gooik': {'environmental': True,
                                           'normal': False,
                                           'reading': 'Municipality = Gooik',
                                           'relevant': False,
                                           'status': 'UNKNOWN',
                                           'typ': 'Bool'},
                  'Municipality = Grimbergen': {'environmental': True,
                                                'normal': False,
                                                'reading': 'Municipality = Grimbergen',
                                                'relevant': False,
                                                'status': 'UNKNOWN',
                                                'typ': 'Bool'},
                  'Municipality = Halle': {'environmental': True,
                                           'normal': False,
                                           'reading': 'Municipality = Halle',
                                           'relevant': False,
                                           'status': 'UNKNOWN',
                                           'typ': 'Bool'},
                  'Municipality = Hasselt': {'environmental': True,
                                             'normal': False,
                                             'reading': 'Municipality = Hasselt',
                                             'relevant': False,
                                             'status': 'UNKNOWN',
                                             'typ': 'Bool'},
                  'Municipality = Herne': {'environmental': True,
                                           'normal': False,
                                           'reading': 'Municipality = Herne',
                                           'relevant': False,
                                           'status': 'UNKNOWN',
                                           'typ': 'Bool'},
                  'Municipality = Hoeilaart': {'environmental': True,
                                               'normal': False,
                                               'reading': 'Municipality = Hoeilaart',
                                               'relevant': False,
                                               'status': 'UNKNOWN',
                                               'typ': 'Bool'},
                  'Municipality = Huldenberg': {'environmental': True,
                                                'normal': False,
                                                'reading': 'Municipality = Huldenberg',
                                                'relevant': False,
                                                'status': 'UNKNOWN',
                                                'typ': 'Bool'},
                  'Municipality = Kampenhout': {'environmental': True,
                                                'normal': False,
                                                'reading': 'Municipality = Kampenhout',
                                                'relevant': False,
                                                'status': 'UNKNOWN',
                                                'typ': 'Bool'},
                  'Municipality = KapelleopdenBos': {'environmental': True,
                                                     'normal': False,
                                                     'reading': 'Municipality = KapelleopdenBos',
                                                     'relevant': False,
                                                     'status': 'UNKNOWN',
                                                     'typ': 'Bool'},
                  'Municipality = Kortenberg': {'environmental': True,
                                                'normal': False,
                                                'reading': 'Municipality = Kortenberg',
                                                'relevant': False,
                                                'status': 'UNKNOWN',
                                                'typ': 'Bool'},
                  'Municipality = Kortrijk': {'environmental': True,
                                              'normal': False,
                                              'reading': 'Municipality = Kortrijk',
                                              'relevant': False,
                                              'status': 'UNKNOWN',
                                              'typ': 'Bool'},
                  'Municipality = Kraainem': {'environmental': True,
                                              'normal': False,
                                              'reading': 'Municipality = Kraainem',
                                              'relevant': False,
                                              'status': 'UNKNOWN',
                                              'typ': 'Bool'},
                  'Municipality = Lennik': {'environmental': True,
                                            'normal': False,
                                            'reading': 'Municipality = Lennik',
                                            'relevant': False,
                                            'status': 'UNKNOWN',
                                            'typ': 'Bool'},
                  'Municipality = Leuven': {'environmental': True,
                                            'normal': False,
                                            'reading': 'Municipality = Leuven',
                                            'relevant': False,
                                            'status': 'UNKNOWN',
                                            'typ': 'Bool'},
                  'Municipality = Liedekerke': {'environmental': True,
                                                'normal': False,
                                                'reading': 'Municipality = Liedekerke',
                                                'relevant': False,
                                                'status': 'UNKNOWN',
                                                'typ': 'Bool'},
                  'Municipality = Linkebeek': {'environmental': True,
                                               'normal': False,
                                               'reading': 'Municipality = Linkebeek',
                                               'relevant': False,
                                               'status': 'UNKNOWN',
                                               'typ': 'Bool'},
                  'Municipality = Londerzeel': {'environmental': True,
                                                'normal': False,
                                                'reading': 'Municipality = Londerzeel',
                                                'relevant': False,
                                                'status': 'UNKNOWN',
                                                'typ': 'Bool'},
                  'Municipality = Machelen': {'environmental': True,
                                              'normal': False,
                                              'reading': 'Municipality = Machelen',
                                              'relevant': False,
                                              'status': 'UNKNOWN',
                                              'typ': 'Bool'},
                  'Municipality = Mechelen': {'environmental': True,
                                              'normal': False,
                                              'reading': 'Municipality = Mechelen',
                                              'relevant': False,
                                              'status': 'UNKNOWN',
                                              'typ': 'Bool'},
                  'Municipality = Meise': {'environmental': True,
                                           'normal': False,
                                           'reading': 'Municipality = Meise',
                                           'relevant': False,
                                           'status': 'UNKNOWN',
                                           'typ': 'Bool'},
                  'Municipality = Merchtem': {'environmental': True,
                                              'normal': False,
                                              'reading': 'Municipality = Merchtem',
                                              'relevant': False,
                                              'status': 'UNKNOWN',
                                              'typ': 'Bool'},
                  'Municipality = Oostende': {'environmental': True,
                                              'normal': False,
                                              'reading': 'Municipality = Oostende',
                                              'relevant': False,
                                              'status': 'UNKNOWN',
                                              'typ': 'Bool'},
                  'Municipality = Opwijk': {'environmental': True,
                                            'normal': False,
                                            'reading': 'Municipality = Opwijk',
                                            'relevant': False,
                                            'status': 'UNKNOWN',
                                            'typ': 'Bool'},
                  'Municipality = Overijse': {'environmental': True,
                                              'normal': False,
                                              'reading': 'Municipality = Overijse',
                                              'relevant': False,
                                              'status': 'UNKNOWN',
                                              'typ': 'Bool'},
                  'Municipality = Pepingen': {'environmental': True,
                                              'normal': False,
                                              'reading': 'Municipality = Pepingen',
                                              'relevant': False,
                                              'status': 'UNKNOWN',
                                              'typ': 'Bool'},
                  'Municipality = Roeselare': {'environmental': True,
                                               'normal': False,
                                               'reading': 'Municipality = Roeselare',
                                               'relevant': False,
                                               'status': 'UNKNOWN',
                                               'typ': 'Bool'},
                  'Municipality = Roosdaal': {'environmental': True,
                                              'normal': False,
                                              'reading': 'Municipality = Roosdaal',
                                              'relevant': False,
                                              'status': 'UNKNOWN',
                                              'typ': 'Bool'},
                  'Municipality = SintGenesiusRode': {'environmental': True,
                                                      'normal': False,
                                                      'reading': 'Municipality = SintGenesiusRode',
                                                      'relevant': False,
                                                      'status': 'UNKNOWN',
                                                      'typ': 'Bool'},
                  'Municipality = SintNiklaas': {'environmental': True,
                                                 'normal': False,
                                                 'reading': 'Municipality = SintNiklaas',
                                                 'relevant': False,
                                                 'status': 'UNKNOWN',
                                                 'typ': 'Bool'},
                  'Municipality = SintPietersLeeuw': {'environmental': True,
                                                      'normal': False,
                                                      'reading': 'Municipality = SintPietersLeeuw',
                                                      'relevant': False,
                                                      'status': 'UNKNOWN',
                                                      'typ': 'Bool'},
                  'Municipality = Steenokkerzeel': {'environmental': True,
                                                    'normal': False,
                                                    'reading': 'Municipality = Steenokkerzeel',
                                                    'relevant': False,
                                                    'status': 'UNKNOWN',
                                                    'typ': 'Bool'},
                  'Municipality = Ternat': {'environmental': True,
                                            'normal': False,
                                            'reading': 'Municipality = Ternat',
                                            'relevant': False,
                                            'status': 'UNKNOWN',
                                            'typ': 'Bool'},
                  'Municipality = Tervuren': {'environmental': True,
                                              'normal': False,
                                              'reading': 'Municipality = Tervuren',
                                              'relevant': False,
                                              'status': 'UNKNOWN',
                                              'typ': 'Bool'},
                  'Municipality = Turnhout': {'environmental': True,
                                              'normal': False,
                                              'reading': 'Municipality = Turnhout',
                                              'relevant': False,
                                              'status': 'UNKNOWN',
                                              'typ': 'Bool'},
                  'Municipality = Vilvoorde': {'environmental': True,
                                               'normal': False,
                                               'reading': 'Municipality = Vilvoorde',
                                               'relevant': False,
                                               'status': 'UNKNOWN',
                                               'typ': 'Bool'},
                  'Municipality = Wemmel': {'environmental': True,
                                            'normal': False,
                                            'reading': 'Municipality = Wemmel',
                                            'relevant': False,
                                            'status': 'UNKNOWN',
                                            'typ': 'Bool'},
                  'Municipality = WezembeekOppem': {'environmental': True,
                                                    'normal': False,
                                                    'reading': 'Municipality = WezembeekOppem',
                                                    'relevant': False,
                                                    'status': 'UNKNOWN',
                                                    'typ': 'Bool'},
                  'Municipality = Zaventem': {'environmental': True,
                                              'normal': False,
                                              'reading': 'Municipality = Zaventem',
                                              'relevant': False,
                                              'status': 'UNKNOWN',
                                              'typ': 'Bool'},
                  'Municipality = Zemst': {'environmental': True,
                                           'normal': False,
                                           'reading': 'Municipality = Zemst',
                                           'relevant': False,
                                           'status': 'UNKNOWN',
                                           'typ': 'Bool'},
                  'Municipality = other_Municipal': {'environmental': True,
                                                     'normal': False,
                                                     'reading': 'Municipality = other_Municipal',
                                                     'relevant': False,
                                                     'status': 'UNKNOWN',
                                                     'typ': 'Bool'}},
 'Professional_Buyer': {'Professional_Buyer': {'environmental': True,
                                               'normal': True,
                                               'reading': 'Professional_Buyer',
                                               'relevant': True,
                                               'status': 'UNKNOWN',
                                               'typ': 'Bool'}},
 'Professional_Declaration_Filed': {'Professional_Declaration_Filed': {'environmental': True,
                                                                       'normal': True,
                                                                       'reading': 'Professional_Declaration_Filed',
                                                                       'relevant': True,
                                                                       'status': 'UNKNOWN',
                                                                       'typ': 'Bool'}},
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
                                                                     'status': 'UNKNOWN',
                                                                     'typ': 'Bool'},
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
                       'relevant': True,
                       'status': 'UNKNOWN',
                       'typ': 'resale',
                       'value': '',
                       'values': ['Less_Than_Three', 'Three_Or_More']},
            'Resale = Less_Than_Three': {'environmental': True,
                                         'normal': False,
                                         'reading': 'Resale = Less_Than_Three',
                                         'relevant': True,
                                         'status': 'UNKNOWN',
                                         'typ': 'Bool'},
            'Resale = Three_Or_More': {'environmental': True,
                                       'normal': False,
                                       'reading': 'Resale = Three_Or_More',
                                       'relevant': True,
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
                                                                                                        'typ': 'Bool'},
                                       'Start_Dt_Dwelling_For_Social_Rent = 2015': {'environmental': True,
                                                                                    'normal': False,
                                                                                    'reading': 'Start_Dt_Dwelling_For_Social_Rent '
                                                                                               '= 2015',
                                                                                    'relevant': True,
                                                                                    'status': 'UNKNOWN',
                                                                                    'typ': 'Bool'},
                                       'Start_Dt_Dwelling_For_Social_Rent = 2016': {'environmental': True,
                                                                                    'normal': False,
                                                                                    'reading': 'Start_Dt_Dwelling_For_Social_Rent '
                                                                                               '= 2016',
                                                                                    'relevant': True,
                                                                                    'status': 'UNKNOWN',
                                                                                    'typ': 'Bool'},
                                       'Start_Dt_Dwelling_For_Social_Rent = 2017': {'environmental': True,
                                                                                    'normal': False,
                                                                                    'reading': 'Start_Dt_Dwelling_For_Social_Rent '
                                                                                               '= 2017',
                                                                                    'relevant': True,
                                                                                    'status': 'UNKNOWN',
                                                                                    'typ': 'Bool'},
                                       'Start_Dt_Dwelling_For_Social_Rent = 2018': {'environmental': True,
                                                                                    'normal': False,
                                                                                    'reading': 'Start_Dt_Dwelling_For_Social_Rent '
                                                                                               '= 2018',
                                                                                    'relevant': True,
                                                                                    'status': 'UNKNOWN',
                                                                                    'typ': 'Bool'},
                                       'Start_Dt_Dwelling_For_Social_Rent = 2019': {'environmental': True,
                                                                                    'normal': False,
                                                                                    'reading': 'Start_Dt_Dwelling_For_Social_Rent '
                                                                                               '= 2019',
                                                                                    'relevant': True,
                                                                                    'status': 'UNKNOWN',
                                                                                    'typ': 'Bool'},
                                       'Start_Dt_Dwelling_For_Social_Rent = 2020': {'environmental': True,
                                                                                    'normal': False,
                                                                                    'reading': 'Start_Dt_Dwelling_For_Social_Rent '
                                                                                               '= 2020',
                                                                                    'relevant': True,
                                                                                    'status': 'UNKNOWN',
                                                                                    'typ': 'Bool'},
                                       'Start_Dt_Dwelling_For_Social_Rent = 2021': {'environmental': True,
                                                                                    'normal': False,
                                                                                    'reading': 'Start_Dt_Dwelling_For_Social_Rent '
                                                                                               '= 2021',
                                                                                    'relevant': True,
                                                                                    'status': 'UNKNOWN',
                                                                                    'typ': 'Bool'},
                                       'Start_Dt_Dwelling_For_Social_Rent = 2022': {'environmental': True,
                                                                                    'normal': False,
                                                                                    'reading': 'Start_Dt_Dwelling_For_Social_Rent '
                                                                                               '= 2022',
                                                                                    'relevant': True,
                                                                                    'status': 'UNKNOWN',
                                                                                    'typ': 'Bool'},
                                       'Start_Dt_Dwelling_For_Social_Rent = 2023': {'environmental': True,
                                                                                    'normal': False,
                                                                                    'reading': 'Start_Dt_Dwelling_For_Social_Rent '
                                                                                               '= 2023',
                                                                                    'relevant': True,
                                                                                    'status': 'UNKNOWN',
                                                                                    'typ': 'Bool'},
                                       'Start_Dt_Dwelling_For_Social_Rent = 2024': {'environmental': True,
                                                                                    'normal': False,
                                                                                    'reading': 'Start_Dt_Dwelling_For_Social_Rent '
                                                                                               '= 2024',
                                                                                    'relevant': True,
                                                                                    'status': 'UNKNOWN',
                                                                                    'typ': 'Bool'},
                                       'Start_Dt_Dwelling_For_Social_Rent = 2025': {'environmental': True,
                                                                                    'normal': False,
                                                                                    'reading': 'Start_Dt_Dwelling_For_Social_Rent '
                                                                                               '= 2025',
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
                     'status': 'UNKNOWN',
                     'typ': 'Bool'},
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
                                                                                  'typ': 'Bool'},
                            'Term_Energy_Renovation = 2015': {'environmental': True,
                                                              'normal': False,
                                                              'reading': 'Term_Energy_Renovation = 2015',
                                                              'relevant': True,
                                                              'status': 'UNKNOWN',
                                                              'typ': 'Bool'},
                            'Term_Energy_Renovation = 2016': {'environmental': True,
                                                              'normal': False,
                                                              'reading': 'Term_Energy_Renovation = 2016',
                                                              'relevant': True,
                                                              'status': 'UNKNOWN',
                                                              'typ': 'Bool'},
                            'Term_Energy_Renovation = 2017': {'environmental': True,
                                                              'normal': False,
                                                              'reading': 'Term_Energy_Renovation = 2017',
                                                              'relevant': True,
                                                              'status': 'UNKNOWN',
                                                              'typ': 'Bool'},
                            'Term_Energy_Renovation = 2018': {'environmental': True,
                                                              'normal': False,
                                                              'reading': 'Term_Energy_Renovation = 2018',
                                                              'relevant': True,
                                                              'status': 'UNKNOWN',
                                                              'typ': 'Bool'},
                            'Term_Energy_Renovation = 2019': {'environmental': True,
                                                              'normal': False,
                                                              'reading': 'Term_Energy_Renovation = 2019',
                                                              'relevant': True,
                                                              'status': 'UNKNOWN',
                                                              'typ': 'Bool'},
                            'Term_Energy_Renovation = 2020': {'environmental': True,
                                                              'normal': False,
                                                              'reading': 'Term_Energy_Renovation = 2020',
                                                              'relevant': True,
                                                              'status': 'UNKNOWN',
                                                              'typ': 'Bool'},
                            'Term_Energy_Renovation = 2021': {'environmental': True,
                                                              'normal': False,
                                                              'reading': 'Term_Energy_Renovation = 2021',
                                                              'relevant': True,
                                                              'status': 'UNKNOWN',
                                                              'typ': 'Bool'},
                            'Term_Energy_Renovation = 2022': {'environmental': True,
                                                              'normal': False,
                                                              'reading': 'Term_Energy_Renovation = 2022',
                                                              'relevant': True,
                                                              'status': 'UNKNOWN',
                                                              'typ': 'Bool'},
                            'Term_Energy_Renovation = 2023': {'environmental': True,
                                                              'normal': False,
                                                              'reading': 'Term_Energy_Renovation = 2023',
                                                              'relevant': True,
                                                              'status': 'UNKNOWN',
                                                              'typ': 'Bool'},
                            'Term_Energy_Renovation = 2024': {'environmental': True,
                                                              'normal': False,
                                                              'reading': 'Term_Energy_Renovation = 2024',
                                                              'relevant': True,
                                                              'status': 'UNKNOWN',
                                                              'typ': 'Bool'},
                            'Term_Energy_Renovation = 2025': {'environmental': True,
                                                              'normal': False,
                                                              'reading': 'Term_Energy_Renovation = 2025',
                                                              'relevant': True,
                                                              'status': 'UNKNOWN',
                                                              'typ': 'Bool'}},
 'Transaction_Type': {'Transaction_Type': {'environmental': True,
                                           'normal': True,
                                           'reading': 'Transaction_Type',
                                           'relevant': True,
                                           'status': 'UNKNOWN',
                                           'typ': 'transaction',
                                           'value': '',
                                           'values': ['Public_Sale', 'Out_Hand', 'Public_Sale_Community']},
                      'Transaction_Type = Out_Hand': {'environmental': True,
                                                      'normal': False,
                                                      'reading': 'Transaction_Type = Out_Hand',
                                                      'relevant': True,
                                                      'status': 'UNKNOWN',
                                                      'typ': 'Bool'},
                      'Transaction_Type = Public_Sale': {'environmental': True,
                                                         'normal': False,
                                                         'reading': 'Transaction_Type = Public_Sale',
                                                         'relevant': True,
                                                         'status': 'UNKNOWN',
                                                         'typ': 'Bool'},
                      'Transaction_Type = Public_Sale_Community': {'environmental': True,
                                                                   'normal': False,
                                                                   'reading': 'Transaction_Type = '
                                                                              'Public_Sale_Community',
                                                                   'relevant': True,
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
                         'Type_Of_Real_Estate = Other_Real_Estate': {'environmental': True,
                                                                     'normal': False,
                                                                     'reading': 'Type_Of_Real_Estate = '
                                                                                'Other_Real_Estate',
                                                                     'relevant': True,
                                                                     'status': 'UNKNOWN',
                                                                     'typ': 'Bool'},
                         'Type_Of_Real_Estate = Residential': {'environmental': True,
                                                               'normal': False,
                                                               'reading': 'Type_Of_Real_Estate = Residential',
                                                               'relevant': True,
                                                               'status': 'UNKNOWN',
                                                               'typ': 'Bool'},
                         'Type_Of_Real_Estate = Residential_Building_Land': {'environmental': True,
                                                                             'normal': False,
                                                                             'reading': 'Type_Of_Real_Estate = '
                                                                                        'Residential_Building_Land',
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
                              'relevant': True,
                              'status': 'UNKNOWN',
                              'typ': 'Bool'},
         'Use = No_House': {'environmental': True,
                            'normal': False,
                            'reading': 'Use = No_House',
                            'relevant': True,
                            'status': 'UNKNOWN',
                            'typ': 'Bool'},
         'Use = Other_House': {'environmental': True,
                               'normal': False,
                               'reading': 'Use = Other_House',
                               'relevant': True,
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
