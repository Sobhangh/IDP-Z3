Disappearing Quantified formulas
=
20200410105450

Problem: quantified expressions in theory may not appear in list of subtences

Example:
```
vocabulary {
    type color constructed from {red, blue, green}
} 
theory {
    ?c[color]: c=red.
}
```
→ no subtence detected !  reason: no unknown symbol left after expansion and simplification → no place to show it on GUI


#issue