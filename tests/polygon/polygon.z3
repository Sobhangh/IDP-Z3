
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
    // Base : real
    // Height: real
    // Surface:real
}

theory {
    { !n[side]: Large(n) <- 10 < Length(n).}
    !n[side]: Length(n) < Length(n+1).
    ~Large(1) | Large(1).

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
    //Type=triangle => Surface = (Base * Height)/2.
    //Subtype=square | Subtype=rectangle => Surface = Length(1)*Length(2).
    //Subtype=irregular & Sides = 4 => Surface = -1.
    //0 =< Base.
    //0 =< Height.
    //?n[side]: n=<Sides & Length(n)=Base.
}
structure {
    Length = {1,1; 2,2; 3,3; 4,4} else 5
}

view expanded
-- vocabulary -------------------------------

-- theory -----------------------------------
True

Or(Not(Large(1)), Large(1))

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

Equilateral == And(Sides < 2, Sides < 3, Sides < 4)

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

Not(Subtype == rectangle)

(Subtype == square) == And(Sides == 4, Equilateral)

True

Perimeter == 10

Angle(1) + Angle(2) + Angle(3) + Angle(4) ==
ToReal(180*(-2 + Sides))

True

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

And(Not(Sides < 1),
    Not(Sides < 2),
    Not(Sides < 3),
    Not(Sides < 4))

And(Not(Large(1)),
    Not(Large(2)),
    Not(Large(3)),
    Not(Large(4)))

-- atoms ------------------------------------
Sides
Vertices
Type
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
Type = triangle
Sides = 3
Type = quadrilateral
Sides = 4
Vertices = 3
Vertices = 4
∀n[side] : Angle(n) < 180
∀n[side] : (Length(n) = Length(1)) ∨ (Sides < n)
Subtype = right_triangle
Subtype = regular_triangle
Subtype = irregular
∀n[side] : (Angle(n) = 60) ∨ (Sides < n)
∃n[side] : Angle(n) = 90
Subtype = square
Subtype = rectangle
∀n[side] : (Angle(n) = 90) ∨ (Sides < n)
Perimeter = (sum{n[side] : true : Length(n)})
(sum{n[side] : true : Angle(n)}) = ((Sides - 2) * 180)
∀x[side] : 0 ≤ Angle(x)
∀x[side] : Angle(x) ≠ 180
∀n[side] : (Angle(n) = 0) ⇔ (Vertices < n)
∀n[side] : (Length(n) = 0) ⇔ (Sides < n)

-- case -------------------------------------
Type:        
  
Definitions: 
  Rule:∀['$Large$0'][]: Large($Large$0) ⇔10 < ( if   $Large$0 = 4 then 4 else  if   $Large$0 = 3 then 3 else  if   $Large$0 = 2 then 2 else  if   $Large$0 = 1 then 1 else 5)
Universals:  
  ~Subtype = rectangle
  Perimeter = (sum{n[side] : true : Length(n)})
  (sum{n[side] : true : Angle(n)}) = ((Sides - 2) * 180)
  ∀x[side] : 0 ≤ Angle(x)
  ∀x[side] : Angle(x) ≠ 180
  ∀n[side] : (Angle(n) = 0) ⇔ (Vertices < n)
  ∀n[side] : (Length(n) = 0) ⇔ (Sides < n)
Consequences:
  ~Large(1)
  ~Type = triangle
  ~Sides = 3
  Type = quadrilateral
  Sides = 4
  ~Vertices = 3
  Vertices = 4
  ~Equilateral
  ~∀n[side] : (Length(n) = Length(1)) ∨ (Sides < n)
  ~Subtype = right_triangle
  ~Subtype = regular_triangle
  Subtype = irregular
  ~∀n[side] : (Angle(n) = 60) ∨ (Sides < n)
  ~Subtype = square
  ~∀n[side] : (Angle(n) = 90) ∨ (Sides < n)
  Sides = 4
  Vertices = 4
  Type = quadrilateral
  Subtype = irregular
  Perimeter = 10
  ~Large(2)
  ~Large(3)
  ~Large(4)
Simplified:  
  (Convex ⇔ (((Angle(1) < 180) ∧ (Angle(2) < 180) ∧ (Angle(3) < 180) ∧ (Angle(4) < 180))))
