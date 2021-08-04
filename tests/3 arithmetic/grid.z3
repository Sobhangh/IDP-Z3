p() = pos(1, 1) ∧ true ∧ q() = p() ∧ is_pos(p()) ∧ is_pos(q()) ∧ is_pos(position(0)) ∧ is_pos(position(1)) ∧ is_pos(position(2)) ∧ (position(0) = pos(0, 0)) ∧ (position(1) = pos(0, 0)) ∧ (position(2) = pos(0, 0)) ∧ (∀$position$ ∈ Pos : position(0) = $position$ ⇔ $position$ = pos(0, 0))

Model 1
==========
p:={->pos(1, 1)}
q:={->pos(1, 1)}
position:={0->pos(0, 0); 1->pos(0, 0); 2->pos(0, 0)}

No more models.
