T, S

Model 1
==========
Color:={->blue}
opposite:={red->green; blue->blue; green->green}
is_color:={red->false; blue->false; green->false}
f:={(A,A)->A; (A,B)->A; (B,A)->B; (B,B)->A}

Model 2
==========
Color:={->blue}
opposite:={red->green; blue->blue; green->green}
is_color:={red->false; blue->false; green->false}
f:={(A,A)->A; (A,B)->A; (B,A)->B; (B,B)->B}

No more models.
propagate
And(True, True, True)
T, S2
No models.
T2, S

Model 1
==========
Color:={->green}
opposite:={red->green; blue->green; green->green}
is_color:={red->false; blue->false; green->false}
f:={(A,A)->A; (A,B)->A; (B,A)->B; (B,B)->A}

Model 2
==========
Color:={->green}
opposite:={red->green; blue->green; green->green}
is_color:={red->false; blue->false; green->false}
f:={(A,A)->A; (A,B)->A; (B,A)->B; (B,B)->B}

No more models.
T4, S2

Model 1
==========
Color:={->blue}
opposite:={red->green; blue->blue; green->red}
is_color:={red->true; blue->false; green->false}
f:={(A,A)->A; (A,B)->A; (B,A)->B; (B,B)->B}

No more models.