Irrelevant:  
  


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
                        'status': 'UNKNOWN',
                        'typ': 'Real',
                        'value': ''},
           'Angle(2)': {'environmental': False,
                        'normal': True,
                        'reading': 'Angle(2)',
                        'relevant': True,
                        'status': 'UNKNOWN',
                        'typ': 'Real',
                        'value': ''},
           'Angle(3)': {'environmental': False,
                        'normal': True,
                        'reading': 'Angle(3)',
                        'relevant': True,
                        'status': 'UNKNOWN',
                        'typ': 'Real',
                        'value': ''},
           'Angle(4)': {'environmental': False,
                        'normal': True,
                        'reading': 'Angle(4)',
                        'relevant': True,
                        'status': 'UNKNOWN',
                        'typ': 'Real',
                        'value': ''},
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
                                                        'value': False},
           '∀n[side] : (Angle(n) = 90) ∨ (Sides < n)': {'environmental': False,
                                                        'normal': False,
                                                        'reading': 'All angles are 90°',
                                                        'relevant': True,
                                                        'status': 'CONSEQUENCE',
                                                        'typ': 'Bool',
                                                        'value': False},
           '∀n[side] : Angle(n) < 180': {'environmental': False,
                                         'normal': False,
                                         'reading': 'All angles are below 180°',
                                         'relevant': True,
                                         'status': 'UNKNOWN',
                                         'typ': 'Bool'},
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
                                        'status': 'UNKNOWN',
                                        'typ': 'Bool'}},
 'Convex': {'Convex': {'environmental': False,
                       'normal': True,
                       'reading': 'Convex',
                       'relevant': True,
                       'status': 'UNKNOWN',
                       'typ': 'Bool'}},
 'Equilateral': {'Equilateral': {'environmental': False,
                                 'normal': True,
                                 'reading': 'Equilateral',
                                 'relevant': True,
                                 'status': 'CONSEQUENCE',
                                 'typ': 'Bool',
                                 'value': False}},
 'Large': {'Large(1)': {'environmental': False,
                        'normal': False,
                        'reading': 'Large(1)',
                        'relevant': True,
                        'status': 'CONSEQUENCE',
                        'typ': 'Bool',
                        'value': False},
           'Large(2)': {'environmental': False,
                        'normal': True,
                        'reading': 'Large(2)',
                        'relevant': True,
                        'status': 'CONSEQUENCE',
                        'typ': 'Bool',
                        'value': False},
           'Large(3)': {'environmental': False,
                        'normal': True,
                        'reading': 'Large(3)',
                        'relevant': True,
                        'status': 'CONSEQUENCE',
                        'typ': 'Bool',
                        'value': False},
           'Large(4)': {'environmental': False,
                        'normal': True,
                        'reading': 'Large(4)',
                        'relevant': True,
                        'status': 'CONSEQUENCE',
                        'typ': 'Bool',
                        'value': False}},
 'Perimeter': {'Perimeter': {'environmental': False,
                             'normal': True,
                             'reading': 'Perimeter',
                             'relevant': True,
                             'status': 'CONSEQUENCE',
                             'typ': 'Real',
                             'value': '10'},
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
                     'value': '4',
                     'values': ['3', '4']},
           'Sides = 3': {'environmental': False,
                         'normal': False,
                         'reading': 'Sides = 3',
                         'relevant': True,
                         'status': 'CONSEQUENCE',
                         'typ': 'Bool',
                         'value': False},
           'Sides = 4': {'environmental': False,
                         'normal': False,
                         'reading': 'Sides = 4',
                         'relevant': True,
                         'status': 'CONSEQUENCE',
                         'typ': 'Bool',
                         'value': True},
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
                                                                'value': False}},
 'Subtype': {'Subtype': {'environmental': False,
                         'normal': True,
                         'reading': 'Subtype',
                         'relevant': True,
                         'status': 'CONSEQUENCE',
                         'typ': 'subtype',
                         'value': 'irregular',
                         'values': ['regular_triangle', 'right_triangle', 'rectangle', 'square', 'irregular']},
             'Subtype = irregular': {'environmental': False,
                                     'normal': False,
                                     'reading': 'Subtype = irregular',
                                     'relevant': True,
                                     'status': 'CONSEQUENCE',
                                     'typ': 'Bool',
                                     'value': True},
             'Subtype = rectangle': {'environmental': False,
                                     'normal': False,
                                     'reading': 'Subtype = rectangle',
                                     'relevant': True,
                                     'status': 'UNIVERSAL',
                                     'typ': 'Bool',
                                     'value': False},
             'Subtype = regular_triangle': {'environmental': False,
                                            'normal': False,
                                            'reading': 'Subtype = regular_triangle',
                                            'relevant': True,
                                            'status': 'CONSEQUENCE',
                                            'typ': 'Bool',
                                            'value': False},
             'Subtype = right_triangle': {'environmental': False,
                                          'normal': False,
                                          'reading': 'Subtype = right_triangle',
                                          'relevant': True,
                                          'status': 'CONSEQUENCE',
                                          'typ': 'Bool',
                                          'value': False},
             'Subtype = square': {'environmental': False,
                                  'normal': False,
                                  'reading': 'Subtype = square',
                                  'relevant': True,
                                  'status': 'CONSEQUENCE',
                                  'typ': 'Bool',
                                  'value': False}},
 'Type': {'Type': {'environmental': False,
                   'normal': True,
                   'reading': 'Type',
                   'relevant': True,
                   'status': 'CONSEQUENCE',
                   'typ': 'type',
                   'value': 'quadrilateral',
                   'values': ['triangle', 'quadrilateral']},
          'Type = quadrilateral': {'environmental': False,
                                   'normal': False,
                                   'reading': 'Type = quadrilateral',
                                   'relevant': True,
                                   'status': 'CONSEQUENCE',
                                   'typ': 'Bool',
                                   'value': True},
          'Type = triangle': {'environmental': False,
                              'normal': False,
                              'reading': 'Type = triangle',
                              'relevant': True,
                              'status': 'CONSEQUENCE',
                              'typ': 'Bool',
                              'value': False}},
 'Vertices': {'Vertices': {'environmental': False,
                           'normal': True,
                           'reading': 'Vertices',
                           'relevant': True,
                           'status': 'CONSEQUENCE',
                           'typ': 'Int',
                           'value': '4',
                           'values': ['3', '4']},
              'Vertices = 3': {'environmental': False,
                               'normal': False,
                               'reading': 'Vertices = 3',
                               'relevant': True,
                               'status': 'CONSEQUENCE',
                               'typ': 'Bool',
                               'value': False},
              'Vertices = 4': {'environmental': False,
                               'normal': False,
                               'reading': 'Vertices = 4',
                               'relevant': True,
                               'status': 'CONSEQUENCE',
                               'typ': 'Bool',
                               'value': True}}}
