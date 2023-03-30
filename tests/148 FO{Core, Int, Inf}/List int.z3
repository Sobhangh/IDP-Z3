(declare-datatypes ((Color 0)) (((red) (blue) (green))))
(declare-datatypes ((List 0)) (((nil) (cons (car Color) (cdr List)))))
(declare-fun a () List)
(assert (and (or ((_ is (nil () List)) a) ((_ is (cons (Color List) List)) a))))


Model 1
==========
a := nil.


Model 2
==========
a := cons(red, nil).


Model 3
==========
a := cons(red, cons(red, nil)).


Model 4
==========
a := cons(red, cons(red, cons(red, nil))).


Model 5
==========
a := cons(red, cons(red, cons(red, cons(red, nil)))).


Model 6
==========
a := cons(red, cons(red, cons(red, cons(red, cons(red, nil))))).


Model 7
==========
a := cons(red, cons(red, cons(red, cons(red, cons(red, cons(red, nil)))))).


Model 8
==========
a := cons(red, cons(red, cons(red, cons(red, cons(red, cons(red, cons(red, nil))))))).


Model 9
==========
a := cons(red, cons(red, cons(red, cons(red, cons(red, cons(red, cons(red, cons(red, nil)))))))).


Model 10
==========
a := cons(red, cons(red, cons(red, cons(red, cons(red, cons(red, cons(red, cons(red, cons(red, nil))))))))).


More models may be available.  Change the max argument to see them.
