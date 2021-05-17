R(rgb(t, u)) = t ∧ is_rgb(rgb(t, u)) ∧ ¬(is_rgb(red)) ∧ ¬(is_red(blue)) ∧ true ∧ true

Model 1
==========
R:={rgb(t, u)->t}
is_rgb:={rgb(t, u)->true; red->false}
is_red:={blue->false}

No more models.
