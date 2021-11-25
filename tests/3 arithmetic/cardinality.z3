And(Vehicle(o2),
    Vehicle(o3),
    2 ==
    If(Vehicle(o1), 1, 0) +
    If(Vehicle(o2), 1, 0) +
    If(Vehicle(o3), 1, 0),
    3 == weight(o1),
    4 == weight(o2),
    5 == weight(o3),
    total ==
    If(Vehicle(o1), weight(o1), 0) +
    If(Vehicle(o2), weight(o2), 0) +
    If(Vehicle(o3), weight(o3), 0),
    min == _min(lambda x ∈ ConfigObj : weight(x)),
    max == _max(lambda x ∈ ConfigObj : weight(x)),
    Exists(c!0,
           _min(lambda x ∈ ConfigObj : weight(x)) ==
           weight(c!0)),
    ForAll(c!1,
           _min(lambda x ∈ ConfigObj : weight(x)) <=
           weight(c!1)),
    Exists(c!2,
           _max(lambda x ∈ ConfigObj : weight(x)) ==
           weight(c!2)),
    ForAll(c!3,
           _max(lambda x ∈ ConfigObj : weight(x)) >=
           weight(c!3)))

Model 1
==========
Vehicle:={o1->false; o2->true; o3->true}
weight:={o1->3; o2->4; o3->5}
total:={->9}
min:={->3}
max:={->5}

No more models.
