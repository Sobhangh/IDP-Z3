No more consequences.

bmi -> 0.00249680097375238
riskLevel -> Low
No more consequences.

length -> 179
weight -> 80
(BMILevel = Obese_II ⇔ 35 ≤ bmi ∧ bmi ≤ 39.9) ∧ (BMILevel = Obese_I ⇔ 30 ≤ bmi ∧ bmi ≤ 34.9) ∧ (BMILevel = Normal ⇔ false ∨ false ∨ false ∨ 18.5 ≤ bmi ∧ bmi ≤ 24.9 ∧ sex = Female ∨ 25 ≤ bmi ∧ bmi ≤ 29.9 ∧ sex = Male ∨ false ∨ false ∨ false ∨ false) ∧ (BMILevel = Severely_Underweight ⇔ bmi < 18.5 ∧ sex = Male) ∧ (BMILevel = Underweight ⇔ false ∨ bmi < 18.5 ∧ sex = Female ∨ 18.5 ≤ bmi ∧ bmi ≤ 24.9 ∧ sex = Male ∨ false ∨ false ∨ false ∨ false ∨ false ∨ false) ∧ (BMILevel = Overweight ⇔ 25 ≤ bmi ∧ bmi ≤ 29.9 ∧ sex = Female) ∧ (BMILevel = Extreme_Obesity ⇔ bmi ≥ 40)
(riskLevel = High ⇔ false ∨ BMILevel = Overweight ∧ sex = Male ∧ waist > 102 ∨ false ∨ BMILevel = Overweight ∧ sex = Female ∧ waist > 88 ∨ BMILevel = Obese_I ∧ sex = Male ∧ waist ≤ 102 ∨ false ∨ BMILevel = Obese_I ∧ sex = Female ∧ waist ≤ 88 ∨ false ∨ false ∨ false ∨ false) ∧ (riskLevel = Very_High ⇔ false ∨ false ∨ false ∨ false ∨ false ∨ BMILevel = Obese_I ∧ sex = Male ∧ waist > 102 ∨ false ∨ BMILevel = Obese_I ∧ sex = Female ∧ waist > 88 ∨ BMILevel = Obese_II ∨ false ∨ false) ∧ (riskLevel = Low ⇔ ¬((BMILevel = Overweight ∨ BMILevel = Obese_I ∨ BMILevel = Obese_II ∨ BMILevel = Extreme_Obesity))) ∧ (riskLevel = Increased ⇔ BMILevel = Overweight ∧ sex = Male ∧ waist ≤ 102 ∨ false ∨ BMILevel = Overweight ∧ sex = Female ∧ waist ≤ 88 ∨ false ∨ false ∨ false ∨ false ∨ false ∨ false ∨ false ∨ false) ∧ (riskLevel = Extremely_High ⇔ BMILevel = Extreme_Obesity)
