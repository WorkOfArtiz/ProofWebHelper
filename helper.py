"""
IMPORTS
"""
import sys
from struct import is_structure
from simplify import simplify_goal, simplify_premises
from parse import parse

"""
COMMAND LINE ARGUMENT PARSING / DEBUG
"""
args = sys.argv[1:]

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
goal = parse(statement)
premises = set()
labels = set()

#Simplifying the goal and the premises (the goal usually provides in statements).
simplify_goal(labels, premises, goal)
simplify_premises(labels, premises)

# If the goal was reached upon expanding the premises
if goal.to_label() in labels:
    print("exact %s." % goal.to_label())
print("Qed.")

print("(*")
print("Premises proved: ")
for premise in premises:
    print("    %s" % premise.to_pw())
print("*)")
