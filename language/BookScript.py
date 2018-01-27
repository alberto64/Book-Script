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
    'edit': 'EDIT',
    'delete': 'DELETE',
    'create': 'CREATE',
    'return': 'RETURN'
}

reserved = {
    'goto': 'GOTO',
    'view': 'VIEW',
    'rent': 'RENT',
    'where': 'WHERE',
    'back': 'BACK',
    'login': 'LOGIN',
    'logout': 'LOGOUT',
    'register': 'REGISTER',
    'help': 'HELP',
    'sort': 'SORT',
    'due': 'DUE',
    'shelf': 'SHELF',
    'book': 'BOOK',
    'library': 'LIBRARY',
    'exit': 'EXIT'
}

tokens = [
  'VARIABLE',
  'INTEGER',
  'STRING',
] + list(reserved.values()) + list(admin.values())


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
         | EDIT
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
is_admin = False
sort = "Ascending"
dao = BookScriptDAO()
libraries = ['bsdb', 'border']


def run(p):
    global is_admin
    global reserved
    global admin
    print(p)
    if type(p) == tuple:
        if p[0] == 'GOTO':
            f_goto(p)
            return
        elif p[0] == 'RENT':
            f_rent_book(p[1])
            return
        elif p[0] == 'WHERE':
            f_find_location_book(p[1])
            return
        elif p[0] == 'SORT':
            f_sort(p[1])
            return
        elif admin.get(str(p[0]).lower()) is not None:
            if is_admin:
                if p[0] == 'EDIT':
                    f_edit(p)
                    return
                elif p[0] == 'DELETE':
                    f_delete(p)
                    return
                elif p[0] == 'CREATE':
                    f_create(p)
                    return
                elif p[0] == 'RETURN':
                    f_return_book(p)
                    return
            else:
                print("Permission Denied, this is only administration commands")
        elif reserved.get(str(p[0]).lower()) is None:
            print("Command %s is not a valid function. Consult 'help' for more information" % p[0])
        else:
            print("The Command %s is not used correctly. Consult 'help' for more information" % p[0])
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
        elif p == 'SORT':
            f_sort(None)
            return
        elif reserved.get(str(p).lower()) is None:
            print("Command %s is not a valid function. Consult 'help' for more information" % p)
        else:
            print("The Command %s is not used correctly. Consult 'help' for more information" % p)
            return

# ~~~~~~~~~~~~~~~~~~~~~~~~~~ VIEW ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


def f_view(p):
    global current_library
    global current_shelf_id
    global dao
    global libraries
    if p is None:
        if current_library is None:
            print("Available Libraries:\n")
            for library in libraries:
                print("\t" + library)
            print('---------------------')

        elif current_shelf is None:
            print("")
            results = dao.getAllShelves()
            print("Available Shelves:\n")
            for shelf in results:
                print("\t" + shelf)
            print('---------------------')
        else:
            results = dao.getBooksByShelfId(current_shelf_id)
            print("Available Shelves:\n")
            for book in results:
                bookinfo = ""
                for args in book:
                    bookinfo += args + " "
                print(bookinfo)
            print('---------------------')
    else:
        print("Error in view method")


# ~~~~~~~~~~~~~~~~~~  GOTO    ~~~~~~~~~~~~~~~~~~~ #


def f_goto(p):
    global current_shelf_id
    global current_library
    global dao
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
                shelf = dao.getShelfById(p[2])
                if shelf is None:
                    print("Bad shelf id")
                else:
                    current_shelf_id = shelf
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

    if current_shelf is None:
        print("Please go to a shelf first to rent a book!")
    else:
        book = dao.getBookByNameAndShelfId(book_name, current_shelf_id)
        if book is None:
            print("Book given is not valid")
        else:
            day = date.today().timetuple()
            while True:
                days_rent = input("For how many days do you wish to rent the book?\n > ")
                try:
                    days_rent = int(days_rent)
                    if days_rent > 60 or days_rent <= 0:
                        print("You can only rent a book between 1 to 60 days")
                    else:
                        break
                except ValueError:
                    print("That is not a number!")
            today = str(day[1]) + '/' + str(day[2]) + '/' + str(day[0])
            due_day = str(day[1]) + '/' + str(day[2] + days_rent) + '/' + str(day[0])
            dao.rentAvailableBook(today, due_day, True, book[0], current_user_id)

            print("Request Accepted, please go to pick up at %s.\n Thank you." % current_library)
            print("This book will be due for the day %s." % due_day)


# ~~~~~~~~~~~~~~~~~~ RETURN ~~~~~~~~~~~~~~~~~~~~ #

