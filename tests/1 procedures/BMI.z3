weight() -> 80
No more consequences.
['Male', 'Female']

bmi() -> 0.003125
riskLevel() -> Low
weight() -> 80
No more consequences.

Low risk if neither Overweight, Obese_I, Obese_II nor Extreme_obesity
bmi() = $bmi$ ⇔ $bmi$ = weight() / (25600)
weight() = 80
BMILevel() = $BMILevel$ ⇐ $BMILevel$ = Underweight ∧ (bmi() < 18.5 ∧ sex() = Female)
BMILevel() = $BMILevel$ ⇐ $BMILevel$ = Severely_Underweight ∧ (bmi() < 18.5 ∧ sex() = Male)

(declare-datatypes ((BMILevelt_t 0)) (((Obese_II) (Obese_I) (Normal) (Severely_Underweight) (Underweight) (Overweight) (Extreme_Obesity))))
(declare-datatypes ((riskLevelt_t 0)) (((High) (Very_High) (Low) (Increased) (Extremely_High))))
(declare-datatypes ((sext_t 0)) (((Male) (Female))))
(declare-fun BMILevel () BMILevelt_t)
(declare-fun riskLevel () riskLevelt_t)
(declare-fun waist () Real)
(declare-fun sex () sext_t)
(declare-fun weight () Real)
(declare-fun bmi () Real)
(assert (let ((a!1 (and (<= (/ 37.0 2.0) bmi) (>= (/ 249.0 10.0) bmi) (= sex Male)))
      (a!2 (and (<= (/ 37.0 2.0) bmi) (>= (/ 249.0 10.0) bmi) (= sex Female)))
      (a!3 (and (<= (to_real 25) bmi) (>= (/ 299.0 10.0) bmi) (= sex Male)))
      (a!4 (and (<= (to_real 25) bmi) (>= (/ 299.0 10.0) bmi) (= sex Female)))
      (a!5 (and (= BMILevel Obese_I)
                (and (<= (to_real 30) bmi) (>= (/ 349.0 10.0) bmi))))
      (a!6 (and (= BMILevel Obese_II)
                (and (<= (to_real 35) bmi) (>= (/ 399.0 10.0) bmi))))
      (a!8 (= (= BMILevel Obese_II)
              (and (<= (to_real 35) bmi) (>= (/ 399.0 10.0) bmi))))
      (a!9 (= (= BMILevel Obese_I)
              (and (<= (to_real 30) bmi) (>= (/ 349.0 10.0) bmi))))
      (a!11 (forall ((c!0 Real))
              (= (= bmi c!0) (= c!0 (/ weight (to_real 25600))))))
      (a!12 (or false
                (and (= BMILevel Overweight)
                     (= sex Male)
                     (< (to_real 102) waist))
                false
                (and (= BMILevel Overweight)
                     (= sex Female)
                     (< (to_real 88) waist))
                (and (= BMILevel Obese_I) (= sex Male) (>= (to_real 102) waist))
                false
                (and (= BMILevel Obese_I)
                     (= sex Female)
                     (>= (to_real 88) waist))
                false
                false
                false
                false))
      (a!13 (or false
                false
                false
                false
                false
                (and (= BMILevel Obese_I) (= sex Male) (< (to_real 102) waist))
                false
                (and (= BMILevel Obese_I) (= sex Female) (< (to_real 88) waist))
                (= BMILevel Obese_II)
                false
                false))
      (a!14 (= (= riskLevel Low)
               (not (or (= BMILevel Overweight)
                        (= BMILevel Obese_I)
                        (= BMILevel Obese_II)
                        (= BMILevel Extreme_Obesity)))))
      (a!15 (or (and (= BMILevel Overweight)
                     (= sex Male)
                     (>= (to_real 102) waist))
                false
                (and (= BMILevel Overweight)
                     (= sex Female)
                     (>= (to_real 88) waist))
                false
                false
                false
                false
                false
                false
                false
                false)))
(let ((a!7 (or (and (= BMILevel Severely_Underweight)
                    (and (> (/ 37.0 2.0) bmi) (= sex Male)))
               (and (= BMILevel Underweight)
                    (and (> (/ 37.0 2.0) bmi) (= sex Female)))
               (and (= BMILevel Underweight) a!1)
               (and (= BMILevel Normal) a!2)
               (and (= BMILevel Normal) a!3)
               (and (= BMILevel Overweight) a!4)
               a!5
               a!6
               (and (= BMILevel Extreme_Obesity) (<= (to_real 40) bmi))))
      (a!10 (= (= BMILevel Underweight)
               (or false
                   (and (> (/ 37.0 2.0) bmi) (= sex Female))
                   a!1
                   false
                   false
                   false
                   false
                   false
                   false))))
  (and (= (to_real 80) weight)
       (or (= BMILevel Extreme_Obesity)
           (= BMILevel Normal)
           (= BMILevel Obese_I)
           (= BMILevel Obese_II)
           (= BMILevel Overweight)
           (= BMILevel Severely_Underweight)
           (= BMILevel Underweight))
       (or (= sex Female) (= sex Male))
       (or (= riskLevel Extremely_High)
           (= riskLevel High)
           (= riskLevel Increased)
           (= riskLevel Low)
           (= riskLevel Very_High))
       (= bmi (/ weight (to_real 25600)))
       a!7
       a!8
       a!9
       (= (= BMILevel Normal)
          (or false false false a!2 a!3 false false false false))
       (= (= BMILevel Severely_Underweight)
          (and (> (/ 37.0 2.0) bmi) (= sex Male)))
       a!10
       (= (= BMILevel Overweight) a!4)
       (= (= BMILevel Extreme_Obesity) (<= (to_real 40) bmi))
       a!11
       (= (= riskLevel High) a!12)
       (= (= riskLevel Very_High) a!13)
       a!14
       (= (= riskLevel Increased) a!15)
       (= (= riskLevel Extremely_High) (= BMILevel Extreme_Obesity))))))

