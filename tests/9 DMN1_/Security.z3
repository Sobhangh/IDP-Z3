  Not HasRating(BE001) ≤ 77
⇒ Not Eligible(BE001)

  Country(BE001) in {Aus, Bel, Can, Den, Est, Fin, Fra, Ger, Hon, Ire, Isr, Ita, Jap, Lux, Net, New, Nor, Por, Sin, Slo, Sou, Spa, Swe, Swi, UniK, UniS}
∧ Issuer_Type(BE001) = Sovereign
⇒ Eligible(BE001)

  Not AssetSubClass(BE001) = ABS
∧ Issuer(BE001) in {FederalHomeLoanMortgageCorporation, FederalNationalMortgageAssociation, GovernmentNationalMortgageAssociation}
⇒ Eligible(BE001)

  Not Issuer(BE001) in {ALBERTA, AfricanDevelopmentBank, BRITISHCOLUMBIA, BankForInternationalSettlements, CaribbeanDevelopmentBank, CouncilOfEuropeDevelopmentBank, EuropeanBankForReconstructionAndDevelopment, EuropeanCentralBank, EuropeanInvestmentBank, EuropeanInvestmentFund, InterAmericanDevelopmentBank, InternationalBankForReconstructionAndDevelopment, InternationalFinanceCorporation, InternationalMonetaryFund, MANITOBA, MultilateralInvestmentGuaranteeAgency, NEWBRUNSWICK, NEWBRUNsELEC, NEWFOUNDLAND, NOVASCOTIA, NordicInvestmentBank, ONTARIO, PRINCEEDWARDISLD, QUEBEC, SASKATCHEWAN, TORONTO}
⇒ Not Eligible(BE001)

  Not AssetSubClass(BE001) = ABS
∧ Issuer(BE001) in {ALBERTA, BRITISHCOLUMBIA, MANITOBA, NEWBRUNSWICK, NEWBRUNsELEC, NEWFOUNDLAND, NOVASCOTIA, ONTARIO, PRINCEEDWARDISLD, QUEBEC, SASKATCHEWAN, TORONTO}
⇒ Eligible(BE001)

  Not Issuer(BE001) in {ALBERTA, BRITISHCOLUMBIA, MANITOBA, NEWBRUNSWICK, NEWBRUNsELEC, NEWFOUNDLAND, NOVASCOTIA, ONTARIO, PRINCEEDWARDISLD, QUEBEC, SASKATCHEWAN, TORONTO}
∧ Issuer_Type(BE001) = Supra
⇒ Eligible(BE001)

⇒ Not Eligible(BE001)

end of decision table
