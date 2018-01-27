import sys
from datetime import date
from language.ply import lex
from language.ply import yacc
from dao.BookScriptDAO import BookScriptDAO

# ~~~~~~~~~~~~~~~~~~~~ SCANNER ~~~~~~~~~~~~~~~~~~~~~~~~ #
sys.path.insert(0, "../..")
if sys.version_info[0] >= 3:
    raw_input = input

# Token's Regex
t_STRING = r'\"[a-zA-Z0-9\W\s]*\"'
t_ignore = " \t"

admin = {
    'delete': 'DELETE',
    'create': 'CREATE',
    'return': 'RETURN'
}

reserved = {
    'goto': 'GOTO', # Good
    'view': 'VIEW', # Good
    'rent': 'RENT', # Good
    'where': 'WHERE', # Good
    'back': 'BACK', # Good
    'login': 'LOGIN', # Good
    'logout': 'LOGOUT', # Good
    'register': 'REGISTER', # Good
    'help': 'HELP', # Good
    'due': 'DUE', # Good
    'shelf': 'SHELF', # Good
    'book': 'BOOK', # Good
    'library': 'LIBRARY', # Good
    'exit': 'EXIT', # Good
    'delete': 'DELETE', # Good
    'create': 'CREATE', # Good
    'return': 'RETURN' # Good
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
         | EXIT
         | LOGOUT
         | RETURN
         | DELETE
         | CREATE
         | REGISTER
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
    print("Syntax error, please consult 'help' for details!")

# Build Parse
parser = yacc.yacc()


# ~~~~~~~~~~~~~~~~~ CODE EXECUTIONER ~~~~~~~~~~~~~~~~~~~~~ #
# System Variables
current_library = None
current_shelf_id = None
current_user = None
current_user_id = None
is_admin = True
dao = BookScriptDAO()
libraries = ['bsdb', 'border']


def run(p):
    global is_admin
    if p is None:
        print("Syntax Error")
    elif type(p) == tuple:
        if p[0] == 'GOTO':
            f_goto(p)
            return
        elif p[0] == 'RENT':
            f_rent_book(p[1])
            return
        elif p[0] == 'WHERE':
            f_find_location_book(p[1])
            return
        elif reserved.get(str(p[0]).lower()) is None:
            print("Command %s is not a valid function. Consult 'help' for more information" % p[0])
            return
        else:
            print("The Command %s is not used correctly or you do not have the correct Permission. Consult 'help' for more information" % p[0])
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
        elif p == 'REGISTER':
            f_register_user()
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
        elif p == 'RETURN':
            f_return_book()
            return
        elif is_admin and p == str("DELETE"):
            f_delete(p)
            return
        elif is_admin and p == 'CREATE':
            f_create(p)
            return
        elif reserved.get(str(p).lower()) is None:
            print("Command %s is not a valid function. Consult 'help' for more information" % p)
            return
        else:
            print("The Command %s is not used correctly. Consult 'help' for more information" % p)
            return

# ~~~~~~~~~~~~~~~~~~~~~~~~~~ VIEW ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


def f_view(p):
    global current_shelf_id
    global current_library
    global dao
    global libraries
    if p is None:
        if current_library is None:
            print("Available Libraries:\n")
            for library in libraries:
                print("\t" + library)
            print('---------------------')
        elif current_shelf_id is None:
            results = dao.getAllShelves()
            print("Available Shelves:\n")
            for shelf in results:
                print("\tShelf " + str(shelf[0]))
            print('---------------------')
        else:
            results = dao.getBooksByShelfId(current_shelf_id)
            print("Available Book:\n")
            for book in results:
                bookinfo = ""
                for args in book:
                  bookinfo+= str(args) + "|"
                print(bookinfo)
            print('---------------------')
    else:
        print("Error in view method")

# ~~~~~~~~~~~~~~~~~~  GOTO    ~~~~~~~~~~~~~~~~~~~ #


def f_goto(p):
    global current_shelf_id
    global current_library
    global dao
    global libraries
    if len(p) == 3:
        if p[1] == "LIBRARY":
            if str(p[2]).replace("\"", "").replace(" ", "").lower() in libraries:
                current_shelf_id = None
                current_library = str(p[2]).replace("\"", "").replace(" ", "").lower()
            else:
                print("Library doesnt exist")
        elif p[1] == "SHELF":
            if current_library is None:
                print("Please enter a library first!")
            else:
                if type(p[2]) != int:
                    print("Invalid Shelf")
                    return
                shelf = dao.getShelfById(int(p[2]))
                if shelf is None:
                    print("Shelf doesnt exist")
                else:
                    print(shelf[0])
                    current_shelf_id = shelf[0]
        else:
            print("Wrong entity only library or shelf permitted!")
    else:
        print("Wrong Number of inputs for command %s", p[0])

# ~~~~~~~~~~~~~~~~~~ RENT ~~~~~~~~~~~~~~~~~~~~ #


def f_rent_book(book_name):
    global dao
    global current_library
    global current_shelf_id
    global current_user_id

    if current_shelf_id is None:
        print("Please go to a shelf first to rent a book!")
    else:
        book = dao.getBookByNameAndShelfId(book_name.replace("\"", ""), current_shelf_id)
        if not book:
            print("Book given is not valid")
        else:
            day = date.today().timetuple()
            while True:
                days_rent = input("For how many days do you wish to rent the book?\n > ")
                try:
                    days_rent = int(days_rent)
                    if days_rent > 10 or days_rent <= 0:
                        print("You can only rent a book between 1 to 10 days")
                    else:
                        break
                except ValueError:
                    print("That is not a number!")

            today = str(day[1]) + '/' + str(day[2]) + '/' + str(day[0])
            new_day = day[2] + days_rent
            new_month = 0
            if day[1] == 12 or day[1] == 10 or day[1] == 8 or day[1] == 7 or day[1] == 5 or day[1] == 3 or day[1] == 1:
                if new_day > 31:
                    new_day = new_day % 31
                    new_month = 1
            elif day[1] == 11 or day[1] == 9 or day[1] == 6 or day[1] == 4:
                if new_day > 30:
                    new_day = new_day % 30
                    new_month = 1
            elif day[1] == 2:
                if new_day > 28 and day[0] % 4 != 0:
                    new_day = new_day % 28
                    new_month = 1
                elif new_day > 29 and day[0] % 4 == 0:
                    new_day = new_day % 29
                    new_month = 1

            due_day = str(day[1] + new_month) + '/' + str(new_day) + '/' + str(day[0])
            dao.rentAvailableBook(today, due_day, 'TRUE', book[0], current_user_id)
            print("Request Accepted, please go to pick up at %s.\n Thank you." % current_library)
            print("This book will be due for the day %s." % due_day)


# ~~~~~~~~~~~~~~~~~~ RETURN ~~~~~~~~~~~~~~~~~~~~ #

def f_return_book():
    global dao
    global current_user_id
    bid = input("Enter the book id you wish to return:\n")
    books = dao.getAllRentedBooksFromUser(current_user_id)
    if books is None:
        print("You dont owe books")
    else:
        book = dao.getRentedBookFromUserById(current_user_id, bid)
        if book is None:
            print("Cannot find book")
        else:
            if dao.getBookByIDAll(book):
              dao.changeBookAvailability(book,'FALSE')
              print("Book has been returned!")
            else:
              print("Book ID Not Found!")

# ~~~~~~~~~~~~~~~~~~~~~ WHERE ~~~~~~~~~~~~~~~~~~~~~~ #


def f_find_location_book(book_name):
    global current_library
    global dao
    if current_library is None:
        print("Please enter a library first to search for a book")
    else:
        list = dao.getBookByName(str(book_name).replace("\"", ""))
        if len(list) == 0:
            print("Book was not found")
        else:
            print("Found in shelves")
            for book in list:
                print(str(book[2]))
        print("-----------------------")

# ~~~~~~~~~~~~~~~ BACK ~~~~~~~~~~~~~~~~~~~~ #


def f_back():
    global current_library
    global current_shelf_id
    if current_library is None:
        print("You cant go back more")
    elif current_shelf_id is None:
        current_library = None
    else:
        current_shelf_id = None


# ~~~~~~~~~~~~~~~ LOGIN ~~~~~~~~~~~~~~~~~~~ #
def f_login():
    global current_user
    global current_user_id
    global is_admin
    global dao

    username = input("What is your username?\n > ")
    password = input("What is your password?\n > ")
    user = dao.getUserByUsernameAndPassword(username,password)
    if user is not None:
        current_user = username
        current_user_id = user[0]
        is_admin = user[1]
        print("Successfully logged in as %s!" % current_user)
    else:
        print("Account not valid account")


# ~~~~~~~~~~~~~~~~~~~~~~~~~ LOGOUT ~~~~~~~~~~~~~~~~~~~ #


def f_logout():
    global current_user
    global current_user_id
    global is_admin
    current_user = None
    current_user_id = None
    is_admin = False


# ~~~~~~~~~~~~~~~~~~~~~~~~ REGISTER ~~~~~~~~~~~~~~~~~~ #

def f_register_user():
    global current_user
    global current_user_id
    global is_admin
    global dao
    print("Please Enter the information for a new account!")
    try:
        username = input("What is your username?\n > ")
        email = input("What is your email?\n > ")
        password = input("What is your password?\n > ")
        address = input("What is your address?\n > ")
        phone = int(input("What is your number?"))
        admin_prev = False
        if is_admin:
            admin_prev = "y" == input("Does user have administrative privileges (Y/N)\n > ").lower()
        user_ID = dao.createNewUser(username,password,address,phone,email,admin_prev)
        if user_ID is not None:
            current_user = username
            current_user_id = user_ID
            is_admin = admin_prev
            print("Successfully created and logged in as %s!" % current_user)
        else:
            print("Account was not created")
    except:
        print("Invalid input, please attempt again!")

# ~~~~~~~~~~~~~~~~~~~~ HELP ~~~~~~~~~~~~~~~~~~~~~~~~~~ #


def f_help():
    global is_admin
    print("<Navigation/Location Commands>\n"
          "\tgoto <library|shelf> <Entity Name>\t\t- It navigates to the location provided\n"
          "\tback\t\t- Back to the previous location\n"
          "\tview\t\t- To see a list of the items in the current location\n"
          "\twhere <name>\t\t- Show the address of shelf or book given\n"
          "\n<User Commands>\n"
          "\tlogin\t\t- Login as user on the system\n"
          "\tlogout\t\t- Logout as user on the system\n"
          "\tregister\t\t- Register a new user on system\n"
          "\texit\t\t- A command that exits system\n"
          "\trent <name>\t\t- To rent the book with the given name\n"
          "\tdue\t\t- See all books the current user owes\n"
          "\thelp\t\t- Show the system commands and their functions\n"
          "\treturn\t\t- Lets user return a book that has due\n")
    if is_admin:
          print("<Administrator Commands>\n"
                "\tdue\t\t- See all books currently owed\n"
                "\tdelete\t\t- Delete a book\n"
                "\tcreate\t\t- Create a book\n")

# ~~~~~~~~~~~~~~~~~~~~~~~ EXIT ~~~~~~~~~~~~~~~~~~~~~~~~~ #


def f_exit():
    print("Thank you for usign Book Script! Bye!")
    exit(0)

# ~~~~~~~~~~~~~~~~~~~~ DELETE ~~~~~~~~~~~~~~~~~~~~~~~ #

def f_delete(p):
    global current_shelf
    global current_library
    global dao

    if (current_library is not None and current_shelf is not None): #This is book
        if len(p) == 2:  # p(2): Two parameters edit <NameBook>
                while True:
                    s = input("Write the id of book you want to be delete or type exit to leave:")
                    if (s.lower() == "exit"):
                        break
                    # Validate the book
                    book =  dao.getBookByID(s)
                    if book is None:
                        print("Book not found")
                    else:
                        dao.deleteBook(book_id)
                        print("Successfully Deleted Book")

        else:
            print("Command %s is not used correct, try\n\tdelete <entity>\t\t- Delete a book\n",p[0])  # Fix the sentence
    elif(current_library is not None and current_shelf is None):
        if len(p) == 2:  # p(2): Two parameters edit <NameBook>
            while True:
                s = input("Write the name of shelf you want to be delete or type exit to leave:")
                if(s.lower() == "exit"):
                    break
                # Validate the book
                book = 1  # TODO: dao.getShelfbyName(shelf_name)
                if book is None:
                    print("Bad shelf name")
                else:
                    print("%s shelf is deleted",p[1])
                    # TODO: dao.deleteShelf(shelf_id)
        else:
            print("Command %s is not used correct, try\n\tdelete <entity>\t\t- Delete a book or shelf\n", p[0])  # Fix the sentence
    else:
        print("Please enter to library and/or shelf first for able delete the book or shelf")


# ~~~~~~~~~~~~~~~~~~~~~ CREATE ~~~~~~~~~~~~~~~~~~~~~~ #

def f_create(p):
    global current_shelf
    global current_library
    global dao

    if (current_library is not None and current_shelf is not None):  # This is book
        if len(p) == 2:  # p(2): Two parameters edit <NameBook>
            while True:
                s = input("Type anything to create book or type exit to leave:")
                if (s.lower() == "exit"):
                    break
                else:
                    book = {}

                    while True:
                        s = input("Please write the name of the book")
                        if (s is not None):
                            book['bname'] = s
                            break
                        else:
                            print("Please write the name of the book")
                    while True:
                        s = input("Which type genre is? ")
                        if (s is not None):
                            book['genre'] = s
                            break
                        else:
                            print("Please write which type genre is?")
                    while True:
                        s = input("Please write the ISBN")
                        if (s is not None):
                            book['isbn'] = s
                            break
                        else:
                            print("Please write the ISBN")
                    while True:
                        s = input("Who is the author? ")
                        if (s is not None):
                            book['author'] = s
                            break
                        else:
                            print("Please write who is author?")
                    while True:
                        s = input("What is the publisher name? ")
                        if (s is not None):
                            book['publisher'] = s
                            break
                        else:
                            print("Please write what is the publisher name? ")
                    while True:
                        s = input("When the publish date is? (ex. YYYY/MM/DD)")
                        if (s is not None):
                            book['date'] = s
                            break
                        else:
                            print("Please write when the publish date is? ")

                    bid=dao.createNewBook(book['isbn'], current_shelf, book['bname'], book['genre'], book['author'], book['publisher'], book['date'])
                    print("bid:%s book is created" % bid)
        else:
            print("Command %s is not used correct, try\n\tcreate <entity>\t\t- Create a book or shelf\n",
                  p[0])  # Fix the sentence
    elif (current_library is not None and current_shelf is None):
        if len(p) == 2:  # p(2): Two parameters edit <NameBook>
            while True:
                s = input("Write the name of shelf you want to be create or type exit to leave:")
                if (s.lower() == "exit"):
                    break
                # Validate the book
                shelf = 1  # TODO: dao.getShelfbyName(book_name)
                if shelf is not None:
                    print("Shelf name already exist, please pick another new name")
                else:
                    shelf = 1 # TODO: dao.addShelfBook(book_name)
                    print("%s shelf is created",p[1])
        else:
            print("Command %s is not used correct, try\n\tcreate <entity>\t\t- Create a book or shelf\n",
                  p[0])  # Fix the sentence
    else:
        print("Please enter to library and/or shelf first for able create the book or shelf")


# ~~~~~~~~~~~~~~~~~~~~~~~~~ DUE ~~~~~~~~~~~~~~~~~~~~ #
def f_due():
    global is_admin
    global current_user_id
    due_books = []
    if is_admin:
      due_books = dao.getAllRentedBooks()
    else:
      due_books = dao.getAllRentedBooksFromUser(current_user_id)

    if due_books is None:
        print("No books are due!")
    else:
        print("Books currently due:\n")
        for entry in due_books:
            line = ""
            for fields in entry:
                line += str(fields) + "|"
            print(line)
    print("------------------------------------------")

# ~~~~~~~~~~~~~~~~~ Input Handler ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


def run_code():
    global current_shelf_id
    global current_library
    global current_user

    if current_user is None:
        s = input("Do you want to register an account? (Y/N) or EXIT\n > ")
        if "y" == s.lower():
            s = "register"
        elif "exit" == s.lower():
            s = "exit"
        else:
            s = "login"
    elif current_library is None:
        s = input(current_user + ' > ')
    elif current_shelf_id is None:
        s = input(current_user + ' / ' + current_library + ' > ')
    else:
        s = input(current_user + ' / ' + current_library + '/Shelf' + str(current_shelf_id) + ' > ')

    parser.parse(s)
