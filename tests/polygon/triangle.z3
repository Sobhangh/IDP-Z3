
-- original ---------------------------------
vocabulary {
    
    type sides = {3..4}
    Sides: sides
    Vertices: sides


    type type constructed from {triangle, quadrilateral}
    Type : type

    type side = {1..4}
    Length(side):real
    Angle(side):real

    type subtype constructed from
        { regular_triangle
        , right_triangle
        , rectangle
        , square
        , irregular}
    Subtype : subtype

    Convex
    Equilateral
    Perimeter:real

    Large(side)
    Base : real
    Height: real
    Surface:real
}

theory {
    Subtype=regular_triangle. 

    [Definition of triangle]
    (Type=triangle      <=> Sides=3).

    [Definition of rectangle]
    (Type=quadrilateral <=> Sides=4).

    [There are as many vertices as there are sides]
    ( (Vertices=3 <=> Sides=3) &
      (Vertices=4 <=> Sides=4)).

    [All triangles are convex]
    (Sides=3 => Convex).

    [Definition of Convex]
    (Convex <=> [All angles are below 180°]
                (∀n[side]: Angle(n)<180)).

    [Definition of Equilateral]
    (Equilateral <=> [All sides have the same length]
                     (∀n[side]: Length(n)=Length(1) | Sides < n)).

    [A triangle is regular, right, or irregular]
    ( Subtype=right_triangle | Subtype=regular_triangle | Subtype=irregular <= Sides=3).


    [A regular triangle is an equilateral triangle]
    (Subtype=regular_triangle <=> Sides=3 & Equilateral).

    [A regular triangle is a triangle where all angles are 60°]
    (Subtype=regular_triangle <=> Sides=3 & [All angles are 60°]
                                            (!n[side]: Angle(n)=60 | Sides < n)).

    [A right triangle is a triangle with a 90° angle]
    (Subtype=right_triangle   <=> Sides=3 & [One angle is 90°]
                                           (?n[side]: Angle(n)=90)).

    [All angles are 90° in squares and rectangles]
    (Subtype=square | Subtype=rectangle <=> Sides=4 & [All angles are 90°]
                                                     (!n[side]: Angle(n)=90 | Sides < n)).

    [In a rectangle, opposite side have the same length, and adjacent sides have different lengths]
    (Subtype=rectangle => Length(1)=Length(3) & Length(2)=Length(4) & Length(1)~=Length(2)).

    [A square is an equilateral quadrilateral]
    (Subtype=square    <=> Sides=4 & Equilateral).

    [In a triangle, no side is longer than the sum of the 2 other sides]
    ( Type=triangle => ( Length(1) =< Length(2) + Length(3))
                    &  ( Length(2) =< Length(3) + Length(1))
                    &  ( Length(3) =< Length(1) + Length(2))).

    // General constraints

    [The perimeter is the sum of the lengths of the sides]
    (Perimeter = sum{n[side] : true : Length(n)}).

    [The sum of the angles is 180° for a triangle, and 360° for a quadrilateral]
    (sum{n[side] : true : Angle(n)} = (Sides-2)*180).

    [Lengths are positive numbers]
    (!x[side]: 0 =< Length(x)).

    [Angles are positive numbers]
    (!x[side]: 0 =< Angle(x)).

    [Angles cannot be 180°]
    (!x[side]: Angle(x) ~= 180).

    [A polygon with N vertices has N angles]
    (!n[side]: Angle(n)=0 <=> Vertices<n ).

    [A polygon with N sides has N lengths]
    (!n[side]: Length(n)=0 <=> Sides<n).



    // TODO : surface
    Type=triangle => Surface = (Base * Height)/2.
    Subtype=square | Subtype=rectangle => Surface = Length(1)*Length(2).
    Subtype=irregular & Sides = 4 => Surface = -1.
    0 =< Base.
    0 =< Height.
    ?n[side]: n=<Sides & Length(n)=Base.
}

view expanded
-- vocabulary -------------------------------

-- theory -----------------------------------
Subtype == regular_triangle

(Type == triangle) == (Sides == 3)

(Type == quadrilateral) == (Sides == 4)

And((Vertices == 3) == (Sides == 3),
    (Vertices == 4) == (Sides == 4))

