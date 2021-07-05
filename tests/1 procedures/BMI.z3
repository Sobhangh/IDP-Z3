No more consequences.
['Male', 'Female']

bmi() -> 0.00249680097375238
riskLevel() -> Low
No more consequences.

length() = 179
weight() = 80
∀$BMILevel$ ∈ BMILevelt_t : BMILevel() = $BMILevel$ ⇒ $BMILevel$ = Severely_Underweight ∧ (bmi() < 18.5 ∧ sex() = Male) ∨ $BMILevel$ = Underweight ∧ (bmi() < 18.5 ∧ sex() = Female) ∨ $BMILevel$ = Underweight ∧ (18.5 ≤ bmi() ∧ bmi() ≤ 24.9 ∧ sex() = Male) ∨ $BMILevel$ = Normal ∧ (18.5 ≤ bmi() ∧ bmi() ≤ 24.9 ∧ sex() = Female) ∨ $BMILevel$ = Normal ∧ (25 ≤ bmi() ∧ bmi() ≤ 29.9 ∧ sex() = Male) ∨ $BMILevel$ = Overweight ∧ (25 ≤ bmi() ∧ bmi() ≤ 29.9 ∧ sex() = Female) ∨ $BMILevel$ = Obese_I ∧ (30 ≤ bmi() ∧ bmi() ≤ 34.9) ∨ $BMILevel$ = Obese_II ∧ (35 ≤ bmi() ∧ bmi() ≤ 39.9) ∨ $BMILevel$ = Extreme_Obesity ∧ bmi() ≥ 40
∀$bmi$ ∈ ℝ : bmi() = $bmi$ ⇔ $bmi$ = weight() / (length() ⨯ length())
∀$riskLevel$ ∈ riskLevelt_t : riskLevel() = $riskLevel$ ⇐ $riskLevel$ = Low ∧ ¬((BMILevel() = Overweight ∨ BMILevel() = Obese_I ∨ BMILevel() = Obese_II ∨ BMILevel() = Extreme_Obesity))
