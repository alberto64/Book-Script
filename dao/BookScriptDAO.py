from config.dbconfig import pg_config
import psycopg2

class BookScriptDAO:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllBooks(self):
        cursor = self.conn.cursor ()
        query = "select * from books;"
        cursor.execute (query,)
        result = []
        for row in cursor:
            result.append (row)
        return result

    def getBookByName(self,bname):
        cursor = self.conn.cursor ()
        query = "select * from books where bname =%s;"
        cursor.execute (query,bname,)
        result = []
        for row in cursor:
            result.append (row)
        return result

    def getAllShelves(self):
        cursor = self.conn.cursor ()
        query = "select distinct shelfID from books;"
        cursor.execute (query)
        result = []
        for row in cursor:
            result.append (row)
        return result

    def getShelfById(self, shelf_id):
        cursor = self.conn.cursor ()
        query = "select distinct shelfID from books where shelfID = %s;"
        cursor.execute (query, (shelf_id,))
        result = cursor.fetchone()
        return result

    def getBooksByShelfId(self, shelf_id):
        cursor = self.conn.cursor ()
        query = "select bID, isbn, bname, bgenre, bauthor, bpublisher, bpublishdate from books where shelfID =%s;"
        cursor.execute (query, (shelf_id,))
        result = []
        for row in cursor:
            result.append (row)
        return result

    def isRented(self, bid):
        cursor = self.conn.cursor ()
        query = "select isRented from booksrental where bid = %s;"
        isRented = cursor.execute (query, (bid,))
        return isRented[0]

    def getBookByID(self, bID):
        cursor = self.conn.cursor ()
        query = "select * from books where bid = %S AND bID NOT IN(select bID from books natural inner join booksrental where bid = %s AND isRented = 'TRUE')"
        cursor.execute (query, (bID,bID,))
        result = []
        for row in cursor:
            result.append (row)
        return result


    def getAllAvailableBooks(self):
        cursor = self.conn.cursor ()
        query = "select * from books where bID NOT IN(select bID from books natural inner join booksrental where isRented = 'TRUE')"
        cursor.execute (query)
        result = []
        for row in cursor:
            result.append (row)
        return result

    def getAllRentedBooks(self):
        cursor = self.conn.cursor ()
        query = "select * from books where bID IN(select bID from books natural inner join booksrental where isRented = 'TRUE')"
        cursor.execute (query)
        result = []
        for row in cursor:
            result.append (row)
        return result

    def getAllRentedBooksFromUser(self, uid):
        cursor = self.conn.cursor ()
        query = "select * from books where bID IN(select bID from books natural inner join booksrental where isRented = 'TRUE' and uID = %s)"
        cursor.execute (query, (uid,))
        result = []
        for row in cursor:
            result.append (row)
        return result

    def rentAvailableBook(self, date_rental, return_date, isrented, bid, uid):
        cursor = self.conn.cursor ()
        rid = BookScriptDAO.getMaxBookRentalID (self) + 1
        query = "insert into booksrental(rid,date_rental,return_date,isrented,bid,uid) values (%s, %s, %s, %s, %s, %s);"
        cursor.execute (query, (rid, date_rental, return_date, isrented, bid, uid,))
        return rid

    def getAllUsers(self):
        cursor = self.conn.cursor ()
        query = "select * from users;"
        cursor.execute (query)
        result = []
        for row in cursor:
            result.append (row)
        return result

    def getUserByID(self, uid):
        cursor = self.conn.cursor ()
        query = "select * from users where uid = %s;"
        cursor.execute (query, (uid,))
        result = []
        for row in cursor:
            result.append (row)
        return result

    def getUserIDByUserName(self, username):
        cursor = self.conn.cursor ()
        query = "select uid from users where username = %s;"
        cursor.execute (query, (username,))
        result = cursor.fetchone ()
        return result

    def createNewBook(self,isbn,shelfid,bname,bgenre,bauthor,bpublisher,bpublishdate):
        cursor = self.conn.cursor ()
        bid = BookScriptDAO.getMaxBookID (self) +1
        query = "insert into books(bid,isbn,shelfid,bname,bgenre,bauthor,bpublisher,bpublishdate) values (%s, %s, %s, %s, %s, %s, %s, %s) ;"
        cursor.execute (query, (bid,isbn,shelfid,bname,bgenre,bauthor,bpublisher,bpublishdate,))
        return bid

    def createNewUser(self,username,password,address,phone,email,isadmin):
        cursor = self.conn.cursor ()
        uid = BookScriptDAO.getMaxUserID (self) +1
        query = "insert into users(uid,username,password,address,phone,email,isadmin) values (%s, %s, %s, %s, %s, %s, %s) ;"
        cursor.execute (query, (uid,username,password,address,phone,email,isadmin,))
        return uid

    def changeBookAvailability(self, bid, isrented):
        cursor = self.conn.cursor ()
        query = "update bookrental set isrented = %s where bid = %s;"
        cursor.execute (query, (bid,isrented,))
        return bid

    def getMaxBookID(self):
        cursor = self.conn.cursor()
        query = "select max(bid) from books;"
        cursor.execute (query)
        maxid = cursor.fetchone ()
        if (maxid is 0) or (maxid is None):
            return 1;
        return maxid[0]

    def getMaxBookRentalID(self):
        cursor = self.conn.cursor()
        query = "select max(rid) from booksrental;"
        cursor.execute (query)
        maxid = cursor.fetchone ()
        if (maxid is 0) or (maxid is None):
            return 1;
        return maxid[0]

    def getMaxUserID(self):
        cursor = self.conn.cursor()
        query = "select max(uid) from users;"
        cursor.execute (query)
        maxid = cursor.fetchone ()
        if (maxid is 0) or (maxid is None):
            return 1;
        return maxid[0]

    def deleteBook(self, bid):
        cursor = self.conn.cursor ()
        query = "delete from books where bid = %s;"
        cursor.execute (query, (bid,))
        self.conn.commit ()
        return bid

    def deleteUser(self, uid):
        cursor = self.conn.cursor ()
        query = "delete from users where uid = %s;"
        cursor.execute (query, (uid,))
        self.conn.commit ()
        return uid

    def getUserByUsernameAndPassword(self, username, password):
        cursor = self.conn.cursor ()
        query = "select uID, isAdmin from users where username = %s and password = %s;"
        cursor.execute (query, (username,password,))
        result = cursor.fetchone()
        return result

    def getPasswordByUsername(self, username):
        cursor = self.conn.cursor ()
        query = "select password from users where username = %s;"
        cursor.execute (query, (username,))
        result = cursor.fetchone()
        return result

    def getUsernameIsAdmin(self, username):
        cursor = self.conn.cursor ()
        query = "select isAdmin from users where username = %s;"
        cursor.execute (query, (username,))
        result = cursor.fetchone()
        return result[0]