Or(Not(Sides == 3), Convex)

Convex ==
And(Angle(1) < 180,
    Angle(2) < 180,
    Angle(3) < 180,
    Angle(4) < 180)

Equilateral ==
And(Or(Length(1) == Length(1), Sides < 1),
    Or(Length(2) == Length(1), Sides < 2),
    Or(Length(3) == Length(1), Sides < 3),
    Or(Length(4) == Length(1), Sides < 4))

Or(Not(Sides == 3),
   Or(Subtype == right_triangle,
      Subtype == regular_triangle,
      Subtype == irregular))

(Subtype == regular_triangle) ==
And(Sides == 3, Equilateral)

(Subtype == regular_triangle) ==
And(Sides == 3,
    And(Or(Angle(1) == 60, Sides < 1),
        Or(Angle(2) == 60, Sides < 2),
        Or(Angle(3) == 60, Sides < 3),
        Or(Angle(4) == 60, Sides < 4)))

(Subtype == right_triangle) ==
And(Sides == 3,
    Or(Angle(1) == 90,
       Angle(2) == 90,
       Angle(3) == 90,
       Angle(4) == 90))

Or(Subtype == square, Subtype == rectangle) ==
And(Sides == 4,
    And(Or(Angle(1) == 90, Sides < 1),
        Or(Angle(2) == 90, Sides < 2),
        Or(Angle(3) == 90, Sides < 3),
        Or(Angle(4) == 90, Sides < 4)))

Or(Not(Subtype == rectangle),
   And(Length(1) == Length(3),
       Length(2) == Length(4),
       Not(Length(1) == Length(2))))

(Subtype == square) == And(Sides == 4, Equilateral)

Or(Not(Type == triangle),
   And(Length(1) <= Length(2) + Length(3),
       Length(2) <= Length(3) + Length(1),
       Length(3) <= Length(1) + Length(2)))

Perimeter == Length(1) + Length(2) + Length(3) + Length(4)

Angle(1) + Angle(2) + Angle(3) + Angle(4) ==
ToReal(180*(-2 + Sides))

And(Length(1) >= 0,
    Length(2) >= 0,
    Length(3) >= 0,
    Length(4) >= 0)

And(Angle(1) >= 0,
    Angle(2) >= 0,
    Angle(3) >= 0,
    Angle(4) >= 0)

And(Not(Angle(1) == 180),
    Not(Angle(2) == 180),
    Not(Angle(3) == 180),
    Not(Angle(4) == 180))

And((Angle(1) == 0) == (Vertices < 1),
    (Angle(2) == 0) == (Vertices < 2),
    (Angle(3) == 0) == (Vertices < 3),
    (Angle(4) == 0) == (Vertices < 4))

And((Length(1) == 0) == (Sides < 1),
    (Length(2) == 0) == (Sides < 2),
    (Length(3) == 0) == (Sides < 3),
    (Length(4) == 0) == (Sides < 4))

Or(Not(Type == triangle), Surface == 1/2*Base*Height)

Or(Not(Or(Subtype == square, Subtype == rectangle)),
   Surface == Length(1)*Length(2))

Or(Not(And(Subtype == irregular, Sides == 4)),
   Surface == -1)

Base >= 0

Height >= 0

Or(And(Sides >= 1, Length(1) == Base),
   And(Sides >= 2, Length(2) == Base),
   And(Sides >= 3, Length(3) == Base),
   And(Sides >= 4, Length(4) == Base))

And(Sides >= 3, Sides <= 4)

And(Vertices >= 3, Vertices <= 4)

