# Book-Script
A programming language for managing a system that represent a virtual library. It utilizes ply for generationg of the lexical analyzer and parser.

## Requirements
* Install Python 3 or above
* Install PostgreSQL
* Install psycopg2

## How To run

Create an instance of a database in the PostgreSQL server. To create the tables following the queries specified on this document https://docs.google.com/document/d/1JXz8idehu4YHer5wXui7BkM04si_E_Fdx_jLNz75TXg/edit?usp=sharing. For every new library (Database), new bookshelfs and a new admin user has to be created manually too.

To run, you need Python 3 and have the module psycopg2 on your machine. Once Python 3 is installed, open a terminal instance and run the app.py file in this folder.

Currently this program supports the following commands:

Navigation/Location Commands:
 * goto [library|shelf] [Name] - It navigates to the location provided
 * back - Back to the previous location
 * view - To see a list of the items in the current location
 * where [name] - Show the address of shelf or book given

User Commands:
 * login - Login as user on the system
 * logout - Logout as user on the system
 * register - Resgister a new user into the system
 * exit - A command that exits system
 * rent [name] - To rent the book with the given name
 * due - See all books the current user owes
 * help - Show the system commands and their functions
 * return - Lets user return a book that is due

Administrator Commands:
 * due - See all books that are due in the system		
 * delete - Delete a book
 * create - Create a book

## Example Usage
### Example #1: Enter the system for the first time and search for a book
```
Welcome to Book Script!!!!
“A library at the run of a program”
Do you want to register an account? (Y/N) or EXIT
 > Y
What is your username?
 > albert
What is your email?
 > albert@test.com
What is your password?
 > qwerty1234
What is your address?
 > My house at Puerto Rico
What is your phone number?
 > 7877877788
Successfully created and logged in as albert
albert > view
Available Libraries:
        latertulia
        borders
--------------------
albert > goto library "La Tertulia"
albert / latertulia > where "La Carreta"
Book found in:
	shelf 1
	shelf 4
--------------------
albert /latertulia> back
albert> logout
Do you want to register an account? (Y/N) or EXIT
 > Exit
Thank you for usign Book Script! Bye!
```
### Example #2: Login and rent a book
```
Welcome to Book Script!!!!
“A library at the run of a program”
Do you want to register an account? (Y/N) or EXIT
What is your username?
 > albert
What is your password?
 > qwerty1234
albert > goto library "borders"
albert / borders > where "Programming for Dummies"
Book found in:
	shelf 2
	shelf 3
--------------------
albert / borders > help
<Navigation/Location Commands>
   goto <library|shelf> <Name> - It navigates to the location provided
   back - Back to the previous location
   view - To see a list of the items in the current location
   where <name> - Show the address of shelf or book given
<User Commands>
   login - Login as user on the system
   logout - Logout as user on the system
   register - Resgister a new user into the system
   exit - A command that exits system
   rent <name> - To rent the book with the given name
   due - See all books the current user owes
   help - Show the system commands and their functions
   return - Lets user return a book that is due
albert / borders > goto shelf 2
albert / borders / shelf2 > rent "Programming for Dummies"
For how many days do you wish to rent the book?
> 10
Request Accepted, please go to pick up at borders.
Thank you!
This book will be due for the day 2/7/2018
albert / borders / shelf2 > due
Books currently due:
1 3835423545 2 Programming for Dummies UPRM Students 7-18-2017
--------------------
albert / borders / shelf2 > exit
Thank you for usign Book Script! Bye!
```
