  Not HasRating(BE001) ≤ 77
⇒ Not Eligible(BE001)

  Not Issuer(BE001) = ALBERTA ∨ Issuer(BE001) = BRITISHCOLUMBIA ∨ Issuer(BE001) = FederalHomeLoanMortgageCorporation ∨ Issuer(BE001) = FederalNationalMortgageAssociation ∨ Issuer(BE001) = GovernmentNationalMortgageAssociation ∨ Issuer(BE001) = MANITOBA ∨ Issuer(BE001) = NEWBRUNSWICK ∨ Issuer(BE001) = NEWBRUNsELEC ∨ Issuer(BE001) = NEWFOUNDLAND ∨ Issuer(BE001) = NOVASCOTIA ∨ Issuer(BE001) = ONTARIO ∨ Issuer(BE001) = PRINCEEDWARDISLD ∨ Issuer(BE001) = QUEBEC ∨ Issuer(BE001) = SASKATCHEWAN ∨ Issuer(BE001) = TORONTO
∧ Not Issuer_Type(BE001) = Sovereign ∨ Issuer_Type(BE001) = Supra
⇒ Not Eligible(BE001)

  Country(BE001) in {Aus, Bel, Can, Den, Est, Fin, Fra, Ger, Hon, Ire, Isr, Ita, Jap, Lux, Net, New, Nor, Por, Sin, Slo, Sou, Spa, Swe, Swi, UniK, UniS}
∧ Issuer_Type(BE001) = Sovereign
⇒ Eligible(BE001)

  Issuer(BE001) in {AfricanDevelopmentBank, BankForInternationalSettlements, CaribbeanDevelopmentBank, CouncilOfEuropeDevelopmentBank, EuropeanBankForReconstructionAndDevelopment, EuropeanCentralBank, EuropeanInvestmentBank, EuropeanInvestmentFund, InterAmericanDevelopmentBank, InternationalBankForReconstructionAndDevelopment, InternationalFinanceCorporation, InternationalMonetaryFund, MultilateralInvestmentGuaranteeAgency, NordicInvestmentBank}
∧ Issuer_Type(BE001) = Supra
⇒ Eligible(BE001)

  Not AssetSubClass(BE001) = ABS
∧ Issuer(BE001) = ALBERTA ∨ Issuer(BE001) = BRITISHCOLUMBIA ∨ Issuer(BE001) = FederalHomeLoanMortgageCorporation ∨ Issuer(BE001) = FederalNationalMortgageAssociation ∨ Issuer(BE001) = GovernmentNationalMortgageAssociation ∨ Issuer(BE001) = MANITOBA ∨ Issuer(BE001) = NEWBRUNSWICK ∨ Issuer(BE001) = NEWBRUNsELEC ∨ Issuer(BE001) = NEWFOUNDLAND ∨ Issuer(BE001) = NOVASCOTIA ∨ Issuer(BE001) = ONTARIO ∨ Issuer(BE001) = PRINCEEDWARDISLD ∨ Issuer(BE001) = QUEBEC ∨ Issuer(BE001) = SASKATCHEWAN ∨ Issuer(BE001) = TORONTO
⇒ Eligible(BE001)

⇒ Not Eligible(BE001)

end of decision table
