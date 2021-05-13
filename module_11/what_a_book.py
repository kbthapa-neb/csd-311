""" 
    what_a_book.py
    khadga Thapa
    5/12/2021
    Console program that interfaces with a MySQL database
"""

""" import statements """
import sys
import csv
import mysql.connector
from mysql.connector import errorcode

""" database config object """
config = {
    "user": "whatabook_user",
    "password": "MySQL8IsGreat!",
    "host": "127.0.0.1",
    "database": "whatabook",
    "raise_on_warnings": True
}


def main():
   menu()


def menu():

    print("\n       ************Welcome To WhatABook Website**************")
    print()

    print("""       What Would you Like To Do Today?

                      1: View Books
                      2: View Store Locations
                      3: View Your Account
                      4: Exit Program""")
                    
    while True:
        try:
            choice = (int(input(""" 
                    Please enter the number located next to your choice: 
                    For example, enter 1 to View Books: """)))
            if choice == 1 :
                view_books()
                break
            elif choice == 2 :
                view_store_locations()
                break
            elif choice == 3:
                my_account()
                break
            elif choice == 4:
            #sys.exit(0)
                break
            else:
                print("     You must only select numbers 1 thorugh 4")
                print("     Please try again")
            menu()
        except ValueError:
            print("     Invalid Choice. Enter 1-4")
            menu()

def view_books():
    db = mysql.connector.connect(**config) # connect to the whatabook database 

    cursor = db.cursor()
   # inner join query 
    cursor.execute("SELECT book_id, book_name, author, details from book")

    # get the results from the cursor object 
    books = cursor.fetchall()

    print("\n       ----- DISPLAYING BOOK LISTING -----")
    
    # iterate over the player data set and display the results 
    for book in books:
        print(" \nBook ID: {}".format(book[0]))
        print(" Book Name: {}".format(book[1]))
        print(" Author: {}".format(book[2]))
        print(" Details: {}".format(book[3]))
        #menu()        
#view_books()

        
#main()
    # keep this function with this indentation!!!!!!!
    menu()
#view_store_locations()
        

def view_store_locations():

    db = mysql.connector.connect(**config) # connect to the whatabook database 

    cursor = db.cursor()

    cursor.execute("SELECT store_id, locale from store")

    locations = cursor.fetchall()

    print("\n         ----- DISPLAYING STORE LOCATIONS -----\n")
    
    for location in locations:
        print("  Locale: {}\n".format(location[1]))
        break
#view_store_locations()

    
    menu()
#main()
   

def my_account():

    while True:
        try:
            global user_id
            user_id = (int(input("""
        !!! We need to verify your identity first!!!
            
        Enter your customer id: For example, enter 1 for user ID 1: """)))

            if user_id >= 1 and user_id <= 3:
                show_account_menu()
                break
    
            else:
                print("\n            !!!!!!!Invalid Customer ID Number!!!!!!!!")
                print("\n           -----------Please try again-------------\n")
                my_account()
        except ValueError:
            print("\n           --------Invalid Choice. Enter a valid User ID Number please!--------")
            my_account()
        my_account()
    

        #menu()

def show_account_menu():
    
    print("\n       ************Welcome To Your Personalized WhatABook Web Account**************")
    print()

    print("\n       ----- Customer Menu -----  ")
    print("""

                What Would you Like To Do In Your Account?

                    1: Show My Whishlist
                    2: Show Books to Add to My Whishlist
                    3: Add books to My Wishlist
                    4: Main Menu
                    5: Exit Program """)

    while True:
        try:
            
            account_choice = (int(input("""

            Please enter the number located next to your choice: 
            For example, enter 1 to view your Whishlist:  """ )))
                    
            if account_choice == 1 :
                show_wishlist()
                break
            elif account_choice == 2 :
                show_books_to_add()
                break
            elif account_choice == 3:
                show_books_to_add()
                add_book_to_wishlist()  
                break
            elif account_choice == 4:
                menu()
                break
            elif account_choice == 5:
                sys.exit(0)
            else:
                print("         You must only select numbers 1 thorugh 5")
                print("         Please try again")
            show_account_menu()
        except ValueError:
            print("         Invalid Choice. Enter 1-5")
            show_account_menu()
    show_account_menu()

def show_wishlist():

    # Display list of books available to be added to wishlists 
    db = mysql.connector.connect(**config) # connect to the whatabook database 

    cursor = db.cursor()
    
    #user_id will appear as undeclared since we are waiting for user to enter a user_id
    #program will work though
    cursor.execute("SELECT user.user_id, user.first_name, user.last_name, book.book_id, book.book_name, book.author " + 
                    "FROM wishlist " + 
                    "INNER JOIN user ON wishlist.user_id = user.user_id " + 
                    "INNER JOIN book ON wishlist.book_id = book.book_id " + 
                    "WHERE user.user_id = {}".format(user_id))
    
    wishlist = cursor.fetchall()

    print("\n        -- DISPLAYING WISHLIST ITEMS --\n")

    for book in wishlist:
        print("\n        Book Name: {}".format(book[4]))
        print("        Author: {}".format(book[5]))
        print()
        
    #keep show_account_menu() with this indentention to make sure account menu pops up again after user selection
    show_account_menu()

def show_books_to_add():

    # query to display books not in wishlist
    db = mysql.connector.connect(**config) # connect to the whatabook database 

    cursor = db.cursor()

    query = ("SELECT book_id, book_name, author, details "
            "FROM book "
            "WHERE book_id NOT IN (SELECT book_id FROM wishlist WHERE user_id = {})".format(user_id))

    print(query)

    cursor.execute(query)

    books_to_add = cursor.fetchall()

    print("\n        -- DISPLAYING AVAILABLE BOOKS --")

    for book in books_to_add:
        print("\n        Book Id: {}".format(book[0]))
        print("        Book Name: {}".format(book[1]))
        print("        Book Author: {}".format(book[2]))
        print("        Book Details: {}".format(book[3]))
        print()

def add_book_to_wishlist():

    while True:
        try:
            


            db = mysql.connector.connect(**config) # connect to the WhatABook database 

            cursor = db.cursor() # cursor for MySQL queries
            book_id = int(input("\n        Enter the id of the book you want to add: "))

            if book_id >= 1 and book_id <=9 :

                cursor.execute("INSERT INTO wishlist(user_id, book_id) VALUES({}, {})".format(user_id, book_id))
   
                db.commit()
                show_account_menu()
            else:
                print("\n         Invalid Choice. Enter 1-9")

        except ValueError:
            print("\n            Invalid Choice. Enter 1-9")
            add_book_to_wishlist()
#the program is initiated, so to speak, here
main()
#menu()
