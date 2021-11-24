And(Vehicle(o1),
    1 == If(Vehicle(o1), 1, 0) + If(Vehicle(o2), 1, 0),
    3 == weight(o1),
    4 == weight(o2),
    total ==
    If(Vehicle(o1), weight(o1), 0) +
    If(Vehicle(o2), weight(o2), 0),
    min == weight(o1) + weight(o2))

Model 1
==========
Vehicle:={o1->true; o2->false}
weight:={o1->3; o2->4}
total:={->3}
min:={->7}

No more models.
