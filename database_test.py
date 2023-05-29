import sqlite3
from tabulate import tabulate
import os


# Define the function to create a connection to the database and create the ebookstore table
def connect_db():
    conn = sqlite3.connect('ebookstore.db')
    cursor = conn.cursor()

    # Check if the ebookstore table already exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ebookstore'")
    table_exists = cursor.fetchone()

    if not table_exists:
        # Create the ebookstore table if it doesn't exist
        cursor.execute('''CREATE TABLE ebookstore
                        (id INTEGER PRIMARY KEY,
                        title TEXT,
                        author TEXT,
                        qty INTEGER)''')

    # Check if all required columns exist in the table
    cursor.execute("PRAGMA table_info(ebookstore)")
    table_columns = cursor.fetchall()

    if len(table_columns) != 4 or \
       table_columns[0][1] != 'id' or \
       table_columns[1][1] != 'title' or \
       table_columns[2][1] != 'author' or \
       table_columns[3][1] != 'qty':

        # Drop the ebookstore table if any required column is missing
        cursor.execute("DROP TABLE IF EXISTS ebookstore")

        # Create the ebookstore table with required columns
        cursor.execute('''CREATE TABLE ebookstore
                        (id INTEGER PRIMARY KEY,
                        title TEXT,
                        author TEXT,
                        qty INTEGER)''')

        # Insert initial data into the table
        rows_to_insert = [
            (3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
            (3002, 'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 40),
            (3003, 'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 25),
            (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
            (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)
        ]
        cursor.executemany('INSERT INTO ebookstore VALUES (?,?,?,?)', rows_to_insert)

    # Check if there are any rows in the table
    cursor.execute("SELECT COUNT(*) FROM ebookstore")
    rows_exist = cursor.fetchone()[0]

    if not rows_exist:
        # Insert initial data into the table if there are no rows
        rows_to_insert = [
            (3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
            (3002, 'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 40),
            (3003, 'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 25),
            (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
            (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)
        ]
        cursor.executemany('INSERT INTO ebookstore VALUES (?,?,?,?)', rows_to_insert)

    return conn



# Define the function to add a book to the ebookstore table
def add_book(conn, book):
    cur = conn.cursor()
    cur.execute("INSERT INTO ebookstore (id, title, author, qty) VALUES (?, ?, ?, ?)", book)
    conn.commit()
    print("Book added successfully.")


def clear():
    """Clears the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def view_books(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM ebookstore")
    books = cur.fetchall()
    if not books:
        print("There are no books in the library.")
    else:
        headers = ['ID', 'Title', 'Author', 'Quantity']
        print(tabulate(books, headers=headers))


def update_book(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM ebookstore")
    books = cur.fetchall()
    if len(books) == 0:
        print("There are no books in the library.")
    else:
        print("Available book IDs:")
        for book in books:
            print(book[0])
        book_id = int(input("Enter the ID of the book you want to update: "))
        found_book = False
        for i, book in enumerate(books):
            if book[0] == book_id:
                found_book = True
                book_title = input("Enter the new title (leave blank to keep the same): ")
                book_author = input("Enter the new author (leave blank to keep the same): ")
                cur.execute("UPDATE ebookstore SET title = :title, author = :author WHERE id = :book_id",
                            {"title": book_title or book[1], "author": book_author or book[2], "book_id": book_id})
                conn.commit()
                print("Book with ID {} updated successfully.".format(book_id))
                break
        if not found_book:
            print("Book with ID {} not found.".format(book_id))



def delete_book(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM ebookstore")
    books = cur.fetchall()
    if len(books) == 0:
        print("There are no books in the library.")
    else:
        print("Available book IDs:")
        for book in books:
            print(book[0])
        book_id = int(input("Enter the ID of the book you want to delete: "))
        found_book = False
        for i, book in enumerate(books):
            if book[0] == book_id:
                cur.execute("DELETE FROM ebookstore WHERE id=?", (book_id,))
                conn.commit()
                found_book = True
                print("Book with ID {} deleted successfully.".format(book_id))
                break
        if not found_book:
            print("Book with ID {} not found.".format(book_id))



# Define the function to search for a book in the ebookstore table
def search_book(conn, book_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM ebookstore WHERE id=?", (book_id,))
    book = cur.fetchone()
    if book:
        print("Book found:")
        print("ID:", book[0])
        print("Title:", book[1])
        print("Author:", book[2])
        print("Qty:", book[3])
    else:
        print("Book not found.")


def reset_db(conn):
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS ebookstore")
    connect_db()


# This function displays a menu of options and returns the user's choice
def menu():
    print("Bookstore Inventory Management")
    print("1. Enter new book")
    print("2. Update book")
    print("3. Delete book")
    print("4. Search books")
    print("5. View Books")
    print("6. Reset database")
    print("0. Exit")
    choice = input("Enter your choice: ")
    return int(choice)


# This function prompts the user to enter details about a new book
def enter_book(conn):
    while True:
        book_id = input("Enter book ID, example 3001: ")
        c = conn.cursor()
        c.execute("SELECT * FROM ebookstore WHERE id=?", (book_id,))
        result = c.fetchone()
        if result:
            print("Book with this ID already exists in the database. Please enter a unique ID.")
        else:
            title = input("Enter book title, example To Kill a Mockingbird: ")
            author = input("Enter book author:, example Harper Lee: ")
            c.execute("SELECT * FROM ebookstore WHERE title=? AND author=?", (title, author))
            result = c.fetchone()
            if result:
                print("Book with this title and author already exists in the database. Please enter a unique title and author.")
            else:
                qty = input("Enter quantity:, example 20: ")
                return (book_id, title, author, qty)




def main():
    # Establishes a connection to the database
    conn = connect_db()

    # Displays the menu and prompts the user to make a choice and clears the screen
    clear()
    choice = menu()

    # Loops until the user chooses to exit
    while choice != 0:
        if choice == 1:
            # Prompts the user to enter details about a new book and adds it to the database
            book = enter_book(conn)
            add_book(conn, book)
        elif choice == 2:
            # Prompts the user to update details about an existing book
            update_book(conn)
        elif choice == 3:
            # Prompts the user to delete an existing book from the database
            delete_book(conn)
        elif choice == 4:
            # Prompts the user to enter a book ID and searches for the book in the database
            book_id = input("Enter book ID: ")
            search_book(conn, book_id)
        elif choice == 5:
            # Displays all the books in the database
            view_books(conn)
        elif choice == 6:
            # Resets the database
            reset_db(conn)
            print("Database reset successfully.")
        else:
            # Prompts the user to enter a valid choice
            print("Invalid choice.")

        # Displays the menu and prompts the user to make a choice
        choice = menu()

    # Closes the database connection when the program exits
    conn.close()
    print("Program exited.")


if __name__ == '__main__':
    main()

