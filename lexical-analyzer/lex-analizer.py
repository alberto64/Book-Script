# -----------------------------------------------------------------------------
# lex-analizer.py
#
# -----------------------------------------------------------------------------

import sys
import ply.lex as lex
import ply.yacc as yacc

sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input

reserved = {
    'goto': 'GOTO',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'view': 'VIEW',
    'rent': 'RENT',
    'where': 'WHERE',
    'back': 'BACK',
    'login': 'LOGIN',
    'help': 'HELP',
    'sort': 'SORT',
    'due': 'DUE',
    'reversed': 'REVERSE',
    'edit': 'EDIT',
    'add': 'ADD',
    'delete': 'DELETE',
    'create': 'CREATE'
}


tokens = [
    'VARIABLE', 'INTEGER', 'FLOAT', 'PERIOD', 'STRING', 'CHAR', 'EQUAL', 'NEQUAL', 'LPAREN', 'RPAREN', 'COMMENT'
] + list(reserved.values())

# Tokens

t_STRING = r'\"[a-zA-Z0-9\W\s]*\"'
t_ignore = " \t"
t_PERIOD = r'\.'
t_CHAR = r'\'(\s|\S)?\''
t_EQUAL = r'=='
t_NEQUAL = r'!='
t_LPAREN = r'('
t_RPAREN = r')'
t_ignore_COMMENT = r'\#.*'


def t_VARIABLE(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'VARIABLE')    # Check for reserved words
    return t


def t_FLOAT(t):
    r'[-+]?((\d+\.\d*)|(\d*\.\d+))'
    t.value = float(t.value)
    return t


def t_INTEGER(t):
    r'[-+]?\d+'
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lex.lex()

# Parsing rules
""""
precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
)

# dictionary of names
names = {}


def p_statement_assign(p):
    'statement : VARIABLE "=" expression'
    names[p[1]] = p[3]


def p_statement_expr(p):
    'statement : expression'
    print(p[1])


def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]


def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = -p[2]


def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]


def p_expression_integer(p):
    "expression : INTEGER"
    p[0] = p[1]


def p_expression_float(p):
    "expression : FLOAT"
    p[0] = p[1]


def p_expression_variable(p):
    "expression : VARIABLE"
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

yacc.yacc()
"""
while 1:
    try:
        s = input('LEX > ')
    except EOFError:
        break
    if not s:
        continue
    lex.input(s)
    while True:
        tok = lex.token()
        if not tok:
            break  # No more input
        print(tok)
