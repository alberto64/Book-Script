import sys
from language.ply import lex
from language.ply import yacc

# ~~~~~~~~~~~~~~~~~~~~ SCANNER ~~~~~~~~~~~~~~~~~~~~~~~~ #
sys.path.insert(0, "../..")
if sys.version_info[0] >= 3:
    raw_input = input

# Token's Regex
t_STRING = r'\"[a-zA-Z0-9\W\s]*\"'
t_ignore = " \t"

reserved = {
    'goto': 'GOTO',
    'view': 'VIEW',
    'rent': 'RENT',
    'return': 'RETURN',
    'where': 'WHERE',
    'back': 'BACK',
    'login': 'LOGIN',
    'logout': 'LOGOUT',
    'help': 'HELP',
    'sort': 'SORT',
    'due': 'DUE',
    # 'reversed': 'REVERSE',
    # 'edit': 'EDIT',
    # 'add': 'ADD',
    # 'delete': 'DELETE',
    # 'create': 'CREATE',
    'shelf': 'SHELF',
    'book': 'BOOK',
    'library': 'LIBRARY',
    'exit': 'EXIT'
}

tokens = [
  'VARIABLE',
  'INTEGER',
  'STRING',
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

# ~~~~~~~~~~~~~~~~~~~~~ PARSER ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
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
         | HELP
         | SORT
         | EXIT
         | LOGOUT
         | RETURN
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


# ~~~~~~~~~~~~~~~~~ CODE EXECUTIONER ~~~~~~~~~~~~~~~~~~~~~ #
# System Variables
current_shelf = None
is_admin = False
current_library = None
current_user = None

def run(p):
    global current_library
    global current_admin
    global current_shelf
    print(p)
    if type(p) == tuple:
        if p[0] == 'VIEW':
            f_view(p)
            return
        elif p[0] == 'GOTO':
            f_goto(p)
            return
        elif p[0] == 'RENT':
            f_rent_book(p[1])
            return
        elif p[0] == 'RETURN':
            f_return_book(p[1])
            return
        elif p[0] == 'WHERE':
            f_find_location_book(p[1])
            return
        elif p[0] == 'SORT':
            f_sort(p[1])
            return
    else:
        if p == 'BACK':
            f_back()
            return
        elif p == 'VIEW':
            f_view(None)
            return
        elif p == 'LOGIN':
            f_login()
            return
        elif p == 'LOGOUT':
            f_logout()
            return
        elif p == 'HELP':
            f_help()
            return
        elif p == 'EXIT':
            f_exit()
            return
        elif p == 'DUE':
            f_due()
            return
        elif p == 'SORT':
            f_sort(None)
            return
        else:
            print("Normal Error")
            return
    print("Execution Error")
    return

# ~~~~~~~~~~~~~~~~~~~~~~~~~~ VIEW ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


def f_view(p):
    global current_shelf
    global current_library
    if p is None:
        if current_library is None:
            f_view_libraries()
        elif current_shelf is None:
            f_view_shelfs(None)
        else:
            f_view_shelf_content(current_shelf)
    elif len(p) == 2:
        if p[1] == 'SHELF':
            f_view_shelfs(None)
        elif p[1] == 'LIBRARY':
            f_view_libraries()
        elif f_is_library_name(p[1]):
            f_view_shelfs(p[1])
        else:
            p_error(p)
    elif len(p) == 3:
        if p[1] == 'SHELF':
            f_view_shelf_content(p[2])
        else:
            p_error(p)
    else:
        print("Error in view method")


def f_is_library_name(s):
    print("Checks if %s is a library" % s)
    return type(s) == str


def f_view_libraries():
    print("Query for libraries available")
    # Query for libraries in system


def f_view_shelfs(s):
    global current_library
    if current_library is None:
        if s is None:
            print("To view shelfs please enter a library or enter a library name")
        else:
            print("Query for shelfs in library: %s " % s)
    else:
        print("Query for shelfs in library: %s " % current_library)


def f_view_shelf_content(shelf_id):
    global current_library
    if current_library is None:
        print("Please enter a library first to view a shelf")
    elif shelf_id is None:
        print("Please give a shelf ID")
    elif f_is_shelf(shelf_id):
        print("Get values")
        print("Books in Shelf %s:" % shelf_id)
    else:
        print("Please enter a valid ID")


def f_is_shelf(shelf_id):
    print("Checks if it exits the Shelf ID")
    return type(shelf_id) == int

# ~~~~~~~~~~~~~~~~~~  GOTO    ~~~~~~~~~~~~~~~~~~~ #


def f_goto(p):
    global current_shelf
    global current_library
    if current_library is None:
        if f_is_library_name(p[1]):
            current_library = str(p[1]).replace("\"", "")
        else:
            print("Bad library name")
    elif current_shelf is None:
        if p[1] == 'SHELF' and len(p) == 3:
            if f_is_shelf(p[2]):
                current_shelf = p[2]
            else:
                print("Bad ID")
        else:
            print("Wrong entity")
    else:
        p_error(p)

# ~~~~~~~~~~~~~~~~~~ RENT ~~~~~~~~~~~~~~~~~~~~ #


def f_rent_book(book_name):
    if current_shelf is None:
        print("Please goto a shelf first to rent a book!")
        return
    else:
        if f_is_book(book_name):
            # Validate and update Data Base
            if f_is_book_available(book_name):
                f_add_book_to_due(book_name)
                f_book_unavailable(book_name)
                print("Request Accepted, please go to pick up at %s.\n Thank you." % current_library)
            else:
                print("Book is not available")
        else:
            print("Please enter a valid book")


def f_add_book_to_due(book_name):
    print("Adds book to users due list")

def f_is_book(book_name):
    print("Checks if book exits in shelf")
    return True


def f_is_book_available(book_name):
    print("Checks if book can be checked out")
    return True


def f_book_unavailable(book_name):
    print("Removes book back to the shelf")

# ~~~~~~~~~~~~~~~~~~ RETURN ~~~~~~~~~~~~~~~~~~~~ #


def f_return_book(book_name):
    if f_is_due():
        if f_is_book(book_name):
            f_remove_book_user(book_name)
            f_book_available(book_name)
        else:
            print("Book doesnt exist")
        return
    else:
        print("You dont have any due books")

def f_is_due():
    global current_user
    print("Check if user owes any books")
    return True

def f_remove_book_user(book_name):
    global current_user
    print("Update users due books")


def f_book_available(book_name):
    print("Adds book back to the shelf")

# ~~~~~~~~~~~~~~~~~~~~~ WHERE ~~~~~~~~~~~~~~~~~~~~~~ #


def f_find_location_book(book_name):
    global current_library
    global current_shelf
    if current_library is None:
        print("Please enter a library first to search for a book")
    elif current_shelf is None:
        f_book_location(book_name)
    elif f_book_in_shelf(book_name):
        print("True")
    else:
        print("False")


def f_book_location(book_name):
    print("Search book in whole library")


def f_book_in_shelf(book_name):
    print("Check if book in current shelf")
    return True


# ~~~~~~~~~~~~~~~~~ SORT ~~~~~~~~~~~~~~~~~~~#

def f_sort(p):
    if p is None or p == "Ascending":
        f_sort_data("Ascending")
        print("Default is ascending order by book name")
    elif p == "Chronological":
        f_sort_data("Chronological")
        print("Sort books by chronological")
    elif p == "Decending":
        f_sort_data("Decending")
        print("Sort books by Decending")
    else:
        print("Bad sort selection")


def f_sort_data(sort_type):
    print("Sort data base by %s " % sort_type)

# ~~~~~~~~~~~~~~~ BACK ~~~~~~~~~~~~~~~~~~~~ #


def f_back():
    global current_library
    global current_shelf
    if current_library is None:
        print("You cant go back more")
    elif current_shelf is None:
        current_library = None
    else:
        current_shelf = None

# ~~~~~~~~~~~~~~~ LOGIN ~~~~~~~~~~~~~~~~~~~ #
def f_login():
    global current_user
    global is_admin

    username = input("What is your username?\n > ")
    password = input("What is your password?\n > ")
    if f_account_exists(username, password):
        current_user = username
        is_admin = f_is_admin(username)
        print("Successfully logged in as %s!" % current_user)
    else:
        print("None valid account")





def f_account_exists(username, password):
    print("Checks if the comb of both user and pass exists")
    return True


def f_is_admin(username):
    print("Checks if user is admin")
    return True

# ~~~~~~~~~~~~~~~~~~~~~~~~~ LOGOUT ~~~~~~~~~~~~~~~~~~~ #


def f_logout():
    global current_user
    global is_admin
    current_user = None
    is_admin = False

# ~~~~~~~~~~~~~~~~~~~~ HELP ~~~~~~~~~~~~~~~~~~~~~~~~~~ #


def f_help():
    print("Documentation")

# ~~~~~~~~~~~~~~~~~~~~~~~ EXIT ~~~~~~~~~~~~~~~~~~~~~~~~~ #


def f_exit():
    print("Thank you for usign Book Script! Bye!")
    exit(0)


# ~~~~~~~~~~~~~~~~~~~~~~~~~ DUE ~~~~~~~~~~~~~~~~~~~~ #
def f_due():
    if is_admin:
        if current_library is None:
            print("Please enter a library first")
        else:
            f_all_books_due()
    else:
            f_books_due()


def f_all_books_due():
    global current_library
    if current_library is None:
        print("Please enter a library to see rented books")
    else:
        print("Query all rented books ")

def f_books_due():
    global current_user
    print("Print all of the users due books")
# ~~~~~~~~~~~~~~~~~ Input Handler ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


def run_code():
    global current_shelf
    global current_library
    global current_user
    # current_library = "Borders"

    if current_user is None:
        s = "login"
    elif current_library is None:
        s = input(' | ' + current_user + ' > ')
    elif current_shelf is None:
        s = input(' | ' + current_user + ' / ' + current_library + ' > ')
    else:
        s = input(' | ' + current_user + ' / ' + current_library + '/Shelf' + str(current_shelf) + ' > ')

    parser.parse(s)
