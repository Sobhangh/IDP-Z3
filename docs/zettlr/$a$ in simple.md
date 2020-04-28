–-
title: \$a\$ in simple.z3
tags: #bug
   ID: 20200427091038
–-

Problem: atom `a = red` has a `'reading': '\$a\$ = red'` in the json result of tests/definition/simple.idp.  The reading should be `a = red` instead.
→ it would be incorrectly displayed in GUI

Root cause:
* Fresh variable a with $a$ reading is created to fill q_v in Definition.annotate
* instantiate does not change the reading.  If it would, the reading would become `red = red`

Options:
* workaround: do Clark completion manually, not automatically
* don't create a variable if the function has no argument
* do not quantify over value of a defined function