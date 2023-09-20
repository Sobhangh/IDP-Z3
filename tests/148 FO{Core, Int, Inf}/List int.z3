(declare-datatypes ((List 0)) (((nil) (cons (car Int) (cdr List)))))
(declare-fun a () List)
(declare-fun increasing (List) Bool)
(declare-fun len (List) Int)
(declare-fun member (Int List) Bool)
(assert (let ((a!1 (forall ((c!0 List))
             (or (not (or ((_ is (nil () List)) c!0)
                          ((_ is (cons (Int List) List)) c!0)))
                 (= (= 0 (len c!0)) (= c!0 nil)))))
      (a!2 (or (and (= 0 (len a)) (= a nil))
               (exists ((c!1 Int))
                 (let ((a!1 (= (len a) (+ (len (cdr a)) 1))))
                   (and a!1 ((_ is (cons (Int List) List)) a))))))
      (a!3 (and (= 0 (len (cdr a))) (= (cdr a) nil)))
      (a!4 (exists ((c!2 Int))
             (let ((a!1 (+ (len (cdr (cdr a))) 1)))
               (and (= (len (cdr a)) a!1)
                    ((_ is (cons (Int List) List)) (cdr a))))))
      (a!5 (= 0 (len (cdr (cdr a)))))
      (a!7 (exists ((c!3 Int))
             (let ((a!1 (len (cdr (cdr (cdr a))))))
             (let ((a!2 (= (len (cdr (cdr a))) (+ a!1 1))))
               (and a!2 ((_ is (cons (Int List) List)) (cdr (cdr a))))))))
      (a!8 (and ((_ is (cons (Int List) List)) a)
                ((_ is (cons (Int List) List)) (cdr a))
                (> (car a) (car (cdr a))))))
(let ((a!6 (and a!5 (= (cdr (cdr a)) nil)))
      (a!9 (or (= a nil)
               (and ((_ is (cons (Int List) List)) a)
                    ((_ is (nil () List)) (cdr a)))
               a!8)))
  (and a!1
       (= 2 (len a))
       (increasing a)
       (member 0 a)
       (or ((_ is (nil () List)) a) ((_ is (cons (Int List) List)) a))
       a!2
       (or a!3 a!4)
       (or a!6 a!7)
       (= (increasing a) a!9)))))


Model 1
==========
a := cons(103146, cons(103145, nil)).


Model 2
==========
a := cons(133758, cons(133757, nil)).


Model 3
==========
a := cons(139611, cons(139610, nil)).


Model 4
==========
a := cons(28957, cons(28956, nil)).


Model 5
==========
a := cons(31394, cons(31393, nil)).


Model 6
==========
a := cons(40249, cons(40248, nil)).


Model 7
==========
a := cons(52046, cons(52045, nil)).


Model 8
==========
a := cons(60411, cons(60410, nil)).


Model 9
==========
a := cons(7719, cons(7718, nil)).


Model 10
==========
a := cons(92696, cons(92695, nil)).


More models may be available.  Change the max argument to see them.