-- subtences ------------------------------------
Subtype = regular_triangle
Type = triangle
Sides = 3
Type = quadrilateral
Sides = 4
Vertices = 3
Vertices = 4
Convex
∀n[side] : Angle(n) < 180
Equilateral
∀n[side] : (Length(n) = Length(1)) ∨ (Sides < n)
Subtype = right_triangle
Subtype = irregular
∀n[side] : (Angle(n) = 60) ∨ (Sides < n)
∃n[side] : Angle(n) = 90
Subtype = square
Subtype = rectangle
∀n[side] : (Angle(n) = 90) ∨ (Sides < n)
Length(1) = Length(3)
Length(2) = Length(4)
Length(1) = Length(2)
Length(1) ≤ (Length(2) + Length(3))
Length(2) ≤ (Length(3) + Length(1))
Length(3) ≤ (Length(1) + Length(2))
Perimeter = (sum{n[side] : true : Length(n)})
(sum{n[side] : true : Angle(n)}) = ((Sides - 2) * 180)
∀x[side] : 0 ≤ Length(x)
∀x[side] : 0 ≤ Angle(x)
∀x[side] : Angle(x) ≠ 180
∀n[side] : (Angle(n) = 0) ⇔ (Vertices < n)
∀n[side] : (Length(n) = 0) ⇔ (Sides < n)
Surface = ((Base * Height) / 2)
Surface = (Length(1) * Length(2))
Surface = -1
0 ≤ Base
0 ≤ Height
∃n[side] : (n ≤ Sides) ∧ (Length(n) = Base)
3 ≤ Sides ≤ 4
3 ≤ Vertices ≤ 4

-- GUILines ------------------------------------
Sides
Vertices
Type
Length(1)
Length(2)
Length(3)
Length(4)
Angle(1)
Angle(2)
Angle(3)
Angle(4)
Subtype
Convex
Equilateral
Perimeter
Large(1)
Large(2)
Large(3)
Large(4)
Base
Height
Surface
Subtype = regular_triangle
Type = triangle
Sides = 3
Type = quadrilateral
Sides = 4
Vertices = 3
Vertices = 4
∀n[side] : Angle(n) < 180
∀n[side] : (Length(n) = Length(1)) ∨ (Sides < n)
Subtype = right_triangle
Subtype = irregular
∀n[side] : (Angle(n) = 60) ∨ (Sides < n)
∃n[side] : Angle(n) = 90
Subtype = square
Subtype = rectangle
∀n[side] : (Angle(n) = 90) ∨ (Sides < n)
Length(1) = Length(3)
Length(2) = Length(4)
Length(1) = Length(2)
Length(1) ≤ (Length(2) + Length(3))
Length(2) ≤ (Length(3) + Length(1))
Length(3) ≤ (Length(1) + Length(2))
Perimeter = (sum{n[side] : true : Length(n)})
(sum{n[side] : true : Angle(n)}) = ((Sides - 2) * 180)
∀x[side] : 0 ≤ Length(x)
∀x[side] : 0 ≤ Angle(x)
∀x[side] : Angle(x) ≠ 180
∀n[side] : (Angle(n) = 0) ⇔ (Vertices < n)
∀n[side] : (Length(n) = 0) ⇔ (Sides < n)
Surface = ((Base * Height) / 2)
Surface = (Length(1) * Length(2))
Surface = -1
0 ≤ Base
0 ≤ Height
∃n[side] : (n ≤ Sides) ∧ (Length(n) = Base)
3 ≤ Sides ≤ 4
3 ≤ Vertices ≤ 4

-- case -------------------------------------
Type:        
  
Definitions: 
  
Universals:  
  Subtype = regular_triangle
  Perimeter = (sum{n[side] : true : Length(n)})
  (sum{n[side] : true : Angle(n)}) = ((Sides - 2) * 180)
  ∀x[side] : 0 ≤ Length(x)
  ∀x[side] : 0 ≤ Angle(x)
  ∀x[side] : Angle(x) ≠ 180
  ∀n[side] : (Angle(n) = 0) ⇔ (Vertices < n)
  ∀n[side] : (Length(n) = 0) ⇔ (Sides < n)
  0 ≤ Base
  0 ≤ Height
  ∃n[side] : (n ≤ Sides) ∧ (Length(n) = Base)
  3 ≤ Sides ≤ 4
  3 ≤ Vertices ≤ 4
  Subtype = regular_triangle
