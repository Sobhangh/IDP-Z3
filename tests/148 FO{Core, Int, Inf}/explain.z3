(declare-datatypes ((List1 0)) (((nil1) (cons1 (car1 Int) (cdr1 List1)))))
(declare-fun a () List1)
(define-funs-rec ( ( member ((x!1 Int) (x!2 List1)) Bool)
                   ( increasing ((x!1 List1)) Bool)
                   ( positive ((x!1 List1)) Bool)
                   ( len1 ((x!1 List1)) Int))
                 ( (or (and ((_ is (cons1 (Int List1) List1)) x!2)
                            ((_ member 0) x!1 (cdr1 x!2)))
                       (and ((_ is (cons1 (Int List1) List1)) x!2)
                            (= (car1 x!2) x!1)))
                   (let ((a!1 (and ((_ is (cons1 (Int List1) List1)) x!1)
                                   ((_ increasing 0) (cdr1 x!1))
                                   ((_ is (cons1 (Int List1) List1)) (cdr1 x!1))
                                   (< (car1 x!1) (car1 (cdr1 x!1))))))
                     (or a!1
                         (and ((_ is (cons1 (Int List1) List1)) x!1)
                              ((_ is (nil1 () List1)) (cdr1 x!1)))
                         (= x!1 nil1)))
                   (or (and ((_ is (cons1 (Int List1) List1)) x!1)
                            (< 0 (car1 x!1))
                            (> 3 (car1 x!1))
                            ((_ positive 0) (cdr1 x!1)))
                       ((_ is (nil1 () List1)) x!1))
                   (ite ((_ is (cons1 (Int List1) List1)) x!1)
                        (+ ((_ len1 0) (cdr1 x!1)) 1)
                        0)))
(assert (and (= 2 ((_ len1 0) a))
     ((_ positive 0) a)
     ((_ increasing 0) a)
     (or ((_ member 0) 1 a) ((_ member 0) 2 a))
     (or ((_ is (nil1 () List1)) a) ((_ is (cons1 (Int List1) List1)) a))
     true
     true
     true
     true))


Model 1
==========
a := cons1(1, cons1(2, nil1)).


More models may be available.  Change the max argument to see them.
