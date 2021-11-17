No more consequences.
And(Or(Not(p), Or(Color == red, Color == blue)),
    Or(Color == red, Color == blue, Color == green))

Model 1
==========
Color:={->blue}

Model 2
==========
Color:={->green}
p:={->false}

Model 3
==========
Color:={->red}
p:={->false}

Model 4
==========
Color:={->red}
p:={->true}

