"""
Functions for Premises (Givens)

All these functions get the next set of arguments:

@param labels   : set(string) contains labels of previously found expressions
@param premises : set(Expression) contains actual premises. will only be used
                  to append to
@param premise  : Expression premise up for investigation
"""
from struct import Implies, Var, And, Not, is_structure

# I basically made a sort of crappy haskell pattern matching
not_not_pattern = ('~', ('~', '*'))   # double negative checks, prem and res

"""
If I have a premise A -> B (with A and B arbitrary expressions)
    and I have A, I have B         (Modus Ponens)
    or if I have ~B I will have ~A (Mollens tollens)
"""
def premise_a_implies_b_simplify(labels, premises, premise):
    # if the premise is not of type Implication, leave
    if premise.t != '->':
        return

    # catch the left hand and right hand side
    A, B = premise.lhs, premise.rhs
    ALabel, BLabel = A.to_label(), B.to_label()
    not_ALabel, not_BLabel = ALabel+"N", BLabel+"N"

    # if I have A       and B is not in labels
    if ALabel in labels and BLabel not in labels:
        # I can use Modus Ponens to get B
        print("insert %s %s." % (BLabel, B.to_pw()))
        print("f_imp_e %s %s." % (premise.to_label(), ALabel))
        premises.add(B)
        labels.add(BLabel)

    # if I have ~B          and I dont have ~A
    if not_BLabel in labels and not_ALabel not in labels:
        # I can use Mollens Tollens to get ~A
        print("insert %s %s." % (BLabel, B.to_pw()))
        print("f_MT %s %s." % (premise.to_label(), ALabel))
        premises.add(Not(A))
        labels.add(not_ALabel)

"""
If I have a premise ~ ~ A
    Then I can extract A from it (Negative Elimination)
"""
def premise_not_not_a_simplify(labels, premises, premise):
    if not is_structure(premise, not_not_pattern):
        return

    A = premise.expr.expr
    A_label = A.to_label()

    if A_label not in labels:
        print("insert %s %s."  % (A_label, A.to_pw()))
        print("f_negneg_e %s." % premise.to_label())
        labels.add(A_label)
        premises.add(A)

"""
If I have a premise A /\ B
    Then I can extract A and B from it
"""
def premise_a_and_b_simplify(labels, premises, premise):
    if premise.t != '&':
        return

    A, B = premise.lhs, premise.rhs
    A_label, B_label = A.to_label(), B.to_label()

    if A_label not in labels:
        print("insert %s %s."  % (A_label, A.to_pw()))
        print("f_con_e1 %s." % premise.to_label())
        labels.add(A_label)
        premises.add(A)

    if B_label not in labels:
        print("insert %s %s."  % (B_label, B.to_pw()))
        print("f_con_e2 %s." % premise.to_label())
        labels.add(B_label)
        premises.add(B)

def simplify_premises(labels, premises):
    old_premises = set()
    # loop until nothing changes anymore
    # iterative because changes can affect other changes
    while len(old_premises) != len(premises):
        old_premises = set(premises)

        for premise in old_premises:
            premise_a_implies_b_simplify(labels, premises, premise)
            premise_a_and_b_simplify(labels, premises, premise)
            premise_not_not_a_simplify(labels, premises, premise)

def simplify_goal(labels, premises, goal):
    # simplify goal by removing implications and double negatives
    while True:
        # If we have a goal A -> B, we need to assume A and get to B to prove it
        if goal.t == '->':
            premise, goal = goal.lhs, goal.rhs
            print("imp_i %s." % premise.to_label())
            premises.add(premise)
            labels.add(premise.to_label())
        # If we have a goal ~~A then it suffices to show A
        elif is_structure(goal, ('~', ('~', '*'))):
            # employ negative introduction (backwards)
            print("negneg_i.")
            goal = goal.expr.expr
        else:
            return

if __name__=='__main__':
    from parse import parse
    premises = set([parse('A -> ~~B'), parse('~~~B')])
    labels = set(p.to_label() for p in premises)
    simplify_premises(labels, premises)
    print("---"*10)
    print("Premises")
    print("---"*10)
    print("\n".join(repr(p) for p in premises))
