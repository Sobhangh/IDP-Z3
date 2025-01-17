
-- original ---------------------------------
vocabulary {

    type sides := {3..4}
    Sides: ()→sides
    Vertices: ()→sides


    type type := {triangle, quadrilateral}
    Type : ()→type

    type side := {1..4}
    Length:(side)→Real
    Angle:(side)→Real

    type subtype :=
        { regular_triangle
        , right_triangle
        , rectangle
        , square
        , irregular}
    Subtype : ()→ subtype

    Convex, Equilateral:() → Bool
    Perimeter:()→Real

    Large:(side) → Bool
    // Base : Real
    // Height: Real
    // Surface:Real
}

theory {
    { !n in side: Large(n) <- 10 < Length(n).}
    !n in side: Length(n) < Length(n+1).
    ~Large(1) | Large(1).

    [Definition of triangle]
    (Type()=triangle      <=> Sides()=3).

    [Definition of rectangle]
    (Type()=quadrilateral <=> Sides()=4).

    [There are as many vertices as there are sides]
    ( (Vertices()=3 <=> Sides()=3) &
      (Vertices()=4 <=> Sides()=4)).

    [All triangles are convex]
    Sides()=3 => Convex().

    [Definition of Convex]
    (Convex() <=> [All angles are below 180°]
                  ∀n in side: Angle(n)<180).

    [Definition of Equilateral]
    (Equilateral() <=> [All sides have the same length]
                       ∀n in side: Length(n)=Length(1) | Sides() < n).

    [A triangle is regular, right, or irregular]
    ( Subtype()=right_triangle | Subtype()=regular_triangle | Subtype()=irregular <= Sides()=3).


    [A regular triangle is an equilateral triangle]
    (Subtype()=regular_triangle <=> Sides()=3 & Equilateral()).

    [A regular triangle is a triangle where all angles are 60°]
    (Subtype()=regular_triangle <=> Sides()=3 & [All angles are 60°]
                                            !n in side: Angle(n)=60 | Sides() < n).

    [A right triangle is a triangle with a 90° angle]
    (Subtype()=right_triangle   <=> Sides()=3 & [One angle is 90°]
                                           ?n in side: Angle(n)=90).

    [All angles are 90° in squares and rectangles]
    (Subtype()=square | Subtype()=rectangle <=> Sides()=4 & [All angles are 90°]
                                                     !n in side: Angle(n)=90 | Sides() < n).

    [In a rectangle, opposite side have the same length, and adjacent sides have different lengths]
    (Subtype()=rectangle => Length(1)=Length(3) & Length(2)=Length(4) & Length(1)~=Length(2)).

    [A square is an equilateral quadrilateral]
    Subtype()=square    <=> Sides()=4 & Equilateral().

    [In a triangle, no side is longer than the sum of the 2 other sides]
    Type()=triangle => [Short L1] Length(1) =< Length(2) + Length(3)
                    &    [Short L2] Length(2) =< Length(3) + Length(1)
                    &  ( Length(3) =< Length(1) + Length(2)).

    // General constraints

    [The perimeter is the sum of the lengths of the sides]
    (Perimeter() = sum(lambda n in side: Length(n))).

    [The sum of the angles is 180° for a triangle, and 360° for a quadrilateral]
    (sum(lambda n in side : Angle(n)) = (Sides()-2)*180).

    [Lengths are positive numbers]
    !x in side: 0 =< Length(x).

    [Angles are positive numbers]
    !x in side: 0 =< Angle(x).

    [Angles cannot be 180°]
    !x in side: Angle(x) ~= 180.

    [A polygon with N vertices has N angles]
    !n in side: Angle(n)=0 <=> Vertices()<n .

    [A polygon with N sides has N lengths]
    !n in side: Length(n)=0 <=> Sides()<n.



    // TODO : surface
    //Type=triangle => Surface = (Base * Height)/2.
    //Subtype=square | Subtype=rectangle => Surface = Length(1)*Length(2).
    //Subtype=irregular & Sides = 4 => Surface = -1.
    //0 =< Base.
    //0 =< Height.
    //?n in side: n=<Sides & Length(n)=Base.

    ~(Length(Sides()) is enumerated) => Length(Sides())=4.
}
structure {
    Length >> {1->1, 2->2, 3->3}.
}

