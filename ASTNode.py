import copy

class Expression(object):
    # .str : normalized idp code, before transformations
    # .sub_exprs : list of (transformed) Expression, to be translated to Z3
    # .type : a declaration object, or 'Bool', 'real', 'int', or None
    # .translated : the Z3 equivalent
    
    def __eq__(self, other):
        return self.str == other.str
    
    def __hash__(self):
        return hash(self.str)

    def __str__(self): return self.str

    def subtences(self):
        out = {}
        for e in self.sub_exprs: out.update(e.subtences())
        return out

    def simplify1(self):
        "simplify this node only"
        return self

    def substitute(self, e0, e1):
        if self == e0: # based on .str !
            return e1
        else:
            sub_exprs1 = [e.substitute(e0, e1) for e in self.sub_exprs]
            if all(e0 == e1 for (e0,e1) in zip(self.sub_exprs, sub_exprs1)): # not changed !
                return self
            else:
                out = copy.copy(self)
                out.sub_exprs = sub_exprs1
                out.str = repr(out)
                return out.simplify1()

    def expand_quantifiers(self, theory):
        sub_exprs1 = [e.expand_quantifiers(theory) for e in self.sub_exprs]
        if all(e0 == e1 for (e0,e1) in zip(self.sub_exprs, sub_exprs1)): # not changed !
            return self
        else:
            self.sub_exprs = sub_exprs1
            return self.simplify1()

    def interpret(self, theory):
        sub_exprs1 = [e.interpret(theory) for e in self.sub_exprs]
        if all(e0 == e1 for (e0,e1) in zip(self.sub_exprs, sub_exprs1)): # not changed !
            return self
        else:
            self.sub_exprs = sub_exprs1
            return self.simplify1()
