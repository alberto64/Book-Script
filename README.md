# Book-Script
A programming language for managing a system that represent a virtual library. It utilizes ply for generationg of the lexical analyzer and parser.

## Requirements 
* Install Python 3 or above
* Install PostgreSQL
* Install psycopg2

## How To run

Create an instance of a database in the PostgreSQL server. To create the tables following the queries specified on this document https://docs.google.com/document/d/1JXz8idehu4YHer5wXui7BkM04si_E_Fdx_jLNz75TXg/edit?usp=sharing. For every new library (Database), new bookshelfs and a new admin user has to be created manually too. 

To run, you need Python 3 on your machine. Once Python 3 is installed, open a terminal instance and run the app.py file in this folder.

Currently this program supports the following commands:

* goto
* login
* view
* back
* where
* due


## Example Usage
### Example #1
```
LIBRARY > view
Shelves in Library Borders
        Shelf 5
        Shelf 2
LIBRARY > where "Harry Potter"
Book "Harry Potter" is found in:
	Shelf 5
	Shelf 7
LIBRARY > goto SHELF 5
LIBRARY/Shelf2 > view
Books in Shelf 2:
        Harry Potter and the Prisoner of Azkaban
        Harry Potter pelao
LIBRARY/Shelf2 > back
LIBRARY > login
What is your username?
 > gustavobravo20
What is your password?
 > ******
Successfully logged in as gustavobravo20!
LIBRARY > due

  Manuel A. Baez, 812-45-7890, “Almanaque Mundial 2016”, November 6, 2017

  Alberto J. De Jesus, 813-67-8907, “100 años De Soledad”, November 8, 2017
```
### Example #2

```
LIBRARY > rent "Harry Potter pelao"
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
