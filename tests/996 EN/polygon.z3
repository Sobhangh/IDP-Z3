¬(subtype() = irregular)
¬(length(2) = length(1))
¬(angle(x) = 180)
- the type is triangle iff the number of edges is 3.
- the type is quadrilateral iff the number of edges is 4.
- (the number of vertices is 3 iff the number of edges is 3) and (the number of vertices is 4 iff the number of edges is 4).
- the number of edges is 3 is a sufficient condition for it is convex.
- it is convex iff (for every n ∈ Side_Nr, it is true that angle(n) < 180).
- it is equilateral iff (for every n ∈ Side_Nr, it is true that length(n) is length(1) or length(n) is 0).
- the number of edges is 3 is a sufficient condition for the subtype is right_triangle or the subtype is regular_triangle or the subtype is irregular.
- the number of edges is 4 is a sufficient condition for the subtype is square or the subtype is rectangle or the subtype is irregular.
- the subtype is square or the subtype is rectangle is a sufficient condition for the number of edges is 4.
- the subtype is regular_triangle iff the number of edges is 3 and it is equilateral.
- the subtype is regular_triangle iff the number of edges is 3 and (for every n ∈ Side_Nr, it is true that angle(n) is 60 or angle(n) is 0).
- the subtype is right_triangle iff the number of edges is 3 and (there is a n ∈ Side_Nr such that angle(n) is 90).
- the number of edges is 4 and the subtype is not irregular iff (for every n ∈ Side_Nr, it is true that angle(n) is 90 or angle(n) is 0).
- the subtype is rectangle is a sufficient condition for length(3) is length(1) and length(2) is length(4) and length(2) is not length(1).
- the subtype is square is a sufficient condition for the number of edges is 4 and it is equilateral.
- the type is triangle is a sufficient condition for (length(1) ≤ length(2) + length(3)) and (length(2) ≤ length(3) + length(1)) and (length(3) ≤ length(1) + length(2)).
- the perimeter is the sum of length(n) for all n ∈ Side_Nr.
- the sum of angle(n) for all n ∈ Side_Nr is (the number of edges - 2) ⨯ 180.
- for every x ∈ Side_Nr, it is true that 0 ≤ length(x).
- for every x ∈ Side_Nr, it is true that 0 ≤ angle(x).
- for every x ∈ Side_Nr, it is true that angle(x) is not 180.
- for every n ∈ Side_Nr, it is true that angle(n) is 0 iff the number of vertices < n.
- for every n ∈ Side_Nr, it is true that length(n) is 0 iff the number of edges < n.
