import sys
import ply.lex as lex
import ply.yacc as yacc


class BookScript:
    # Lists
    reserved = list()
    tokens = list()

    # Parser Object
    parser = None
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
    def __init__(self):
        sys.path.insert(0, "../..")
        if sys.version_info[0] >= 3:
            raw_input = input

        self.reserved = {
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
            'shelf':'SHELF',
            'book':'BOOK',
            'library':'LIBRARY'
        }

        self.tokens = [
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
        ] + list(self.reserved.values())

        # Build the lexer
        lex.lex()

        # Build Parse
        self.parser = yacc.yacc()

    def t_VARIABLE(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value,'VARIABLE')    # Check for reserved words
        return t

    def t_FLOAT(self, t):
        r'[-+]?((\d+\.\d*)|(\d*\.\d+))'
        t.value = float(t.value)
        return t

    def t_INTEGER(self, t):
        r'[-+]?\d+'
        t.value = int(t.value)
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)



    # Parsing rules

    def p_start(self, p):

        """
        start : statement
              | variable
              | empty
        """
        self.run(p[1])

    def p_statement(self, p):

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

    def p_verb(self, p):

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

    def p_entity(self, p):

        """
        entity : SHELF
               | BOOK
               | LIBRARY
        """

        p[0] = p[1].upper()

    def p_variable(self, p):
        """
        variable : VARIABLE
        """
        self.p_error(p)

    def p_empty(self, p):

        """
        empty :
        """
        p[0] = None

    def p_error(self, p):
        print("Syntax error found!")

    def run(self, p):
        if type(p) == tuple:
            if p[0] == 'VIEW':
                if p[1] == 'SHELF':
                    self.f_view_shelf_content(p[2])
                    return
            elif p[0] == 'GOTO':
                if p[1] == 'SHELF':
                    self.current_shelf = p[2]
                    return
            elif p[0] == 'RENT':
                if self.current_shelf == None:
                    print("Please goto a shelf first to rent a book!")
                    return
                else:
                    self.f_rent_book(p[1])
                    return

            elif p[0] == 'WHERE':
                self.f_find_location_book(p[1])
                return

            print("ERROR!")
            return

        else:
            if p == 'BACK':
                self.current_shelf = None
                return
            elif p == 'VIEW':
                if self.current_shelf == None:
                    self.f_view_library_content()
                    return
                else:
                    self.f_view_shelf_content(self.current_shelf)
                    return


            elif p == 'LOGIN':
                self.f_login()
                return
            elif p == 'DUE':
                if self.current_admin == None:
                    pass
                else:
                    if self.current_shelf == None:
                        print("Please goto a shelf first to view all rented books!")
                        return
                    else:
                        self.f_view_rented_books()
                        return

            return

    def f_view_shelf_content(self, shelf_id):
        # Testing
        content = list()
        content.append("Harry Potter and the Prisoner of Azkaban")
        content.append("Harry Potter pelao")
        print("Books in Shelf %s:" % shelf_id)
        for part in content:
            print("\t%s" % part)

    def f_view_library_content(self):
        # Testing
        content = list()
        content.append(5)
        content.append(2)
        print("Shelves in Library %s" % self.current_library)
        for shelf in content:
            print("\tShelf %d" % shelf)

    def f_find_location_book(self, book_name):
        # Testing Purposes
        shelves = list()
        shelves.append(5)
        shelves.append(7)

        print("Book %s is found in:" % book_name)
        for shelf in shelves:
            print("\tShelf %d" % shelf)

    def f_rent_book(self, book_name):
        id_number = input("What is your id number?\n > ")
        password = input("What is your password?\n > ")
        # Validate and update Data Base
        print("Request Accepted, please go to pick up at %s.\n Thank you." % self.current_library)

    def f_login(self):
        username = input("What is your username?\n > ")
        password = input("What is your password?\n > ")
        self.current_admin = username
        print("Successfully logged in as %s!" % self.current_admin)

    def f_view_rented_books(self):
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

    def run_code(self, s):
        if self.current_admin == None:
            s = input(' > ')
        if self.current_shelf == None:
            s = input(self.current_library + ' > ')
        else:
            s = input(self.current_library + '/Shelf' + str(self.current_shelf) + ' > ')
        self.parser.parse(s)





        # lex.input(s)
        # while True:
        #     tok = lex.token()
        #     if not tok:
        #         break  # No more input
        #     print(tok)
