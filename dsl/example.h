vocabulary {
    p;
    q : Bool;
    r;
    a : Int;
    b : Int;
    c : Int;

    type Color constructed from {red, green, blue};

    col : Color;
    col2 : Color;
    col3 : Color;

    f(Int,Int) : Int;
}

theory {

f(a,b) ~= f(b,a);

f(a,c) = f(c,a);

}