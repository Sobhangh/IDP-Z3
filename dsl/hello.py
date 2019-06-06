

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
print(parentdir)
import configcase
from DSLClasses import *

model: File = idpparser.model_from_str("""
vocabulary {
    type name constructed from {triangle, quadrilateral}
    type subname constructed from
        { triangle_equilateral
        , right_triangle
        , rectangle
        , square
        , irregular}
    Name : name
    Subname : subname

    type sides = {3..4}
    Vertices: sides
    Sides: sides

    type side = {1..4}
    Length(side):real
    Angle(side):real
    Perimeter:real
    Base : real
    Height: real
    Surface:real

    Convex
    Equilateral
}

theory {
    Vertices=3 <=> Sides=3.
    Vertices=4 <=> Sides=4.
    Name=triangle      <=> Sides=3.
    Name=quadrilateral <=> Sides=4.

    // General rules
    Sides=3 => Convex.
    (!n[side]: n=<Sides => Angle(n)<180) <=> Convex.
    (!n[side]: n=<Sides => Length(n)=Length(1)) <=> Equilateral.


    Perimeter = sum{n[side] : n=<Sides : Length(n)}.
    sum{n[side] : n=<Sides : Angle(n)} = (Sides-2)*180.

    // triangle
    Subname=triangle_equilateral <=> Sides=3 & Equilateral.
    Subname=triangle_equilateral <=> Sides=3 & (!n[side]: n=<Sides => Angle(n)=60).
    Subname=right_triangle <=> Sides=3 & (?n[side]: n=<Sides => Angle(n)=90).

    // quadrilateral
    Subname=square | Subname=rectangle <=> Sides=4 & (!n[side]: n=<Sides => Angle(n)=90).
    Subname=rectangle => Length(1)=Length(3) & Length(2)=Length(4) & Length(1)~=Length(2).
    Subname=square => Sides=4 & Equilateral.

    // surface : not linear --> not supported by Z3!
    0 =< Base.
    0 =< Height.
     Name=triangle => Surface = (Base * Height)/2.
    Subname=square | Subname=rectangle => Surface = Length(1)*Length(2).

    // feasibility
    Name=triangle => Length(1) =< Length(2) + Length(3).
    Name=triangle => Length(2) =< Length(3) + Length(1).
    Name=triangle => Length(3) =< Length(1) + Length(2).

    // positive values
    0 < Vertices.
    0 < Sides.
    !x[side]: 0 =< Length(x).
    !x[side]: 0 =< Angle(x).
}
""")
for i in range(1):
    c = ConfigCase(model.translate)
    c.assumptions = [c.atoms["Subname = square"]]
    out = c.propagation()
    print(out["Surface"]['[\"Surface = Length(1) * Length(2)\"]']["ct"]) # expected True

# solver = c.mk_solver()
# print(solver)
# print(solver.check())
# print(solver.model())

# print(c.relevantVals)