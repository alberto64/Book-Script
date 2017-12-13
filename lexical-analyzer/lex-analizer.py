# -----------------------------------------------------------------------------
# lex-analizer.py
#
# -----------------------------------------------------------------------------
import ply.lex as lex
import ply.yacc as yacc
import sys

tokens = [
    'VARIABLE', 'COMMAND', 'STRING', 'NUMBER'
]


# Tokens
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'


