- Definition:
     it is big if the perimeter > 5.
     it is big if length n°1 > 3.
- [Definition of triangle]
  the type is triangle if and only if the number of edges is 3.
- [Definition of rectangle]
  the type is quadrilateral if and only if the number of edges is 4.
- [There are as many vertices as there are sides]
  (the number of vertices is 3 if and only if the number of edges is 3) and (the number of vertices is 4 if and only if the number of edges is 4).
- [All triangles are convex]
  if the number of edges is 3, then it is convex.
- [Definition of convex]
  it is convex if and only if (for every n in Side_Nr, it is true that angle n°n < 180).
- [Definition of equilateral]
  it is equilateral if and only if (for every n in Side_Nr, it is true that length n°n is length n°1 or length n°n is 0).
- [nr_of_sides() = 3 ⇒ subtype() = right_triangle ∨ subtype() = regular_triangle ∨ subtype() = irregular]
  the subtype is right_triangle or the subtype is regular_triangle or the subtype is irregular are necessary conditions for the number of edges is 3.
- [nr_of_sides() = 4 ⇒ subtype() = square ∨ subtype() = rectangle ∨ subtype() = irregular]
  the subtype is square or the subtype is rectangle or the subtype is irregular are necessary conditions for the number of edges is 4.
- [Squares and rectangles are quadrilaterals]
  if the subtype is square or the subtype is rectangle, then the number of edges is 4.
- [A regular triangle is an equilateral triangle]
  the subtype is regular_triangle if and only if the number of edges is 3 and it is equilateral.
- [A regular triangle is a triangle where all angles are 60°]
  the subtype is regular_triangle if and only if the number of edges is 3 and (for every n in Side_Nr, it is true that angle n°n is 60 or angle n°n is 0).
- [A right triangle is a triangle with a 90° angle]
  the subtype is right_triangle if and only if the number of edges is 3 and (there is a n in Side_Nr such that angle n°n is 90).
- [All angles are 90° in squares and rectangles]
  the number of edges is 4 and the subtype is not irregular if and only if (for every n in Side_Nr, it is true that angle n°n is 90 or angle n°n is 0).
- [In a rectangle, opposite Side_Nr have the same length, and adjacent sides have different lengths]
  if the subtype is rectangle, then length n°3 is length n°1 and length n°2 is length n°4 and length n°2 is not length n°1.
- [A square is an equilateral quadrilateral]
  if the subtype is square, then the number of edges is 4 and it is equilateral.
- [In a triangle, no Side_Nr is longer than the sum of the 2 other sides]
  if the type is triangle, then (length n°1 ≤ length n°2 + length n°3) and (length n°2 ≤ length n°3 + length n°1) and (length n°3 ≤ length n°1 + length n°2).
- [The perimeter is the sum of the lengths of the sides]
  the perimeter is the sum of length n°n for all n in Side_Nr.
- [The sum of the angles is 180° for a triangle, and 360° for a quadrilateral]
  (the sum of angle n°n for all n in Side_Nr such that 0 ≤ n) is (the number of edges - 2) ⨯ 180.
- [Lengths are positive numbers]
  for every x in Side_Nr, it is true that 0 ≤ length n°x.
- [Angles are positive numbers]
  for every x in Side_Nr, it is true that 0 ≤ angle n°x.
- [Angles cannot be 180°]
  for every x in Side_Nr, it is true that angle n°x is not 180.
- [A polygon with N vertices has N angles]
  for every n in Side_Nr, it is true that angle n°n is 0 if and only if the number of vertices < n.
- [A polygon with N sides has N lengths]
  for every n in Side_Nr, it is true that length n°n is 0 if and only if the number of edges < n.
