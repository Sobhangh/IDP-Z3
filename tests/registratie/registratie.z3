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

Or(Tax == 1,
   Tax == 2,
   Tax == 4,
   Tax == 7,
   Tax == 6,
   Tax == 10,
   Tax == 12)

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
--
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
       Not(Term_Energy_Renovation == Certification_Date + 5)))

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
    Term_Energy_Renovation == Certification_Date + 5)

(Registration_Type == Dwelling_For_Social_Renting) ==
And(Type_Of_Real_Estate == Residential,
    Use == Social_Renting,
    Start_Dt_Dwelling_For_Social_Rent ==
    Certification_Date + 3,
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
    Certification_Date_Sale == Certification_Date + 8)

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
