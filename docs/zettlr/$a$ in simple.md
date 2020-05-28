–-
title: \$a\$ in simple.z3
tags: #fixed
Date: 20200427091038
–-

Problem: atom `a = red` has a `'reading': '\$a\$ = red'` in the json result of tests/definition/simple.idp.  The reading should be `a = red` instead.
→ it would be incorrectly displayed in GUI

Other problem: select epoxy=e1 
* → unsatisfiable: fixed
* but shows \$Cost\$ = 0.539


Root cause:
* Fresh variable a with $a$ reading is created to fill q_v in Definition.annotate
* instantiate does not change the reading.  If it would, the reading would become `red = red`
* translation of '\$Cost\$ = a' is None

Options:
- [ ] workaround: do Clark completion manually, not automatically  → not working!
- [ ] don't create a variable if the function has no argument
- [ ] do not quantify over output value of a defined function
- [x] instantiate() updates expr.original 

The instantiation of $\{\forall x: \forall y: f(x)=y \leftarrow p(x,y).\}$ for $f(a)$ is $p(a, f(a))$. 
$\{\forall x: \forall y: f(x)=y \leftarrow p(x,y).\}$ can be replaced by $\{\forall x: p(x,f(x)).\}$ if $f(x)$ is total, non recursive and the definition constructive