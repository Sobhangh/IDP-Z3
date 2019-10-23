
class Expression(object):
    # .sub_exprs : list of (transformed) Expression, to be translated to Z3
    # .type : a declaration object, or 'Bool', 'real', 'int', or None
    # .translated : the Z3 equivalent
    
    def subtences(self):
        out = {}
        for e in self.sub_exprs: out.update(e.subtences())
        return out
