# Book-Script
A programming language for managing a system that represent a virtual library. It utilizes ply for generationg of the lexical analyzer and parser.


## How To run

To run, you need Python 3 on your machine. Once Python 3 is installed, open a terminal instance and run the app.py file in this folder.

Currently this program supports the following commands:

* GOTO
* LOGIN
* VIEW
* BACK
* WHERE
* DUE

Since the application is not connected to a database, all the values that will appear will be simulated data.


## Example Usage
### Example #1
```
LIBRARY > VIEW
Shelves in Library Borders
        Shelf 5
        Shelf 2
LIBRARY > GOTO SHELF 5
LIBRARY/Shelf2 > view
Books in Shelf 2:
        Harry Potter and the Prisoner of Azkaban
        Harry Potter pelao
LIBRARY/Shelf2 > BACK
LIBRARY > login
What is your username?
 > gustavobravo20
What is your password?
 > ******
Successfully logged in as gustavobravo20!
LIBRARY > DUE

  Manuel A. Baez, 812-45-7890, “Almanaque Mundial 2016”, November 6, 2017

  Alberto J. De Jesus, 813-67-8907, “100 años De Soledad”, November 8, 2017
```
### Example #2

```
LIBRARY > RENT "Harry Potter pelao"
Please goto a shelf first to rent a book!
LIBRARY > goto shelf 2
LIBRARY/Shelf2 > rent "Harry Potter pelao"
What is your id number?
 > 802148888
What is your password?
 > ******
Request Accepted, please go to pick up at Borders.
 Thank you.
```