Consequences:
  Type = triangle <= {'((Type = triangle) ⇔ (Sides = 3))', 'Sides', 'Sides = 3'}
  Sides = 3 <= {'((Subtype = regular_triangle) ⇔ ((Sides = 3) ∧ Equilateral))', 'Subtype', 'Subtype = regular_triangle'}
  ~Type = quadrilateral <= {'((Type = quadrilateral) ⇔ (Sides = 4))', 'Sides', 'Sides = 4'}
  ~Sides = 4 <= {'Sides'}
  Vertices = 3 <= {'(((Vertices = 3) ⇔ (Sides = 3)) ∧ ((Vertices = 4) ⇔ (Sides = 4)))', 'Sides', 'Sides = 3'}
  ~Vertices = 4 <= {'(((Vertices = 3) ⇔ (Sides = 3)) ∧ ((Vertices = 4) ⇔ (Sides = 4)))', 'Sides', 'Sides = 4'}
  Convex <= {'((Sides = 3) ⇒ Convex)', 'Sides', 'Sides = 3'}
  ∀n[side] : Angle(n) < 180 <= {'(Convex ⇔ (∀n[side] : Angle(n) < 180))', 'Convex'}
  Equilateral <= {'((Subtype = regular_triangle) ⇔ ((Sides = 3) ∧ Equilateral))', 'Subtype', 'Subtype = regular_triangle'}
  ∀n[side] : (Length(n) = Length(1)) ∨ (Sides < n) <= {'(Equilateral ⇔ (∀n[side] : (Length(n) = Length(1)) ∨ (Sides < n)))', 'Equilateral', 'n = 4', 'Sides'}
  ~Subtype = right_triangle <= {'Subtype'}
  ~Subtype = irregular <= {'Subtype'}
  ∀n[side] : (Angle(n) = 60) ∨ (Sides < n) <= {'((Subtype = regular_triangle) ⇔ ((Sides = 3) ∧ (∀n[side] : (Angle(n) = 60) ∨ (Sides < n))))', 'Subtype', 'Subtype = regular_triangle'}
  ~∃n[side] : Angle(n) = 90 <= {'((Subtype = right_triangle) ⇔ ((Sides = 3) ∧ (∃n[side] : Angle(n) = 90)))', 'Subtype', 'Subtype = right_triangle'}
  ~Subtype = square <= {'Subtype'}
  ~Subtype = rectangle <= {'Subtype'}
  ~∀n[side] : (Angle(n) = 90) ∨ (Sides < n) <= Z3 proof
  Length(1) = Length(3) <= Z3 proof
  ~Length(2) = Length(4) <= Z3 proof
  Length(1) = Length(2) <= Z3 proof
  Length(1) ≤ (Length(2) + Length(3)) <= {'((Type = triangle) ⇒ ((Length(1) ≤ (Length(2) + Length(3))) ∧ (Length(2) ≤ (Length(3) + Length(1))) ∧ (Length(3) ≤ (Length(1) + Length(2)))))', 'Type', 'Type = triangle'}
  Length(2) ≤ (Length(3) + Length(1)) <= {'((Type = triangle) ⇒ ((Length(1) ≤ (Length(2) + Length(3))) ∧ (Length(2) ≤ (Length(3) + Length(1))) ∧ (Length(3) ≤ (Length(1) + Length(2)))))', 'Type', 'Type = triangle'}
  Length(3) ≤ (Length(1) + Length(2)) <= {'((Type = triangle) ⇒ ((Length(1) ≤ (Length(2) + Length(3))) ∧ (Length(2) ≤ (Length(3) + Length(1))) ∧ (Length(3) ≤ (Length(1) + Length(2)))))', 'Type', 'Type = triangle'}
  Surface = ((Base * Height) / 2) <= {'(Type = triangle) ⇒ (Surface = ((Base * Height) / 2))', 'Type', 'Type = triangle'}
  ~Surface = -1 <= Z3 proof
  Sides = 3 <= {'((Subtype = regular_triangle) ⇔ ((Sides = 3) ∧ Equilateral))', 'Subtype', 'Subtype = regular_triangle'}
  Vertices = 3 <= {'(((Vertices = 3) ⇔ (Sides = 3)) ∧ ((Vertices = 4) ⇔ (Sides = 4)))', 'Sides', 'Sides = 3'}
  Type = triangle <= {'((Type = triangle) ⇔ (Sides = 3))', 'Sides', 'Sides = 3'}
  Length(4) = 0 <= Z3 proof
  Angle(1) = 60 <= Z3 proof
  Angle(2) = 60 <= Z3 proof
  Angle(3) = 60 <= Z3 proof
  Angle(4) = 0 <= Z3 proof