def f_return_book(p):
    global dao
    if len(p) == 3:
        due_book = dao.getDueBook(str(p[1]).replace("\"", ""). lower(), p[2])
        if due_book is None:
            print("You dont owe that book")
        else:
            dao.changeBookAvilability(p[2], False)
    else:
        print("Wrong number of inputs")
# ~~~~~~~~~~~~~~~~~~~~~ WHERE ~~~~~~~~~~~~~~~~~~~~~~ #


def f_find_location_book(book_name):
    global current_library
    global dao
    if current_library is None:
        print("Please enter a library first to search for a book")
    elif current_shelf is None:
        shelfs = dao.getShelfByBook(str(book_name).replace("\"", "").replace(" ", "").lower())
        print("The Book %s is on:" % book_name)
        for shelf in shelfs:
            print("\tShelf %d " % shelf)
    else:
        print("Exit the shelf to look for a book")

# ~~~~~~~~~~~~~~~~~ SORT ~~~~~~~~~~~~~~~~~~~#


def f_sort(p):
    global sort
    if p is None or p == "Ascending":
        sort = "Ascending"
    elif p == "Chronological":
        sort = "Chronological"
    elif p == "Decending":
        sort = "Decending"
    elif p == "Genre":
        sort = "Genre"
    else:
        print("Bad sort selection")
        return
    print("Sorting way is now %s" % sort)

# ~~~~~~~~~~~~~~~ BACK ~~~~~~~~~~~~~~~~~~~~ #


def f_back():
    global current_library
    global current_shelf_id
    if current_library is None:
        print("You cant go back more")
    elif current_shelf_id is None:
        current_library = None
    else:
        current_shelf = None


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
    global current_user_id
    global current_user
    global is_admin
    current_user_id = None
    current_user = None
    is_admin = False


# ~~~~~~~~~~~~~~~~~~~~~~~~ REGISTER ~~~~~~~~~~~~~~~~~~ #

def f_register_user():
    global current_user
    global current_user_id
    global is_admin
    print("Please Enter the information for a new account!")
    username = input("What is your username?\n > ")
    email = input("What is your email?\n > ")
    password = input("What is your password?\n > ")
    address = input("What is your address?\n > ")
    phone = input("What is your number?\n > ")
    admin_prev = False
    if is_admin:
        admin_prev = "y" == input("Does user have administrative privileges (Y/N)\n > ").lower()
    user_ID = dao.createNewUser(username, password, address, phone, email, admin_prev)
    if user_ID is not None:
        current_user = username
        current_user_id = user_ID
        is_admin = admin_prev
        print("Successfully created and logged in as %s!" % current_user)
    else:
        print("Account was not created")

# ~~~~~~~~~~~~~~~~~~~~ HELP ~~~~~~~~~~~~~~~~~~~~~~~~~~ #


def f_help():
    global is_admin
    print("<Navigation/Location Commands>\n"
          "\t* Optional Inputs\n"
          "\tgoto <library|shelf> <Entity Name>\t\t- It navigates to the location provided\n"
          "\tback\t\t- Back to the previous location\n"
          "\tview [*<library|shelf> <Entity Name>]\t\t- To see a list of the items in the current location "
          "or see those under the current location\n"
          "\tSort <Type>\t\t- Configure type of sorting (By: Chronological, Ascending, Descending, Genre)\n"
          "\twhere <name>\t\t- Show the address of shelf or book given\n"
          "\n<User Commands>\n"
          "\tlogin\t\t- Login as user on the system\n"
          "\tlogout\t\t- Logout as user on the system\n"
          "\texit\t\t- A command that exits system\n"
          "\trent <name>\t\t- To rent the book with the given name\n"
          "\tdue\t\t- See all books the current user owes\n"
          "\thelp\t\t- Show the system commands and their functions\n")
    if is_admin:
          print("<Administrator Commands>\n"
                "\tedit <\"Info\"|\"Loc\">\t\t-Edit a book information or location\n"
                "\tdelete <entity>\t\t- Delete a book or shelf\n"
                "\tcreate <entity>\t\t- Create a book or shelf\n"
                "\treturn\t\t- Lets user return a book that has due\n")

# ~~~~~~~~~~~~~~~~~~~~~~~ EXIT ~~~~~~~~~~~~~~~~~~~~~~~~~ #


def f_exit():
    print("Thank you for usign Book Script! Bye!")
    exit(0)

# ~~~~~~~~~~~~~~~~~~~~ EDIT ~~~~~~~~~~~~~~~~~~~~~~~~~ #

