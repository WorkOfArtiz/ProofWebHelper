# Note that the to_label uses more or less reverse polish notation

# The structures
class Var:
    t = 'var'
    def __init__(self, var):
        self.var = var

    def to_label(self):
        return self.var.lower()

    def to_pw(self):
        return self.var

    def __str__(self):
        return str(self.var)

    def __repr__(self):
        return "Var (%s)" % self.var

# code to make sure every variable with the same name points to the exact same
# object
variables = dict()
def Variable(variable_name):
    if variable_name in variables.keys():
        return variables.get(variable_name)
    variable = Var(variable_name)
    variables[variable_name] = variable
    return variable

def get_variables():
    return variables.values()

class Not:
    t = '~'
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        if self.expr.t in ('~','var'):
            return "not %s" % str(self.expr)
        return "not (%s)" % str(self.expr)

    def to_pw(self):
        if self.expr.t in ('~','var'):
            return "~%s" % self.expr.to_pw()
        return "~(%s)" % self.expr.to_pw()

    def to_label(self):
        return "%sN" % self.expr.to_label()

    def __repr__(self):
        return "Not (%s)" % repr(self.expr)

class And:
    t = '&'
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def to_label(self):
        return "%s%sA" % (self.lhs.to_label(),self.rhs.to_label())

    def to_pw(self):
        return "(%s /\ %s)" % (self.lhs.to_pw(), self.rhs.to_pw())

    def __str__(self):
        return "%s and %s" % (str(self.lhs), str(self.rhs))

    def __repr__(self):
        return "And (%s) (%s)" % (repr(self.lhs), repr(self.rhs))

class Or:
    t = '|'
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def to_label(self):
        return "%s%sO" % (self.lhs.to_label(),self.rhs.to_label())

    def to_pw(self):
        return "(%s \/ %s)" % (self.lhs.to_pw(), self.rhs.to_pw())

    def __str__(self):
        return "%s or %s" % (str(self.lhs), str(self.rhs))

    def __repr__(self):
        return "Or (%s) (%s)" % (repr(self.lhs), repr(self.rhs))

class Implies:
    t = '->'
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def to_label(self):
        return "%s%sI" % (self.lhs.to_label(),self.rhs.to_label())

    def to_pw(self):
        return "(%s -> %s)" % (self.lhs.to_pw(), self.rhs.to_pw())

    def __str__(self):
        return "(%s -> %s)" % (str(self.lhs), str(self.rhs))

    def __repr__(self):
        return "Implies (%s) (%s)" % (repr(self.lhs), repr(self.rhs))


# @param expr: one of the above classes
# @param structure: a structure like
#                                     ('~', ('&', '*', '*'))
#                                     ('|', ('~', '*'), ('~', '*'))
def is_structure(expr, structure):
    top = structure[0]
    if top == '*':
        return True

    if expr.t != top:
        return False

    if top in ('->','&', '|'):
        op, lhs, rhs = structure
        return is_structure(expr.lhs, lhs) and is_structure(expr.rhs, rhs)
    else:
        op, sub = structure
        return is_structure(expr.expr, sub)
