import psycopg2
import csv
import os


def clear():
    os.system('clear')


def search_library(cur):
    found = 0
    results = {}
    clear()
    my_title = input("What's the title of the book you're looking for? ")
    cur.execute("SELECT id,title,author FROM book WHERE title=%s", (my_title,))
    while True:
        possible_book = cur.fetchone()
        if possible_book == None:
            break
        found += 1
        results[found] = possible_book[0]
        print("\nResult # {}".format(found))
        print("Title: {}".format(possible_book[1]))
        print("Author: {}\n".format(possible_book[2]))
    if found == 0:
            print("\nSorry, there were no results for that search.\n\n")
            return
    choice = input("\nFor which result # would you like to see more details? ")
    cur.execute("SELECT * FROM book WHERE id=%s", (results.get(int(choice)),))
    my_book = cur.fetchone()
    print("\nTitle: {}".format(my_book[1]))
    print("Author: {}".format(my_book[2]))
    print("Copyright: {}".format(my_book[3]))
    print("ISBN: {}".format(my_book[4]))
    print("Pages: {}".format(my_book[5]))
    print("List Price: ${}".format(my_book[6]))
    print("Keyword: {}".format(my_book[7]))
    input("\nWhen you're ready, press enter to continue. ")
    clear()


def add_book(cur):
    # get user input for each
    clear()
    print("Add a Book:\n")
    print("Let's get some information on the book you want to enter. ")
    print("If you don't know an answer, just press enter to leave it blank.\n")
    my_title = input("What is the title? ")
    my_author = input("Who is the author? Please enter last name first (e.g. Shakespeare William)")
    my_copyright = input("What year was it first published? ")
    my_isbn = input("What is the ISBN? ")
    my_pages = input("How many pages does it have? ")
    my_price = input("What is the list price in US dollars? (e.g. 7.99)")
    my_keyword = input("What keyword do you most associate with this book? ")
    if my_copyright == "":
        my_copyright = 0
    if my_pages == "":
        my_pages = 0
    if my_price == "":
        my_price = 0
    cur.execute("INSERT INTO book (title, author, copyright, isbn, pages, price, keyword) VALUES (%s, %s, %s, %s, %s, %s, %s)", (my_title, my_author, my_copyright, my_isbn, my_pages, my_price, my_keyword))
    print("\nGreat! You've now added {} to the library!".format(my_title))
    input("\nWhen you're ready, press enter to continue. ")
    clear()


def main():
    conn = psycopg2.connect("dbname=librarydb user=rebelmerf host=/tmp/")
    cur = conn.cursor()

    # This is just for reference right now on the types and layout of the table:
    # cur.execute("CREATE TABLE book (id serial PRIMARY KEY, title varchar, author varchar, copyright integer, isbn varchar, pages integer, price decimal, keyword varchar);")
    # Doing a simplified version for this assignment:
    # --ignoring author names can have prefix/suffix
    # --ignoring alphabetizing differently with books that start with A/An/The

    quit = False
    choice = ""

    clear()

    while not quit:
        print("Would you like to search for a book or add a new one?")
        choice = input("(Please press 's' for search, 'a' for add, or 'q' to quit.) ")
        if choice.lower() == 's':
            search_library(cur)
        elif choice.lower() == 'a':
            add_book(cur)
        else:
            quit = True

    clear()

    conn.commit()

    cur.close()
    conn.close()


main()
