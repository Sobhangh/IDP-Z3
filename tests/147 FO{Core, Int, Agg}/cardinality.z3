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
    max2 == _max(lambda x ∈ ConfigObj : weight(x)),
    fleetTotal(f1) ==
    If(Vehicle(o1), weight(o1), 0) +
    If(Vehicle(o2), weight(o2), 0) +
    0,
    fleetTotal(f2) == 0 + 0 + If(Vehicle(o3), weight(o3), 0),
    fleetCard(f1) ==
    If(Vehicle(o1), 1, 0) + If(Vehicle(o2), 1, 0) + 0,
    fleetCard(f2) == 0 + 0 + If(Vehicle(o3), 1, 0),
    fleetMin(f1) ==
    _min(lambda x ∈ ConfigObj :  if   fleetOf(x) = f then weight(x) else 999)(f1),
    fleetMin(f2) ==
    _min(lambda x ∈ ConfigObj :  if   fleetOf(x) = f then weight(x) else 999)(f2),
    Or(_min(lambda x ∈ ConfigObj : weight(x)) == weight(o1),
       _min(lambda x ∈ ConfigObj : weight(x)) == weight(o2),
       _min(lambda x ∈ ConfigObj : weight(x)) == weight(o3)),
    _min(lambda x ∈ ConfigObj : weight(x)) <= weight(o1),
    _min(lambda x ∈ ConfigObj : weight(x)) <= weight(o2),
    _min(lambda x ∈ ConfigObj : weight(x)) <= weight(o3),
    Or(_max(lambda x ∈ ConfigObj : weight(x)) == weight(o1),
       _max(lambda x ∈ ConfigObj : weight(x)) == weight(o2),
       _max(lambda x ∈ ConfigObj : weight(x)) == weight(o3)),
    _max(lambda x ∈ ConfigObj : weight(x)) >= weight(o1),
    _max(lambda x ∈ ConfigObj : weight(x)) >= weight(o2),
    _max(lambda x ∈ ConfigObj : weight(x)) >= weight(o3),
    Or(_min(lambda x ∈ ConfigObj :  if   fleetOf(x) = f then weight(x) else 999)(f1) ==
       weight(o1),
       _min(lambda x ∈ ConfigObj :  if   fleetOf(x) = f then weight(x) else 999)(f1) ==
       weight(o2),
       999 ==
       _min(lambda x ∈ ConfigObj :  if   fleetOf(x) = f then weight(x) else 999)(f1)),
    _min(lambda x ∈ ConfigObj :  if   fleetOf(x) = f then weight(x) else 999)(f1) <=
    weight(o1),
    _min(lambda x ∈ ConfigObj :  if   fleetOf(x) = f then weight(x) else 999)(f1) <=
    weight(o2),
    999 >=
    _min(lambda x ∈ ConfigObj :  if   fleetOf(x) = f then weight(x) else 999)(f1),
    Or(999 ==
       _min(lambda x ∈ ConfigObj :  if   fleetOf(x) = f then weight(x) else 999)(f2),
       999 ==
       _min(lambda x ∈ ConfigObj :  if   fleetOf(x) = f then weight(x) else 999)(f2),
       _min(lambda x ∈ ConfigObj :  if   fleetOf(x) = f then weight(x) else 999)(f2) ==
       weight(o3)),
    999 >=
    _min(lambda x ∈ ConfigObj :  if   fleetOf(x) = f then weight(x) else 999)(f2),
    999 >=
    _min(lambda x ∈ ConfigObj :  if   fleetOf(x) = f then weight(x) else 999)(f2),
    _min(lambda x ∈ ConfigObj :  if   fleetOf(x) = f then weight(x) else 999)(f2) <=
    weight(o3))

Model 1
==========
Vehicle := {o2, o3}.
fleetOf := {o1 -> f1, o2 -> f1, o3 -> f2}.
weight := {o1 -> 3, o2 -> 4, o3 -> 5}.
total := 9.
min := 3.
max := 5.
max2 := 5.
fleetTotal := {f1 -> 4, f2 -> 5}.
fleetCard := {f1 -> 1, f2 -> 1}.
fleetMin := {f1 -> 3, f2 -> 5}.


No more models.