Simplified:  
  
Irrelevant:  
  ~Sides = 4 <= {'Sides'}
  ~Subtype = right_triangle <= {'Subtype'}
  ~Subtype = irregular <= {'Subtype'}
  ~Subtype = square <= {'Subtype'}
  ~Subtype = rectangle <= {'Subtype'}
  ~∀n[side] : (Angle(n) = 90) ∨ (Sides < n) <= Z3 proof
  Length(1) = Length(3) <= Z3 proof
  ~Length(2) = Length(4) <= Z3 proof
  Length(1) = Length(2) <= Z3 proof
  ~Surface = (Length(1) * Length(2))
  ~Surface = -1 <= Z3 proof
  3 ≤ Sides ≤ 4
  3 ≤ Vertices ≤ 4


-- meta -------------------------------------
{'symbols': [{'idpname': 'Sides', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'},
             {'idpname': 'Vertices', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'},
             {'idpname': 'Type', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'},
             {'idpname': 'Length', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'},
             {'idpname': 'Angle', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'},
             {'idpname': 'Subtype', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'},
             {'idpname': 'Convex', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'expanded'},
             {'idpname': 'Equilateral',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'expanded'},
             {'idpname': 'Perimeter', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'},
             {'idpname': 'Base', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'},
             {'idpname': 'Height', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'},
             {'idpname': 'Surface', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'Angle': {'(sum{n[side] : true : Angle(n)}) = ((Sides - 2) * 180)': {'environmental': False,
                                                                      'normal': False,
                                                                      'reading': 'The sum of the angles is 180° for a '
                                                                                 'triangle, and 360° for a '
                                                                                 'quadrilateral',
                                                                      'relevant': True,
                                                                      'status': 'UNIVERSAL',
                                                                      'typ': 'Bool',
                                                                      'value': True},
           'Angle(1)': {'environmental': False,
                        'normal': True,
                        'reading': 'Angle(1)',
                        'relevant': True,
                        'status': 'CONSEQUENCE',
                        'typ': 'Real',
                        'value': '60'},
           'Angle(2)': {'environmental': False,
                        'normal': True,
                        'reading': 'Angle(2)',
                        'relevant': True,
                        'status': 'CONSEQUENCE',
                        'typ': 'Real',
                        'value': '60'},
           'Angle(3)': {'environmental': False,
                        'normal': True,
                        'reading': 'Angle(3)',
                        'relevant': True,
                        'status': 'CONSEQUENCE',
                        'typ': 'Real',
                        'value': '60'},
           'Angle(4)': {'environmental': False,
                        'normal': True,
                        'reading': 'Angle(4)',
                        'relevant': True,
                        'status': 'CONSEQUENCE',
                        'typ': 'Real',
                        'value': '0'},
           '∀n[side] : (Angle(n) = 0) ⇔ (Vertices < n)': {'environmental': False,
                                                          'normal': False,
                                                          'reading': 'A polygon with N vertices has N angles',
                                                          'relevant': True,
                                                          'status': 'UNIVERSAL',
                                                          'typ': 'Bool',
                                                          'value': True},
           '∀n[side] : (Angle(n) = 60) ∨ (Sides < n)': {'environmental': False,
                                                        'normal': False,
                                                        'reading': 'All angles are 60°',
                                                        'relevant': True,
                                                        'status': 'CONSEQUENCE',
                                                        'typ': 'Bool',
                                                        'value': True},
           '∀n[side] : (Angle(n) = 90) ∨ (Sides < n)': {'environmental': False,
                                                        'normal': False,
                                                        'reading': 'All angles are 90°',
                                                        'relevant': False,
                                                        'status': 'CONSEQUENCE',
                                                        'typ': 'Bool',
                                                        'value': False},
           '∀n[side] : Angle(n) < 180': {'environmental': False,
                                         'normal': False,
                                         'reading': 'All angles are below 180°',
                                         'relevant': True,
                                         'status': 'CONSEQUENCE',
                                         'typ': 'Bool',
                                         'value': True},
           '∀x[side] : 0 ≤ Angle(x)': {'environmental': False,
                                       'normal': False,
                                       'reading': 'Angles are positive numbers',
                                       'relevant': True,
                                       'status': 'UNIVERSAL',
                                       'typ': 'Bool',
                                       'value': True},
           '∀x[side] : Angle(x) ≠ 180': {'environmental': False,
                                         'normal': False,
                                         'reading': 'Angles cannot be 180°',
                                         'relevant': True,
                                         'status': 'UNIVERSAL',
                                         'typ': 'Bool',
                                         'value': True},
           '∃n[side] : Angle(n) = 90': {'environmental': False,
                                        'normal': False,
                                        'reading': 'One angle is 90°',
                                        'relevant': True,
                                        'status': 'CONSEQUENCE',
                                        'typ': 'Bool',
                                        'value': False}},
 'Base': {'0 ≤ Base': {'environmental': False,
                       'normal': False,
                       'reading': '0 ≤ Base',
                       'relevant': True,
                       'status': 'UNIVERSAL',
                       'typ': 'Bool',
                       'value': True},
          'Base': {'environmental': False,
                   'normal': True,
                   'reading': 'Base',
                   'relevant': True,
                   'status': 'UNKNOWN',
                   'typ': 'Real',
                   'value': ''}},
 'Convex': {'Convex': {'environmental': False,
                       'normal': True,
                       'reading': 'Convex',
                       'relevant': True,
                       'status': 'CONSEQUENCE',
                       'typ': 'Bool',
                       'value': True}},
 'Equilateral': {'Equilateral': {'environmental': False,
                                 'normal': True,
                                 'reading': 'Equilateral',
                                 'relevant': True,
                                 'status': 'CONSEQUENCE',
                                 'typ': 'Bool',
                                 'value': True}},
 'Height': {'0 ≤ Height': {'environmental': False,
                           'normal': False,
                           'reading': '0 ≤ Height',
                           'relevant': True,
                           'status': 'UNIVERSAL',
                           'typ': 'Bool',
                           'value': True},
            'Height': {'environmental': False,
                       'normal': True,
                       'reading': 'Height',
                       'relevant': True,
                       'status': 'UNKNOWN',
                       'typ': 'Real',
                       'value': ''}},
 'Large': {'Large(1)': {'environmental': False,
                        'normal': True,
                        'reading': 'Large(1)',
                        'relevant': False,
                        'status': 'UNKNOWN',
                        'typ': 'Bool'},
           'Large(2)': {'environmental': False,
                        'normal': True,
                        'reading': 'Large(2)',
                        'relevant': False,
                        'status': 'UNKNOWN',
                        'typ': 'Bool'},
           'Large(3)': {'environmental': False,
                        'normal': True,
                        'reading': 'Large(3)',
                        'relevant': False,
                        'status': 'UNKNOWN',
                        'typ': 'Bool'},
           'Large(4)': {'environmental': False,
                        'normal': True,
                        'reading': 'Large(4)',
                        'relevant': False,
                        'status': 'UNKNOWN',
                        'typ': 'Bool'}},
 'Length': {'Length(1)': {'environmental': False,
                          'normal': True,
                          'reading': 'Length(1)',
                          'relevant': True,
                          'status': 'UNKNOWN',
                          'typ': 'Real',
                          'value': ''},
            'Length(1) = Length(2)': {'environmental': False,
                                      'normal': False,
                                      'reading': 'Length(1) = Length(2)',
                                      'relevant': False,
                                      'status': 'CONSEQUENCE',
                                      'typ': 'Bool',
                                      'value': True},
            'Length(1) = Length(3)': {'environmental': False,
                                      'normal': False,
                                      'reading': 'Length(1) = Length(3)',
                                      'relevant': False,
                                      'status': 'CONSEQUENCE',
                                      'typ': 'Bool',
                                      'value': True},
            'Length(1) ≤ (Length(2) + Length(3))': {'environmental': False,
                                                    'normal': False,
                                                    'reading': 'Length(1) ≤ (Length(2) + Length(3))',
                                                    'relevant': True,
                                                    'status': 'CONSEQUENCE',
                                                    'typ': 'Bool',
                                                    'value': True},
            'Length(2)': {'environmental': False,
                          'normal': True,
                          'reading': 'Length(2)',
                          'relevant': True,
                          'status': 'UNKNOWN',
                          'typ': 'Real',
                          'value': ''},
            'Length(2) = Length(4)': {'environmental': False,
                                      'normal': False,
                                      'reading': 'Length(2) = Length(4)',
                                      'relevant': False,
                                      'status': 'CONSEQUENCE',
                                      'typ': 'Bool',
                                      'value': False},
            'Length(2) ≤ (Length(3) + Length(1))': {'environmental': False,
                                                    'normal': False,
                                                    'reading': 'Length(2) ≤ (Length(3) + Length(1))',
                                                    'relevant': True,
                                                    'status': 'CONSEQUENCE',
                                                    'typ': 'Bool',
                                                    'value': True},
            'Length(3)': {'environmental': False,
                          'normal': True,
                          'reading': 'Length(3)',
                          'relevant': True,
                          'status': 'UNKNOWN',
                          'typ': 'Real',
                          'value': ''},
            'Length(3) ≤ (Length(1) + Length(2))': {'environmental': False,
                                                    'normal': False,
                                                    'reading': 'Length(3) ≤ (Length(1) + Length(2))',
                                                    'relevant': True,
                                                    'status': 'CONSEQUENCE',
                                                    'typ': 'Bool',
                                                    'value': True},
            'Length(4)': {'environmental': False,
                          'normal': True,
                          'reading': 'Length(4)',
                          'relevant': True,
                          'status': 'CONSEQUENCE',
                          'typ': 'Real',
                          'value': '0'},
            '∀n[side] : (Length(n) = 0) ⇔ (Sides < n)': {'environmental': False,
                                                         'normal': False,
                                                         'reading': 'A polygon with N sides has N lengths',
                                                         'relevant': True,
                                                         'status': 'UNIVERSAL',
                                                         'typ': 'Bool',
                                                         'value': True},
            '∀n[side] : (Length(n) = Length(1)) ∨ (Sides < n)': {'environmental': False,
                                                                 'normal': False,
                                                                 'reading': 'All sides have the same length',
                                                                 'relevant': True,
                                                                 'status': 'CONSEQUENCE',
                                                                 'typ': 'Bool',
                                                                 'value': True},
            '∀x[side] : 0 ≤ Length(x)': {'environmental': False,
                                         'normal': False,
                                         'reading': 'Lengths are positive numbers',
                                         'relevant': True,
                                         'status': 'UNIVERSAL',
                                         'typ': 'Bool',
                                         'value': True}},
 'Perimeter': {'Perimeter': {'environmental': False,
                             'normal': True,
                             'reading': 'Perimeter',
                             'relevant': True,
                             'status': 'UNKNOWN',
                             'typ': 'Real',
                             'value': ''},
               'Perimeter = (sum{n[side] : true : Length(n)})': {'environmental': False,
                                                                 'normal': False,
                                                                 'reading': 'The perimeter is the sum of the lengths '
                                                                            'of the sides',
                                                                 'relevant': True,
                                                                 'status': 'UNIVERSAL',
                                                                 'typ': 'Bool',
                                                                 'value': True}},
 'Sides': {'Sides': {'environmental': False,
                     'normal': True,
                     'reading': 'Sides',
                     'relevant': True,
                     'status': 'CONSEQUENCE',
                     'typ': 'Int',
                     'value': '',
                     'values': ['3', '4']},
           'Sides = 3': {'environmental': False,
                         'normal': False,
                         'reading': 'Sides = 3',
                         'relevant': True,
                         'status': 'CONSEQUENCE',
                         'typ': 'Bool',
                         'value': True},
           'Sides = 4': {'environmental': False,
                         'normal': False,
                         'reading': 'Sides = 4',
                         'relevant': False,
                         'status': 'CONSEQUENCE',
                         'typ': 'Bool',
                         'value': False},
           '∃n[side] : (n ≤ Sides) ∧ (Length(n) = Base)': {'environmental': False,
                                                           'normal': False,
                                                           'reading': '∃n[side] : (n ≤ Sides) ∧ (Length(n) = Base)',
                                                           'relevant': True,
                                                           'status': 'UNIVERSAL',
                                                           'typ': 'Bool',
                                                           'value': True}},
 'Subtype': {'Subtype': {'environmental': False,
                         'normal': True,
                         'reading': 'Subtype',
                         'relevant': True,
                         'status': 'UNIVERSAL',
                         'typ': 'subtype',
                         'value': '',
                         'values': ['regular_triangle', 'right_triangle', 'rectangle', 'square', 'irregular']},
             'Subtype = irregular': {'environmental': False,
                                     'normal': False,
                                     'reading': 'Subtype = irregular',
                                     'relevant': False,
                                     'status': 'CONSEQUENCE',
                                     'typ': 'Bool',
                                     'value': False},
             'Subtype = rectangle': {'environmental': False,
                                     'normal': False,
                                     'reading': 'Subtype = rectangle',
                                     'relevant': False,
                                     'status': 'CONSEQUENCE',
                                     'typ': 'Bool',
                                     'value': False},
             'Subtype = regular_triangle': {'environmental': False,
                                            'normal': False,
                                            'reading': 'Subtype = regular_triangle',
                                            'relevant': True,
                                            'status': 'UNIVERSAL',
                                            'typ': 'Bool',
                                            'value': True},
             'Subtype = right_triangle': {'environmental': False,
                                          'normal': False,
                                          'reading': 'Subtype = right_triangle',
                                          'relevant': False,
                                          'status': 'CONSEQUENCE',
                                          'typ': 'Bool',
                                          'value': False},
             'Subtype = square': {'environmental': False,
                                  'normal': False,
                                  'reading': 'Subtype = square',
                                  'relevant': False,
                                  'status': 'CONSEQUENCE',
                                  'typ': 'Bool',
                                  'value': False}},
 'Surface': {'Surface': {'environmental': False,
                         'normal': True,
                         'reading': 'Surface',
                         'relevant': True,
                         'status': 'UNKNOWN',
                         'typ': 'Real',
                         'value': ''},
             'Surface = ((Base * Height) / 2)': {'environmental': False,
                                                 'normal': False,
                                                 'reading': 'Surface = ((Base * Height) / 2)',
                                                 'relevant': True,
                                                 'status': 'CONSEQUENCE',
                                                 'typ': 'Bool',
                                                 'value': True},
             'Surface = (Length(1) * Length(2))': {'environmental': False,
                                                   'normal': False,
                                                   'reading': 'Surface = (Length(1) * Length(2))',
                                                   'relevant': False,
                                                   'status': 'UNKNOWN',
                                                   'typ': 'Bool'},
             'Surface = -1': {'environmental': False,
                              'normal': False,
                              'reading': 'Surface = -1',
                              'relevant': False,
                              'status': 'CONSEQUENCE',
                              'typ': 'Bool',
                              'value': False}},
 'Type': {'Type': {'environmental': False,
                   'normal': True,
                   'reading': 'Type',
                   'relevant': True,
                   'status': 'CONSEQUENCE',
                   'typ': 'type',
                   'value': '',
                   'values': ['triangle', 'quadrilateral']},
          'Type = quadrilateral': {'environmental': False,
                                   'normal': False,
                                   'reading': 'Type = quadrilateral',
                                   'relevant': True,
                                   'status': 'CONSEQUENCE',
                                   'typ': 'Bool',
                                   'value': False},
          'Type = triangle': {'environmental': False,
                              'normal': False,
                              'reading': 'Type = triangle',
                              'relevant': True,
                              'status': 'CONSEQUENCE',
                              'typ': 'Bool',
                              'value': True}},
 'Vertices': {'Vertices': {'environmental': False,
                           'normal': True,
                           'reading': 'Vertices',
                           'relevant': True,
                           'status': 'CONSEQUENCE',
                           'typ': 'Int',
                           'value': '',
                           'values': ['3', '4']},
              'Vertices = 3': {'environmental': False,
                               'normal': False,
                               'reading': 'Vertices = 3',
                               'relevant': True,
                               'status': 'CONSEQUENCE',
                               'typ': 'Bool',
                               'value': True},
              'Vertices = 4': {'environmental': False,
                               'normal': False,
                               'reading': 'Vertices = 4',
                               'relevant': True,
                               'status': 'CONSEQUENCE',
                               'typ': 'Bool',
                               'value': False}}}
