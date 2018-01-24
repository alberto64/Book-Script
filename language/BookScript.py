import sys
from language.ply import lex
from language.ply import yacc


sys.path.insert(0, "../..")
if sys.version_info[0] >= 3:
    raw_input = input

# Token's Regex

t_STRING = r'\"[a-zA-Z0-9\W\s]*\"'
t_ignore = " \t"
t_VIEW = r'view/i'
t_GOTO = r'goto/i'
t_SHELF = r'shelf/i'
t_BOOK = r'book/i'
t_LIBRARY = r'library/i'
t_WHERE = r'where/i'
t_DUE = r'due/i'
t_BACK = r'back/i'
t_RENT = r'rent/i'

#System Variables
current_shelf = None
current_admin = None
current_library = None

reserved = {
    'goto': 'GOTO',
    # 'then': 'THEN',
    # 'else': 'ELSE',
    # 'while': 'WHILE',
    'view': 'VIEW',
    'rent': 'RENT',
    'where': 'WHERE',
    'back': 'BACK',
    'login': 'LOGIN',
    # 'help': 'HELP',
    # 'sort': 'SORT',
    'due': 'DUE',
    # 'reversed': 'REVERSE',
    # 'edit': 'EDIT',
    # 'add': 'ADD',
    # 'delete': 'DELETE',
    # 'create': 'CREATE',
    'shelf': 'SHELF',
    'book': 'BOOK',
    'library': 'LIBRARY'
}

tokens = [
  'VARIABLE',
  'INTEGER',
  # 'FLOAT',
  # 'PERIOD',
  'STRING',
  # 'CHAR',
  # 'EQUAL',
  # 'NEQUAL',
  # 'LPAREN',
  # 'RPAREN',
  # 'COMMENT'
] + list(reserved.values())

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

lex.lex()

# Parsing rules

def p_start(p):

    """
    start : statement
          | variable
          | empty
    """
    run(p[1])

def p_statement(p):

    """
    statement : verb entity STRING
              | verb entity INTEGER
              | verb entity
              | verb STRING
              | verb
    """
    if len(p) == 4:
        p[0] = (p[1], p[2], p[3])
    elif len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = (p[1])

def p_verb(p):

    """
    verb : VIEW
         | GOTO
         | WHERE
         | RENT
         | LOGIN
         | DUE
         | BACK
    """
    p[0] = p[1].upper()

def p_entity(p):

    """
    entity : SHELF
           | BOOK
           | LIBRARY
    """

    p[0] = p[1].upper()

def p_variable(p):
    """
    variable : VARIABLE
    """
    p_error(p)

def p_empty(p):

    """
    empty :
    """
    p[0] = None

def p_error(p):
    print("Syntax error found!")

# Build Parse
parser = yacc.yacc()

def run(p):
    global current_library
    global current_admin
    global current_shelf
    if type(p) == tuple:
        if p[0] == 'VIEW':
            if p[1] == 'SHELF':
                f_view_shelf_content(p[2])
                return
        elif p[0] == 'GOTO':
            if p[1] == 'SHELF':
                current_shelf = p[2]
                return
        elif p[0] == 'RENT':
            if current_shelf == None:
                print("Please goto a shelf first to rent a book!")
                return
            else:
                f_rent_book(p[1])
                return

        elif p[0] == 'WHERE':
            f_find_location_book(p[1])
            return

        print("ERROR!")
        return

    else:
        if p == 'BACK':
            current_shelf = None
            return
        elif p == 'VIEW':
            if current_shelf == None:
                f_view_library_content()
                return
            else:
                f_view_shelf_content(current_shelf)
                return


        elif p == 'LOGIN':
            f_login()
            return
        elif p == 'DUE':
            if current_admin == None:
                pass
            else:
                if current_shelf == None:
                    print("Please goto a shelf first to view all rented books!")
                    return
                else:
                    f_view_rented_books()
                    return

        return

def f_view_shelf_content(shelf_id):
    # Testing
    content = list()
    content.append("Harry Potter and the Prisoner of Azkaban")
    content.append("Harry Potter pelao")
    print("Books in Shelf %s:" % shelf_id)
    for part in content:
        print("\t%s" % part)

def f_view_library_content():
    # Testing
    content = list()
    content.append(5)
    content.append(2)
    print("Shelves in Library %s" % current_library)
    for shelf in content:
        print("\tShelf %d" % shelf)

def f_find_location_book(book_name):
    # Testing Purposes
    shelves = list()
    shelves.append(5)
    shelves.append(7)

    print("Book %s is found in:" % book_name)
    for shelf in shelves:
        print("\tShelf %d" % shelf)

def f_rent_book(book_name):
    id_number = input("What is your id number?\n > ")
    password = input("What is your password?\n > ")
    # Validate and update Data Base
    print("Request Accepted, please go to pick up at %s.\n Thank you." % current_library)

def f_login():
    username = input("What is your username?\n > ")
    password = input("What is your password?\n > ")
    current_admin = username
    print("Successfully logged in as %s!" % current_admin)

def f_view_rented_books():
    rented = []
    rented.append(
    """
    Manuel A. Baez, 812-45-7890, “Almanaque Mundial 2016”, November 6, 2017
    """
    )
    rented.append(
    """
    Alberto J. De Jesus, 813-67-8907, “100 años De Soledad”, November 8, 2017
    """
    )
    for record in rented:
        print(record)

def run_code():
    global current_shelf
    global current_library
    global current_admin

    current_library = "Borders"
    if current_library == None:
        s = input(' | > ')
    elif current_shelf == None:
        s = input(' | ' + current_library + ' > ')
    else:
        s = input(' | ' + current_library + '/Shelf' + str(current_shelf) + ' > ')

    parser.parse(s)
    return s

