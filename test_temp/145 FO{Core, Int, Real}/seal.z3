And((cSID == b) == And(263/125 <= Depth, 619/250 >= Depth),
    (cSID == c) == And(346/125 <= Depth, 3391/1000 >= Depth),
    (cSID == d) == And(2147/500 <= Depth, 2603/500 >= Depth),
    (cSID == e) == And(2737/500 <= Depth, 3343/500 >= Depth),
    (cSID == f) == And(1039/125 <= Depth, 2687/250 >= Depth),
    Or(cSID == b,
       cSID == c,
       cSID == d,
       cSID == e,
       cSID == f))
sat