def f_edit(p):
    global current_shelf
    global current_library
    global dao

    if(current_library is not None and current_shelf is not None):
        if len(p) == 2: #p(2): Two parameters edit <NameBook>
            #Validate the book
            book = 1  # TODO: dao.getBookbyName(book_name)
            if book is None:
                print("Bad book name")
            else:
                while True:
                    s = input("Which do you want to modify: \"Name\", \"Author\", \"Genre\", \"Publisher\" or \"Publish_Date\"? or type exit to leave")
                    if s.lower() == "name":
                        while True:
                            s = input("Write new name: ")
                            if (s is not None):
                                book[3] = s
                                print("Name book modified")
                                break
                            else:
                                print("Please write new name")
                    elif s.lower() == "author":
                        while True:
                            s = input("Write new author: ")
                            if (s is not None):
                                book[5] = s
                                print("Author modified")
                                break
                            else:
                                print("Please write new author")
                    elif s.lower() == "genre":
                        while True:
                            s = input("Write new genre: ")
                            if (s is not None):
                                book[4] = s
                                print("Genre modified")
                                break
                            else:
                                print("Please write new genre")
                    elif s.lower() == "publisher":
                        while True:
                            s = input("Write new publisher: ")
                            if (s is not None):
                                book[6] = s
                                print("Publisher modified")
                                break
                            else:
                                print("Please write new publisher")
                    elif s.lower() == "publish_date":
                        while True:
                            s = input("Write new publish date: ")
                            if (s is not None):
                                book[7] = s
                                print("Publish date modified")
                                break
                            else:
                                print("Please write new publish date")
                    elif s.lower() == "exit":
                        print("Book Modification is done")
                        break
                    else:
                        print("Invalid options, try again")
        else:
            print("Command %s is not used correct, try\n\tedit <Info>\t\t-Edit a book information",p[0]) #Fix the sentence
    else:
        print("Please enter to library and/or shelf first to be able modify the book") #Editing here


# ~~~~~~~~~~~~~~~~~~~~ DELETE ~~~~~~~~~~~~~~~~~~~~~~~ #

def f_delete(p):
    global current_shelf
    global current_library
    global dao

    if (current_library is not None and current_shelf is not None): #This is book
        if len(p) == 2:  # p(2): Two parameters edit <NameBook>
                while True:
                    s = input("Write the name of book you want to be delete or type exit to leave:")
                    if (s.lower() == "exit"):
                        break
                    # Validate the book
                    book = 1  # TODO: dao.getBookbyName(book_name)
                    if book is None:
                        print("Bad book name")
                    else:
                        print("")
                        # TODO: dao.deleteBook(book_id)
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
                s = input("Write the name of book you want to be create or type exit to leave:")
                if (s.lower() == "exit"):
                    break
                # Validate the book
                book = 1  # TODO: dao.getBookbyName(book_name)
                if book is not None:
                    print("Book name already exist, please pick another new name")
                else:
                    book = 1 # TODO: dao.addNewBook(book_name)
                    while True:
                        s = input("Which type genre is? ")
                        if (s is not None):
                            book[4] = s
                            break
                        else:
                            print("Please write which type genre is?")
                    while True:
                        s = input("Who is the author? ")
                        if (s is not None):
                            book[5] = s
                            break
                        else:
                            print("Please write who is author?")
                    while True:
                        s = input("What is the publisher name? ")
                        if (s is not None):
                            book[6] = s
                            break
                        else:
                            print("Please write what is the publisher name? ")
                    while True:
                        s = input("When the publish date is?")
                        if (s is not None):
                            book[7] = s
                            break
                        else:
                            print("Please write when the publish date is? ")
                    print("%s book is created",p[1])
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
    global dao
    if is_admin:
        due_books = dao.getAllRentedBooks()
    else:
        due_books = dao.getAllRentedBooksFromUser(current_user_id)
    print("Current Due Books:")
    for entry in due_books:
        print("\t" + entry[0] + " " + entry[1] + " " + entry[2] + " " + entry[3] + " " + entry[4] + " " + entry[5])
    print("-----------------------------")

# ~~~~~~~~~~~~~~~~~ Input Handler ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


def run_code():
    global current_shelf
    global current_library
    global current_user
    # current_library = "Borders"

    if current_user is None:
        s = input("Do you want to register an account? (Y/N)\n > ")
        if "y" == s.lower():
            s = "register"
        else:
            s = "login"
    elif current_library is None:
        s = input(current_user + ' > ')
    elif current_shelf is None:
        s = input(current_user + ' / ' + current_library + ' > ')
    else:
        s = input(current_user + ' / ' + current_library + '/Shelf' + str(current_shelf) + ' > ')

    parser.parse(s)
