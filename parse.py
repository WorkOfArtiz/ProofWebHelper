# EBNF:
# <statement>  =     <chain>                             |
#                    <chain> '->' <statement> ]
# <chain>      =     <expression> '\/' <chain>           |
#                    <expression> '/\' <chain>           |
# <expression> = '(' <statement> ')'                     |
#                '~' <expression>                        |
#                    <variable>
# <variable>   =     [A-Za-z_]+
#
# Example:
# A \/ ~A
# (A -> B) -> C -> A -> B -> C
#
# functions work as follows:
# (expression, last_index) <- parse function (input string)
import re
from struct import Var, Not, And, Or, Implies

def parse(string):

    # removing whitespace
    string = re.sub(r'\s+', '', string)
    statement, i = parse_statement(string)
    return statement

# <statement> =      <chain>                             |
#                    <chain> '->' <statement> ]
def parse_statement(string):
    chain, i = parse_chain(string)
    string = string[i:]
    if string != "" and string[:2] == '->':
        statement, j = parse_statement(string[2:])
        return Implies(chain, statement), i + j + 2
    return chain, i

#  <chain>   =       <expression> '\/' <expression>      |
#                    <expression> '/\' <expression>      |
def parse_chain(string):
    expression, i = parse_expression(string)
    string = string[i:]

    if string != "" and string[:2] == '\\/':
        chain, j = parse_chain(string[2:])
        return Or(expression, chain), i+j+2

    if string != "" and string[:2] == '/\\':
        chain, j = parse_chain(string[2:])
        return And(expression, chain), i+j+2

    return expression, i

# <expression> = '(' <statement> ')'                     |
#                '~' <expression>                        |
#                    <variable>
def parse_expression(string):
    if string[0] == '(':
        expression, i = parse_statement(string[1:])
        assert string[1+i] == ')'
        return expression, i + 2
    elif string[0] == '~':
        expression, i = parse_expression(string[1:])
        return Not(expression), i + 1
    else:
        variable, i = parse_variable(string)
        return (variable, i)

var = re.compile('[A-Za-z_]+')
def parse_variable(string):
    m = var.match(string)
    assert m != None
    variable = m.group()
    return Var(variable), len(variable)

if __name__ == '__main__':
    tests = [
        'A \/ ~A',
        '(~A -> B) \/ B',
        'A -> B -> C',
        '(A -> B) -> C',
        'A -> (B -> C)',
        '(()A',
        '~(A \/ C) -> ~~(C)'
    ]

    for test in tests:
        try:
            exp = parse(test)
            print("'%s' should be the same as '%s'" % (test, exp.to_pw()))
        except:
            print("Test '%s' was not well formed" % test)
