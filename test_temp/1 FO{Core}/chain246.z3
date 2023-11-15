And(Or(colorOf(A, A) == Red, colorOf(A, A) == Blue),
    Or(colorOf(A, B) == Red, colorOf(A, B) == Blue),
    Or(colorOf(A, C) == Red, colorOf(A, C) == Blue),
    Or(colorOf(A, D) == Red, colorOf(A, D) == Blue),
    Or(colorOf(B, A) == Red, colorOf(B, A) == Blue),
    Or(colorOf(B, B) == Red, colorOf(B, B) == Blue),
    Or(colorOf(B, C) == Red, colorOf(B, C) == Blue),
    Or(colorOf(B, D) == Red, colorOf(B, D) == Blue),
    Or(colorOf(C, A) == Red, colorOf(C, A) == Blue),
    Or(colorOf(C, B) == Red, colorOf(C, B) == Blue),
    Or(colorOf(C, C) == Red, colorOf(C, C) == Blue),
    Or(colorOf(C, D) == Red, colorOf(C, D) == Blue),
    Or(colorOf(D, A) == Red, colorOf(D, A) == Blue),
    Or(colorOf(D, B) == Red, colorOf(D, B) == Blue),
    Or(colorOf(D, C) == Red, colorOf(D, C) == Blue),
    Or(colorOf(D, D) == Red, colorOf(D, D) == Blue),
    And(Not(_monochrome_triangle(A, A, A)),
        Not(_monochrome_triangle(A, A, B)),
        Not(_monochrome_triangle(A, A, C)),
        Not(_monochrome_triangle(A, A, D)),
        Not(_monochrome_triangle(A, B, A)),
        Not(_monochrome_triangle(A, B, B)),
        _monochrome_triangle(A, B, C) ==
        And(colorOf(A, B) == colorOf(B, C),
            colorOf(B, C) == colorOf(C, A)),
        _monochrome_triangle(A, B, D) ==
        And(colorOf(A, B) == colorOf(B, D),
            colorOf(B, D) == colorOf(D, A)),
        Not(_monochrome_triangle(A, C, A)),
        _monochrome_triangle(A, C, B) ==
        And(colorOf(A, C) == colorOf(C, B),
            colorOf(C, B) == colorOf(B, A)),
        Not(_monochrome_triangle(A, C, C)),
        _monochrome_triangle(A, C, D) ==
        And(colorOf(A, C) == colorOf(C, D),
            colorOf(C, D) == colorOf(D, A)),
        Not(_monochrome_triangle(A, D, A)),
        _monochrome_triangle(A, D, B) ==
        And(colorOf(A, D) == colorOf(D, B),
            colorOf(D, B) == colorOf(B, A)),
        _monochrome_triangle(A, D, C) ==
        And(colorOf(A, D) == colorOf(D, C),
            colorOf(D, C) == colorOf(C, A)),
        Not(_monochrome_triangle(A, D, D)),
        Not(_monochrome_triangle(B, A, A)),
        Not(_monochrome_triangle(B, A, B)),
        _monochrome_triangle(B, A, C) ==
        And(colorOf(B, A) == colorOf(A, C),
            colorOf(A, C) == colorOf(C, B)),
        _monochrome_triangle(B, A, D) ==
        And(colorOf(B, A) == colorOf(A, D),
            colorOf(A, D) == colorOf(D, B)),
        Not(_monochrome_triangle(B, B, A)),
        Not(_monochrome_triangle(B, B, B)),
        Not(_monochrome_triangle(B, B, C)),
        Not(_monochrome_triangle(B, B, D)),
        _monochrome_triangle(B, C, A) ==
        And(colorOf(B, C) == colorOf(C, A),
            colorOf(C, A) == colorOf(A, B)),
        Not(_monochrome_triangle(B, C, B)),
        Not(_monochrome_triangle(B, C, C)),
        _monochrome_triangle(B, C, D) ==
        And(colorOf(B, C) == colorOf(C, D),
            colorOf(C, D) == colorOf(D, B)),
        _monochrome_triangle(B, D, A) ==
        And(colorOf(B, D) == colorOf(D, A),
            colorOf(D, A) == colorOf(A, B)),
        Not(_monochrome_triangle(B, D, B)),
        _monochrome_triangle(B, D, C) ==
        And(colorOf(B, D) == colorOf(D, C),
            colorOf(D, C) == colorOf(C, B)),
        Not(_monochrome_triangle(B, D, D)),
        Not(_monochrome_triangle(C, A, A)),
        _monochrome_triangle(C, A, B) ==
        And(colorOf(C, A) == colorOf(A, B),
            colorOf(A, B) == colorOf(B, C)),
        Not(_monochrome_triangle(C, A, C)),
        _monochrome_triangle(C, A, D) ==
        And(colorOf(C, A) == colorOf(A, D),
            colorOf(A, D) == colorOf(D, C)),
        _monochrome_triangle(C, B, A) ==
        And(colorOf(C, B) == colorOf(B, A),
            colorOf(B, A) == colorOf(A, C)),
        Not(_monochrome_triangle(C, B, B)),
        Not(_monochrome_triangle(C, B, C)),
        _monochrome_triangle(C, B, D) ==
        And(colorOf(C, B) == colorOf(B, D),
            colorOf(B, D) == colorOf(D, C)),
        Not(_monochrome_triangle(C, C, A)),
        Not(_monochrome_triangle(C, C, B)),
        Not(_monochrome_triangle(C, C, C)),
        Not(_monochrome_triangle(C, C, D)),
        _monochrome_triangle(C, D, A) ==
        And(colorOf(C, D) == colorOf(D, A),
            colorOf(D, A) == colorOf(A, C)),
        _monochrome_triangle(C, D, B) ==
        And(colorOf(C, D) == colorOf(D, B),
            colorOf(D, B) == colorOf(B, C)),
        Not(_monochrome_triangle(C, D, C)),
        Not(_monochrome_triangle(C, D, D)),
        Not(_monochrome_triangle(D, A, A)),
        _monochrome_triangle(D, A, B) ==
        And(colorOf(D, A) == colorOf(A, B),
            colorOf(A, B) == colorOf(B, D)),
        _monochrome_triangle(D, A, C) ==
        And(colorOf(D, A) == colorOf(A, C),
            colorOf(A, C) == colorOf(C, D)),
        Not(_monochrome_triangle(D, A, D)),
        _monochrome_triangle(D, B, A) ==
        And(colorOf(D, B) == colorOf(B, A),
            colorOf(B, A) == colorOf(A, D)),
        Not(_monochrome_triangle(D, B, B)),
        _monochrome_triangle(D, B, C) ==
        And(colorOf(D, B) == colorOf(B, C),
            colorOf(B, C) == colorOf(C, D)),
        Not(_monochrome_triangle(D, B, D)),
        _monochrome_triangle(D, C, A) ==
        And(colorOf(D, C) == colorOf(C, A),
            colorOf(C, A) == colorOf(A, D)),
        _monochrome_triangle(D, C, B) ==
        And(colorOf(D, C) == colorOf(C, B),
            colorOf(C, B) == colorOf(B, D)),
        Not(_monochrome_triangle(D, C, C)),
        Not(_monochrome_triangle(D, C, D)),
        Not(_monochrome_triangle(D, D, A)),
        Not(_monochrome_triangle(D, D, B)),
        Not(_monochrome_triangle(D, D, C)),
        Not(_monochrome_triangle(D, D, D))))
