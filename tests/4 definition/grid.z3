And(2 == gridSize,
    x1 == clip(4),
    p == _add(pos(1, 2), pos(2, 1)),
    is(pos, _add(pos(1, 1), pos(1, 1))),
    is(pos, _add(pos(1, 1), pos(1, 2))),
    is(pos, _add(pos(1, 1), pos(2, 1))),
    is(pos, _add(pos(1, 1), pos(2, 2))),
    is(pos, _add(pos(1, 2), pos(1, 1))),
    is(pos, _add(pos(1, 2), pos(1, 2))),
    is(pos, _add(pos(1, 2), pos(2, 1))),
    is(pos, _add(pos(1, 2), pos(2, 2))),
    is(pos, _add(pos(2, 1), pos(1, 1))),
    is(pos, _add(pos(2, 1), pos(1, 2))),
    is(pos, _add(pos(2, 1), pos(2, 1))),
    is(pos, _add(pos(2, 1), pos(2, 2))),
    is(pos, _add(pos(2, 2), pos(1, 1))),
    is(pos, _add(pos(2, 2), pos(1, 2))),
    is(pos, _add(pos(2, 2), pos(2, 1))),
    is(pos, _add(pos(2, 2), pos(2, 2))),
    Or(1 == x1, 2 == x1),
    is(pos, p),
    clip(4) == If(4 > gridSize, gridSize, 4),
    _add(pos(1, 2), pos(2, 1)) == makePos(3, 3),
    makePos(3, 3) == pos(clip(3), clip(3)),
    clip(3) == If(3 > gridSize, gridSize, 3),
    _add(pos(1, 1), pos(1, 1)) == makePos(2, 2),
    makePos(2, 2) == pos(clip(2), clip(2)),
    clip(2) == If(2 > gridSize, gridSize, 2),
    _add(pos(1, 1), pos(1, 2)) == makePos(2, 3),
    makePos(2, 3) == pos(clip(2), clip(3)),
    _add(pos(1, 1), pos(2, 1)) == makePos(3, 2),
    makePos(3, 2) == pos(clip(3), clip(2)),
    _add(pos(1, 1), pos(2, 2)) == makePos(3, 3),
    _add(pos(1, 2), pos(1, 1)) == makePos(2, 3),
    _add(pos(1, 2), pos(1, 2)) == makePos(2, 4),
    makePos(2, 4) == pos(clip(2), clip(4)),
    _add(pos(1, 2), pos(2, 2)) == makePos(3, 4),
    makePos(3, 4) == pos(clip(3), clip(4)),
    _add(pos(2, 1), pos(1, 1)) == makePos(3, 2),
    _add(pos(2, 1), pos(1, 2)) == makePos(3, 3),
    _add(pos(2, 1), pos(2, 1)) == makePos(4, 2),
    makePos(4, 2) == pos(clip(4), clip(2)),
    _add(pos(2, 1), pos(2, 2)) == makePos(4, 3),
    makePos(4, 3) == pos(clip(4), clip(3)),
    _add(pos(2, 2), pos(1, 1)) == makePos(3, 3),
    _add(pos(2, 2), pos(1, 2)) == makePos(3, 4),
    _add(pos(2, 2), pos(2, 1)) == makePos(4, 3),
    _add(pos(2, 2), pos(2, 2)) == makePos(4, 4),
    makePos(4, 4) == pos(clip(4), clip(4)),
    And((_add(pos(1, 1), pos(1, 1)) == pos(1, 1)) ==
        (pos(1, 1) == makePos(2, 2)),
        (_add(pos(1, 1), pos(1, 1)) == pos(1, 2)) ==
        (pos(1, 2) == makePos(2, 2)),
        (_add(pos(1, 1), pos(1, 1)) == pos(2, 1)) ==
        (pos(2, 1) == makePos(2, 2)),
        (_add(pos(1, 1), pos(1, 1)) == pos(2, 2)) ==
        (pos(2, 2) == makePos(2, 2)),
        (_add(pos(1, 1), pos(1, 2)) == pos(1, 1)) ==
        (pos(1, 1) == makePos(2, 3)),
        (_add(pos(1, 1), pos(1, 2)) == pos(1, 2)) ==
        (pos(1, 2) == makePos(2, 3)),
        (_add(pos(1, 1), pos(1, 2)) == pos(2, 1)) ==
        (pos(2, 1) == makePos(2, 3)),
        (_add(pos(1, 1), pos(1, 2)) == pos(2, 2)) ==
        (pos(2, 2) == makePos(2, 3)),
        (_add(pos(1, 1), pos(2, 1)) == pos(1, 1)) ==
        (pos(1, 1) == makePos(3, 2)),
        (_add(pos(1, 1), pos(2, 1)) == pos(1, 2)) ==
        (pos(1, 2) == makePos(3, 2)),
        (_add(pos(1, 1), pos(2, 1)) == pos(2, 1)) ==
        (pos(2, 1) == makePos(3, 2)),
        (_add(pos(1, 1), pos(2, 1)) == pos(2, 2)) ==
        (pos(2, 2) == makePos(3, 2)),
        (_add(pos(1, 1), pos(2, 2)) == pos(1, 1)) ==
        (pos(1, 1) == makePos(3, 3)),
        (_add(pos(1, 1), pos(2, 2)) == pos(1, 2)) ==
        (pos(1, 2) == makePos(3, 3)),
        (_add(pos(1, 1), pos(2, 2)) == pos(2, 1)) ==
        (pos(2, 1) == makePos(3, 3)),
        (_add(pos(1, 1), pos(2, 2)) == pos(2, 2)) ==
        (pos(2, 2) == makePos(3, 3)),
        (_add(pos(1, 2), pos(1, 1)) == pos(1, 1)) ==
        (pos(1, 1) == makePos(2, 3)),
        (_add(pos(1, 2), pos(1, 1)) == pos(1, 2)) ==
        (pos(1, 2) == makePos(2, 3)),
        (_add(pos(1, 2), pos(1, 1)) == pos(2, 1)) ==
        (pos(2, 1) == makePos(2, 3)),
        (_add(pos(1, 2), pos(1, 1)) == pos(2, 2)) ==
        (pos(2, 2) == makePos(2, 3)),
        (_add(pos(1, 2), pos(1, 2)) == pos(1, 1)) ==
        (pos(1, 1) == makePos(2, 4)),
        (_add(pos(1, 2), pos(1, 2)) == pos(1, 2)) ==
        (pos(1, 2) == makePos(2, 4)),
        (_add(pos(1, 2), pos(1, 2)) == pos(2, 1)) ==
        (pos(2, 1) == makePos(2, 4)),
        (_add(pos(1, 2), pos(1, 2)) == pos(2, 2)) ==
        (pos(2, 2) == makePos(2, 4)),
        (_add(pos(1, 2), pos(2, 1)) == pos(1, 1)) ==
        (pos(1, 1) == makePos(3, 3)),
        (_add(pos(1, 2), pos(2, 1)) == pos(1, 2)) ==
        (pos(1, 2) == makePos(3, 3)),
        (_add(pos(1, 2), pos(2, 1)) == pos(2, 1)) ==
        (pos(2, 1) == makePos(3, 3)),
        (_add(pos(1, 2), pos(2, 1)) == pos(2, 2)) ==
        (pos(2, 2) == makePos(3, 3)),
        (_add(pos(1, 2), pos(2, 2)) == pos(1, 1)) ==
        (pos(1, 1) == makePos(3, 4)),
        (_add(pos(1, 2), pos(2, 2)) == pos(1, 2)) ==
        (pos(1, 2) == makePos(3, 4)),
        (_add(pos(1, 2), pos(2, 2)) == pos(2, 1)) ==
        (pos(2, 1) == makePos(3, 4)),
        (_add(pos(1, 2), pos(2, 2)) == pos(2, 2)) ==
        (pos(2, 2) == makePos(3, 4)),
        (_add(pos(2, 1), pos(1, 1)) == pos(1, 1)) ==
        (pos(1, 1) == makePos(3, 2)),
        (_add(pos(2, 1), pos(1, 1)) == pos(1, 2)) ==
        (pos(1, 2) == makePos(3, 2)),
        (_add(pos(2, 1), pos(1, 1)) == pos(2, 1)) ==
        (pos(2, 1) == makePos(3, 2)),
        (_add(pos(2, 1), pos(1, 1)) == pos(2, 2)) ==
        (pos(2, 2) == makePos(3, 2)),
        (_add(pos(2, 1), pos(1, 2)) == pos(1, 1)) ==
        (pos(1, 1) == makePos(3, 3)),
        (_add(pos(2, 1), pos(1, 2)) == pos(1, 2)) ==
        (pos(1, 2) == makePos(3, 3)),
        (_add(pos(2, 1), pos(1, 2)) == pos(2, 1)) ==
        (pos(2, 1) == makePos(3, 3)),
        (_add(pos(2, 1), pos(1, 2)) == pos(2, 2)) ==
        (pos(2, 2) == makePos(3, 3)),
        (_add(pos(2, 1), pos(2, 1)) == pos(1, 1)) ==
        (pos(1, 1) == makePos(4, 2)),
        (_add(pos(2, 1), pos(2, 1)) == pos(1, 2)) ==
        (pos(1, 2) == makePos(4, 2)),
        (_add(pos(2, 1), pos(2, 1)) == pos(2, 1)) ==
        (pos(2, 1) == makePos(4, 2)),
        (_add(pos(2, 1), pos(2, 1)) == pos(2, 2)) ==
        (pos(2, 2) == makePos(4, 2)),
        (_add(pos(2, 1), pos(2, 2)) == pos(1, 1)) ==
        (pos(1, 1) == makePos(4, 3)),
        (_add(pos(2, 1), pos(2, 2)) == pos(1, 2)) ==
        (pos(1, 2) == makePos(4, 3)),
        (_add(pos(2, 1), pos(2, 2)) == pos(2, 1)) ==
        (pos(2, 1) == makePos(4, 3)),
        (_add(pos(2, 1), pos(2, 2)) == pos(2, 2)) ==
        (pos(2, 2) == makePos(4, 3)),
        (_add(pos(2, 2), pos(1, 1)) == pos(1, 1)) ==
        (pos(1, 1) == makePos(3, 3)),
        (_add(pos(2, 2), pos(1, 1)) == pos(1, 2)) ==
        (pos(1, 2) == makePos(3, 3)),
        (_add(pos(2, 2), pos(1, 1)) == pos(2, 1)) ==
        (pos(2, 1) == makePos(3, 3)),
        (_add(pos(2, 2), pos(1, 1)) == pos(2, 2)) ==
        (pos(2, 2) == makePos(3, 3)),
        (_add(pos(2, 2), pos(1, 2)) == pos(1, 1)) ==
        (pos(1, 1) == makePos(3, 4)),
        (_add(pos(2, 2), pos(1, 2)) == pos(1, 2)) ==
        (pos(1, 2) == makePos(3, 4)),
        (_add(pos(2, 2), pos(1, 2)) == pos(2, 1)) ==
        (pos(2, 1) == makePos(3, 4)),
        (_add(pos(2, 2), pos(1, 2)) == pos(2, 2)) ==
        (pos(2, 2) == makePos(3, 4)),
        (_add(pos(2, 2), pos(2, 1)) == pos(1, 1)) ==
        (pos(1, 1) == makePos(4, 3)),
        (_add(pos(2, 2), pos(2, 1)) == pos(1, 2)) ==
        (pos(1, 2) == makePos(4, 3)),
        (_add(pos(2, 2), pos(2, 1)) == pos(2, 1)) ==
        (pos(2, 1) == makePos(4, 3)),
        (_add(pos(2, 2), pos(2, 1)) == pos(2, 2)) ==
        (pos(2, 2) == makePos(4, 3)),
        (_add(pos(2, 2), pos(2, 2)) == pos(1, 1)) ==
        (pos(1, 1) == makePos(4, 4)),
        (_add(pos(2, 2), pos(2, 2)) == pos(1, 2)) ==
        (pos(1, 2) == makePos(4, 4)),
        (_add(pos(2, 2), pos(2, 2)) == pos(2, 1)) ==
        (pos(2, 1) == makePos(4, 4)),
        (_add(pos(2, 2), pos(2, 2)) == pos(2, 2)) ==
        (pos(2, 2) == makePos(4, 4))))

Model 1
==========
gridSize:={->2}
_add:={(pos(1, 1),pos(1, 1))->pos(2, 2); (pos(1, 1),pos(1, 2))->pos(2, 2); (pos(1, 1),pos(2, 1))->pos(2, 2); (pos(1, 1),pos(2, 2))->pos(2, 2); (pos(1, 2),pos(1, 1))->pos(2, 2); (pos(1, 2),pos(1, 2))->pos(2, 2); (pos(1, 2),pos(2, 1))->pos(2, 2); (pos(1, 2),pos(2, 2))->pos(2, 2); (pos(2, 1),pos(1, 1))->pos(2, 2); (pos(2, 1),pos(1, 2))->pos(2, 2); (pos(2, 1),pos(2, 1))->pos(2, 2); (pos(2, 1),pos(2, 2))->pos(2, 2); (pos(2, 2),pos(1, 1))->pos(2, 2); (pos(2, 2),pos(1, 2))->pos(2, 2); (pos(2, 2),pos(2, 1))->pos(2, 2); (pos(2, 2),pos(2, 2))->pos(2, 2)}
x1:={->2}
p:={->pos(2, 2)}
clip:={4->2; 3->2}
makePos:={(3,3)->pos(2, 2)}

