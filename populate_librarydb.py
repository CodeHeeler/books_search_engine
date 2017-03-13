import psycopg2
import csv


def main():
    conn = psycopg2.connect("dbname=librarydb user=rebelmerf host=/tmp/")
    cur = conn.cursor()
    cur.execute("CREATE TABLE book (id serial PRIMARY KEY, title varchar, author varchar, copyright integer, isbn varchar, pages integer, price decimal, keyword varchar);")
    # Doing a simplified version for this assignment:
    # --ignoring author names can have prefix/suffix, auther last name first
    # --ignoring alphabetizing differently with books that start with A/An/The
    # --filling in unknown fields with placeholders

    with open('initial_book_list.txt') as f:
        reader = csv.reader(f)
        for row in reader:
            my_title = row[0]
            my_author = row[1]
            if row[2] == "":
                my_copyright = 0
            else:
                my_copyright = row[2]
            my_isbn = row[3]
            if row[4] == "":
                my_pages = 0
            else:
                my_pages = row[4]
            if row[5] == "":
                my_price = 0
            else:
                my_price = row[5]
            my_keyword = row[6]
            cur.execute("INSERT INTO book (title, author, copyright, isbn, pages, price, keyword) VALUES (%s, %s, %s, %s, %s, %s, %s)", (my_title, my_author, my_copyright, my_isbn, my_pages, my_price, my_keyword))

    conn.commit()

    cur.close()
    conn.close()


main()