display {
    view() = expanded.
    unit('m', `Length, `Perimeter).
    unit('degrees', `Angle).
}

-- meta -------------------------------------
{'manualPropagation': False,
 'manualRelevance': False,
 'optionalPropagation': False,
 'optionalRelevance': False,
 'symbols': [{'environmental': False,
              'idpname': 'Sides',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'expanded'},
             {'environmental': False,
              'idpname': 'Vertices',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'expanded'},
             {'environmental': False,
              'idpname': 'Type',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'expanded'},
             {'environmental': False,
              'idpname': 'Length',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'unit': 'm',
              'view': 'expanded'},
             {'environmental': False,
              'idpname': 'Angle',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'unit': 'degrees',
              'view': 'expanded'},
             {'environmental': False,
              'idpname': 'Subtype',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'expanded'},
             {'environmental': False,
              'idpname': 'Convex',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'expanded'},
             {'environmental': False,
              'idpname': 'Equilateral',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'expanded'},
             {'environmental': False,
              'idpname': 'Perimeter',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'unit': 'm',
              'view': 'expanded'},
             {'environmental': False,
              'idpname': 'Large',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'Angle': {'Angle(1)': {'environmental': False,
                        'is_assignment': True,
                        'normal': True,
                        'reading': 'Angle(1)',
                        'relevant': True,
                        'status': 'UNKNOWN',
                        'typ': 'Real'},
           'Angle(2)': {'environmental': False,
                        'is_assignment': True,
                        'normal': True,
                        'reading': 'Angle(2)',
                        'relevant': True,
                        'status': 'UNKNOWN',
                        'typ': 'Real'},
           'Angle(3)': {'environmental': False,
                        'is_assignment': True,
                        'normal': True,
                        'reading': 'Angle(3)',
                        'relevant': True,
                        'status': 'UNKNOWN',
                        'typ': 'Real'},
           'Angle(4)': {'environmental': False,
                        'is_assignment': True,
                        'normal': True,
                        'reading': 'Angle(4)',
                        'relevant': True,
                        'status': 'UNKNOWN',
                        'typ': 'Real'},
           'sum(lambda n ∈ side : Angle(n)) = (Sides() - 2) ⨯ 180': {'environmental': False,
                                                                     'is_assignment': False,
                                                                     'normal': False,
                                                                     'reading': 'The sum of the angles is 180° for a '
                                                                                'triangle, and 360° for a '
                                                                                'quadrilateral',
                                                                     'relevant': False,
                                                                     'status': 'UNIVERSAL',
                                                                     'typ': 'Bool',
                                                                     'value': True},
           '∀ n ∈ side: Angle(n) < 180': {'environmental': False,
                                          'is_assignment': False,
                                          'normal': False,
                                          'reading': 'All angles are below 180°',
                                          'relevant': True,
                                          'status': 'UNKNOWN',
                                          'typ': 'Bool'},
           '∀ n ∈ side: Angle(n) = 0 ⇔ Vertices() < n': {'environmental': False,
                                                         'is_assignment': False,
                                                         'normal': False,
                                                         'reading': 'A polygon with N vertices has N angles',
                                                         'relevant': False,
                                                         'status': 'UNIVERSAL',
                                                         'typ': 'Bool',
                                                         'value': True},
           '∀ n ∈ side: Angle(n) = 60 ∨ Sides() < n': {'environmental': False,
                                                       'is_assignment': False,
                                                       'normal': False,
                                                       'reading': 'All angles are 60°',
                                                       'relevant': False,
                                                       'status': 'UNIVERSAL',
                                                       'typ': 'Bool',
                                                       'value': False},
           '∀ n ∈ side: Angle(n) = 90 ∨ Sides() < n': {'environmental': False,
                                                       'is_assignment': False,
                                                       'normal': False,
                                                       'reading': 'All angles are 90°',
                                                       'relevant': False,
                                                       'status': 'UNIVERSAL',
                                                       'typ': 'Bool',
                                                       'value': False},
           '∀ x ∈ side: 0 ≤ Angle(x)': {'environmental': False,
                                        'is_assignment': False,
                                        'normal': False,
                                        'reading': 'Angles are positive numbers',
                                        'relevant': False,
                                        'status': 'UNIVERSAL',
                                        'typ': 'Bool',
                                        'value': True},
           '∀ x ∈ side: Angle(x) ≠ 180': {'environmental': False,
                                          'is_assignment': False,
                                          'normal': False,
                                          'reading': 'Angles cannot be 180°',
                                          'relevant': False,
                                          'status': 'UNIVERSAL',
                                          'typ': 'Bool',
                                          'value': True},
           '∃ n ∈ side: Angle(n) = 90': {'environmental': False,
                                         'is_assignment': False,
                                         'normal': False,
                                         'reading': 'One angle is 90°',
                                         'relevant': False,
                                         'status': 'UNKNOWN',
                                         'typ': 'Bool'}},
 'Convex': {'Convex()': {'environmental': False,
                         'is_assignment': False,
                         'normal': True,
                         'reading': 'Convex',
                         'relevant': True,
                         'status': 'UNKNOWN',
                         'typ': 'Bool'}},
 'Equilateral': {'Equilateral()': {'environmental': False,
                                   'is_assignment': False,
                                   'normal': True,
                                   'reading': 'Equilateral',
                                   'relevant': False,
                                   'status': 'UNIVERSAL',
                                   'typ': 'Bool',
                                   'value': False}},
 'Large': {'Large(1)': {'environmental': False,
                        'is_assignment': False,
                        'normal': True,
                        'reading': 'Large(1)',
                        'relevant': False,
                        'status': 'UNIVERSAL',
                        'typ': 'Bool',
                        'value': False},
           'Large(2)': {'environmental': False,
                        'is_assignment': False,
                        'normal': True,
                        'reading': 'Large(2)',
                        'relevant': False,
                        'status': 'UNIVERSAL',
                        'typ': 'Bool',
                        'value': False},
           'Large(3)': {'environmental': False,
                        'is_assignment': False,
                        'normal': True,
                        'reading': 'Large(3)',
                        'relevant': False,
                        'status': 'UNIVERSAL',
                        'typ': 'Bool',
                        'value': False},
           'Large(4)': {'environmental': False,
                        'is_assignment': False,
                        'normal': True,
                        'reading': 'Large(4)',
                        'relevant': False,
                        'status': 'UNIVERSAL',
                        'typ': 'Bool',
                        'value': False}},
 'Length': {},
 'Perimeter': {'Perimeter()': {'environmental': False,
                               'is_assignment': True,
                               'normal': True,
                               'reading': 'Perimeter',
                               'relevant': False,
                               'status': 'UNIVERSAL',
                               'typ': 'Real',
                               'value': '10'},
               'Perimeter() = sum(lambda n ∈ side : Length(n))': {'environmental': False,
                                                                  'is_assignment': False,
                                                                  'normal': False,
                                                                  'reading': 'The perimeter is the sum of the lengths '
                                                                             'of the sides',
                                                                  'relevant': False,
                                                                  'status': 'UNIVERSAL',
                                                                  'typ': 'Bool',
                                                                  'value': True}},
 'Sides': {'Length(Sides())': {'environmental': False,
                               'is_assignment': True,
                               'normal': False,
                               'reading': 'Length(Sides)',
                               'relevant': False,
                               'status': 'UNIVERSAL',
                               'typ': 'Real',
                               'value': '4',
                               'values': ['4']},
           'Length(Sides()) = 4': {'environmental': False,
                                   'is_assignment': False,
                                   'normal': False,
                                   'reading': 'Length(Sides) = 4',
                                   'relevant': False,
                                   'status': 'UNIVERSAL',
                                   'typ': 'Bool',
                                   'value': True},
           'Length(Sides()) is enumerated': {'environmental': False,
                                             'is_assignment': False,
                                             'normal': False,
                                             'reading': 'Length(Sides) is enumerated',
                                             'relevant': False,
                                             'status': 'UNIVERSAL',
                                             'typ': 'Bool',
                                             'value': False},
           'Sides()': {'environmental': False,
                       'is_assignment': True,
                       'normal': True,
                       'reading': 'Sides',
                       'relevant': False,
                       'status': 'UNIVERSAL',
                       'typ': 'Int',
                       'value': '4',
                       'values': ['4']},
           'Sides() = 1': {'environmental': False,
                           'is_assignment': True,
                           'normal': False,
                           'reading': 'Sides = 1',
                           'relevant': False,
                           'status': 'UNIVERSAL',
                           'typ': 'Bool',
                           'value': False},
           'Sides() = 2': {'environmental': False,
                           'is_assignment': True,
                           'normal': False,
                           'reading': 'Sides = 2',
                           'relevant': False,
                           'status': 'UNIVERSAL',
                           'typ': 'Bool',
                           'value': False},
           'Sides() = 3': {'environmental': False,
                           'is_assignment': True,
                           'normal': False,
                           'reading': 'Sides = 3',
                           'relevant': False,
                           'status': 'UNIVERSAL',
                           'typ': 'Bool',
                           'value': False},
           'Sides() = 4': {'environmental': False,
                           'is_assignment': True,
                           'normal': False,
                           'reading': 'Sides = 4',
                           'relevant': False,
                           'status': 'UNIVERSAL',
                           'typ': 'Bool',
                           'value': True},
           '∀ n ∈ side: Length(n) = 0 ⇔ Sides() < n': {'environmental': False,
                                                       'is_assignment': False,
                                                       'normal': False,
                                                       'reading': 'A polygon with N sides has N lengths',
                                                       'relevant': False,
                                                       'status': 'UNIVERSAL',
                                                       'typ': 'Bool',
                                                       'value': True},
           '∀ n ∈ side: Length(n) = Length(1) ∨ Sides() < n': {'environmental': False,
                                                               'is_assignment': False,
                                                               'normal': False,
                                                               'reading': 'All sides have the same length',
                                                               'relevant': False,
                                                               'status': 'UNIVERSAL',
                                                               'typ': 'Bool',
                                                               'value': False}},
 'Subtype': {'Subtype()': {'environmental': False,
                           'is_assignment': True,
                           'normal': True,
                           'reading': 'Subtype',
                           'relevant': False,
                           'status': 'UNIVERSAL',
                           'typ': 'subtype',
                           'value': 'irregular',
                           'values': ['irregular']},
             'Subtype() = irregular': {'environmental': False,
                                       'is_assignment': True,
                                       'normal': False,
                                       'reading': 'Subtype = irregular',
                                       'relevant': False,
                                       'status': 'UNIVERSAL',
                                       'typ': 'Bool',
                                       'value': True},
             'Subtype() = rectangle': {'environmental': False,
                                       'is_assignment': True,
                                       'normal': False,
                                       'reading': 'Subtype = rectangle',
                                       'relevant': False,
                                       'status': 'UNIVERSAL',
                                       'typ': 'Bool',
                                       'value': False},
             'Subtype() = regular_triangle': {'environmental': False,
                                              'is_assignment': True,
                                              'normal': False,
                                              'reading': 'Subtype = regular_triangle',
                                              'relevant': False,
                                              'status': 'UNIVERSAL',
                                              'typ': 'Bool',
                                              'value': False},
             'Subtype() = right_triangle': {'environmental': False,
                                            'is_assignment': True,
                                            'normal': False,
                                            'reading': 'Subtype = right_triangle',
                                            'relevant': False,
                                            'status': 'UNIVERSAL',
                                            'typ': 'Bool',
                                            'value': False},
             'Subtype() = square': {'environmental': False,
                                    'is_assignment': True,
                                    'normal': False,
                                    'reading': 'Subtype = square',
                                    'relevant': False,
                                    'status': 'UNIVERSAL',
                                    'typ': 'Bool',
                                    'value': False}},
 'Type': {'Type()': {'environmental': False,
                     'is_assignment': True,
                     'normal': True,
                     'reading': 'Type',
                     'relevant': False,
                     'status': 'UNIVERSAL',
                     'typ': 'type',
                     'value': 'quadrilateral',
                     'values': ['quadrilateral']},
          'Type() = quadrilateral': {'environmental': False,
                                     'is_assignment': True,
                                     'normal': False,
                                     'reading': 'Type = quadrilateral',
                                     'relevant': False,
                                     'status': 'UNIVERSAL',
                                     'typ': 'Bool',
                                     'value': True},
          'Type() = triangle': {'environmental': False,
                                'is_assignment': True,
                                'normal': False,
                                'reading': 'Type = triangle',
                                'relevant': False,
                                'status': 'UNIVERSAL',
                                'typ': 'Bool',
                                'value': False}},
 'Vertices': {'Vertices()': {'environmental': False,
                             'is_assignment': True,
                             'normal': True,
                             'reading': 'Vertices',
                             'relevant': False,
                             'status': 'UNIVERSAL',
                             'typ': 'Int',
                             'value': '4',
                             'values': ['4']},
              'Vertices() = 3': {'environmental': False,
                                 'is_assignment': True,
                                 'normal': False,
                                 'reading': 'Vertices = 3',
                                 'relevant': False,
                                 'status': 'UNIVERSAL',
                                 'typ': 'Bool',
                                 'value': False},
              'Vertices() = 4': {'environmental': False,
                                 'is_assignment': True,
                                 'normal': False,
                                 'reading': 'Vertices = 4',
                                 'relevant': False,
                                 'status': 'UNIVERSAL',
                                 'typ': 'Bool',
                                 'value': True}}}
