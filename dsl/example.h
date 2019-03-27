vocabulary {
    p.
    q : Bool.
    r.
    a : Int.
    b : Int.
    c : Int.

    type Color constructed from {red, green, blue}.

    col : Color.
    col2 : Color.
    col3 : Color.
}

theory {
    p <=> (q | r).

    ~r.

     a  + b * c = 13 .
     a > 0 .
     a < 6 .
     b > 1 .
     c > 1 .

     col ~= red.

     col ~= col2.
     col2 ~= col3.
     col3 ~= col.
}