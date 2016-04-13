"""
IMPORTS
"""
import sys
from struct import is_structure
from parse import parse

"""
COMMAND LINE ARGUMENT PARSING / DEBUG
"""
args = ['example.proof']
#args = sys.argv[1:]

if '-h' in args or '--help' in args:
    print('Usage:')
    print('python helper.py ... --help ...    for help')
    print('python helper.py ...  -h    ...    for help')
    print('<command> | python helper.py       for stdin input')
    print('python helper.py <filename>        for file input')
    exit(0)

# if no files are given
input_stream = open(args[0]) if args else sys.stdin

"""
READING INPUT
"""
for line in input_stream:
    line = line.strip()
    if line.startswith('Theorem'):
        print(line)
        print('Proof.')
        statement = line.split(":")[1].strip()[:-1]
    elif line == 'Proof.' or line == 'Qed.':
        pass
    else:
        print(line)

"""
ACTUAL PARSING / PROGRAM
"""
statement = parse(statement)
premises = []

while statement.t == '->':
    premises.append(statement.lhs)
    print("imp_i %s." % statement.lhs.to_label())
    statement = statement.rhs


and_pattern = ('&', '*', '*')            # an AND in the premises is very annoying
double_neg_pattern = ('~', ('~', '*'))   # double negative checks, prem and res

# looping through the premises looking for patterns
todo = premises                          # I'll use this as stack
premises = []                            # I'll fill this by emptying the stack
labels = set(p.to_label() for p in todo) # Labels can't be made double

while todo:
    item = todo.pop()


    # Here some auto magic stuff is done to preprocess the premises
    if is_structure(item, double_neg_pattern):
        new_premise = item.expr.expr
        new_label = new_premise.to_label()

        if new_label in labels:
            premises.append(item)
            continue

        print("insert %s %s." % (new_label, new_premise.to_pw()))
        print("f_negneg_e %s." % item.to_label())
        labels.add(new_label)
        todo.append(new_premise)

    elif is_structure(item, and_pattern):
        prem_l, prem_r = item.lhs, item.rhs
        label_l, label_r = prem_l.to_label(), prem_r.to_label()

        if label_l not in labels:
            print("insert %s %s." % (prem_l.to_label(), prem_l.to_pw()))
            print("f_con_e1 %s." % item.to_label())
            labels.add(label_l)
            todo.append(prem_l)
        else:
            premises.append(item)

        if label_r not in labels:
            print("insert %s %s." % (prem_r.to_label(), prem_r.to_pw()))
            print("f_con_e2 %s." % item.to_label())
            labels.add(label_r)
            todo.append(prem_r)
        else:
            premises.append(item)
    else:
        premises.append(item)

# if statement is double negative
if is_structure(statement, double_neg_pattern):
    # employ negative introduction (backwards)
    print("negneg_i.")
    statement = statement.expr.expr

# Since Im feeling like whatever, it will automatically solve trivial proofs
if statement.to_label() in labels:
    print("exact %s." % statement.to_label())

# print("Premises:")
# for premise in premises:
#     print(premise)
# print("Proof this:")
# print(statement.__repr__())
