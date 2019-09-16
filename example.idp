
  vocabulary {
      Radial
      InnerDiameter : real
      OuterDiameter : real
      Length : real
      Depth : real
      type spring constructed from {b,c,d,e,f}
      cSID : spring
  }

  theory {
       // InnerDiameter = 68.8.
       0<InnerDiameter.
       OuterDiameter = 75 .
       Length = 8.87 .

       Radial => Depth = (OuterDiameter-InnerDiameter) * 0.5.
       ~Radial => Depth = Length.

       cSID=b <=> (2.104 =< Depth & Depth =< 2.476).
       cSID=c <=> (2.768 =< Depth & Depth =< 3.391).
       cSID=d <=> (4.294 =< Depth & Depth =< 5.206).
       cSID=e <=> (5.474 =< Depth & Depth =< 6.686).
       cSID=f <=> (8.312 =< Depth & Depth =< 10.748).
  }
