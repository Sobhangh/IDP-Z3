
class Expression(object):
    # .str : normalized idp code, before transformations
    # .sub_exprs : list of (transformed) Expression, to be translated to Z3
    # .type : a declaration object, or 'Bool', 'real', 'int', or None
    # .translated : the Z3 equivalent
    
    def __str__(self): return self.str

    def subtences(self):
        out = {}
        for e in self.sub_exprs: out.update(e.subtences())
        return out
