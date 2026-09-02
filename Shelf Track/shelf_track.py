'''
This program will manage book inventory and information for a bookstore. The
data will be stored in a database using SQLite. The program will allow the user
to add entries, delete entries, update information, search the database and to
view all the books in the database.

For this program I did some research on the AUTOINCREMENT function of SQLite
(https://www.geeksforgeeks.org/sqlite/sqlite-autoincrement/) as well as the
sqlite_sequence https://sqlite.org/fileformat.html.
This specifically helps in generating correct Book ID's and also prevents re-
use of old ID's when a book is deleted.
I also researched the use of the zip() function from:
https://www.geeksforgeeks.org/python/zip-in-python/

To improve modularity of the code, I added additional functions for updating
books. I also added an additional functionality where the autor table can be
updated by the user if the author_id does not exist within the add_books()
function.
'''

# Import sqlite3 module to enable database functionality.
import sqlite3
from tabulate import tabulate


# Create functions for the relevant operations of the shelf_track program
def add_books():
    '''
    This function will allow the user to add books to the database. It will
    also check the database if the current book the user wants to add already
    exists. This will prevent duplication of the database. The user will be
    required to add a title, author ID and quantity.

    The function also checks if the autor ID exists in the author table. If not
    it wil launch the create_author() function to allow the user to create the
    new author.

    The function does not take any paramiters and does not return anything but
    updates to the relevant tables in the database is made.
    '''
    # Ask the user for a title
    title = input("Please provide a book title: ")

    # Ask the user to provide an author ID. This loop will evaluate if the
    # author ID is exactly 4 digits.
    while True:
        try:
            author_id = int(input("Please provide a 4 digit author ID: "))

            if len(str(author_id)) == 4:
                test = test_author(author_id)

                if test:
                    break
                elif not test:
                    print("Incorrect input. Please provide 4 digit ID.\n")
            else:
                print("Incorrect input. Please provide 4 digit ID.\n")

        except ValueError:
            print("Incorrect input. Please provide 4 digit ID.\n")

    # Request the quantity from the user:
    while True:
        try:
            quantity = int(input("Please provide the book quantity: "))
            break
        except ValueError:
            print("Please input numbers for quantity.\n")

    # Check if the book is already listed in the database
    cursor.execute(
        '''
        SELECT * FROM book
        WHERE authorID = ? AND title = ?
        ''', (author_id, title)
    )

    result = cursor.fetchone()

    # If statement to either create the entry or to inform user that the book
    # already exists.
    if result is None:

        cursor.execute(
            '''
            INSERT INTO book (title, authorID, qty)
            VALUES (?, ?, ?)
            ''', (title, author_id, quantity)
        )

        print("\nBook successfully captured in database.\n")

    else:
        print("\nThe book you entered already exists in the database.\n"
              "If you rather want to update the book, please use the\n"
              "update option in the main menu.\n")

    # Commit changes to the database
    db.commit()

    # END OF FUNCTION


def test_author(author_id):
    '''
    This function is used to test if the author to be added in add_books()
    function already exists in the author table. If not, the user has the
    option to create it using add_author or else the function will exit and the
    add_books() function will request a different ID from the user or continue
    with the created author.

    PARAMETERS
    The function takes in the author_id inserted by the user to test if it does
    exist in the author table.

    RETURNS
    The function returns True if the id exists or the author was successfully
    created or returns False if the user wants to insert a different id.
    '''

    cursor.execute(
        '''
        SELECT * FROM author
        WHERE id = ?
        ''', (author_id,)
    )
    result = cursor.fetchone()

    while True:
        if result is None:
            choice = input('''The author does not exist. Do you want to create
one?

y - yes
n - no, try different id
: ''').lower()

            if choice == 'y':
                add_author()
                return True
            elif choice == 'n':
                return False
                break
            else:
                print("Incorrect choice. Please try again.")

        else:
            return True

    # END OF FUNCTION


def add_author():
    '''
    This function allows the user to add an author to the author table in the
    database. It will request the ID, name and country for the author. The
    function will also check if the author already exists to prevent any
    duplication to take place.

    The function does not take in any parameters and also does not return any-
    thing. It only updates the author table with the new details.
    '''
    # Ask the user for the author id
    while True:
        try:
            author_id = int(input("\nPlease enter the author ID: "))

            if len(str(author_id)) == 4:
                # Check if id already exists
                cursor.execute(
                    '''
                    SELECT * FROM author
                    WHERE id = ?
                    ''', (author_id,)
                )
                result = cursor.fetchone()

                if result is None:
                    break
                else:
                    print("\nThe ID already exists in the database.\n")

            else:
                print("\nPlease provide a 4 digit id.\n")

        except ValueError:
            print("\nPlease provide a 4 digit id.\n")

    # Ask the user for the author name and country
    while True:
        name = input("\nPlease enter the author name and surname: ")
        country = input("\nPlease enter the author country of origin: ")

        # Check if the details already exist
        cursor.execute(
            '''
            SELECT * FROM author
            WHERE name = ? AND country = ?
            ''', (name, country)
        )

        result = cursor.fetchone()

        if result is None:
            break
        else:
            print("\nThe details already exist in the database.")

    # Add author details to author table
    cursor.execute(
        '''
        INSERT INTO author
        VALUES (?, ?, ?)
        ''', (author_id, name, country)
    )

    # Commit changes to database
    db.commit()

    print("Author added to database.")

    # END OF FUNCTION


def update_book():
    '''
    This function will allow the user to make updates to listed books in the
    database. The user can either update quantity or the title and authorID.
    The function does not take in parameters but it will update the database
    if any udates were made.
    '''
    # Options menu for updates required:
    while True:
        try:
            choice = int(input('''\nDo you want to:
1. Update quantities
2. Update title or auhor ID
3. Review and update author details
4. Exit to main menu
: '''
                               ))

            # Update quantity:
            if choice == 1:
                book_id = get_id()
                if book_id != 0:
                    update_qty(book_id)

            # Update title or author id:
            elif choice == 2:
                book_id = get_id()
                if book_id != 0:
                    update_other(book_id)

            elif choice == 3:
                book_id = get_id()
                if book_id != 0:
                    edit_author(book_id)

            elif choice == 4:
                break

            else:
                print("\nIncorrect choice. Please try again.\n")

        except ValueError:
            print("\nIncorrect choice. Please try again.\n")

    # END OF FUNCTION


def edit_author(book_id):
    '''
    This function allows the user to view the author details of the selected
    book id and also provides options to edit the author details. It is called
    within the update_book() function.

    PARAMETERS
    The function takes in the book_id as parameter

    RETURNS
    The function does not return anything but only displays the details on the
    screen and updates the autnor database if any changes has been made.
    '''

    # Join author and book tables to obtain relevant data to edit or view
    cursor.execute(
        '''
        SELECT book.id, book.title, book.authorID, author.name,
        author.country
        FROM book
        INNER JOIN author
        ON book.authorID = author.id
        WHERE book.id = ?
        ''', (book_id,)
    )

    # Get data from query and display to the user
    result = cursor.fetchone()

    data = [(result[1], result[3], result[4])]

    headers = ['Book Title', 'Author', 'Country of origin']

    print("\nThe details of the book requested are:\n")
    print(tabulate(data, headers=headers, tablefmt='fancy_grid'))

    # Request user if they want to update author and update if required:
    author_id = result[2]

    while True:
        choice = input('''Do you want to update author name?
y - yes
n - no
: ''').lower()

        if choice == 'y':
            name = input("Please provide updated author name: ")
            cursor.execute(
                '''
                UPDATE author SET name = ?
                WHERE id = ?
                ''', (name, author_id)
            )

            db.commit()

            print("\nAuthor name updated.\n")
            break

        elif choice == 'n':
            break

        else:
            print("Incorrect choice. Please try again.")

    while True:
        choice = input('''Do you want to update the author country?
y - yes
n - no
: ''').lower()

        if choice == 'y':
            country = input("Please provide updated counrty: ")
            cursor.execute(
                '''
                UPDATE author SET country = ?
                WHERE id = ?
                ''', (country, author_id)
            )

            db.commit()

            print("\nCountry updated.\n")
            break

        elif choice == 'n':
            break

        else:
            print("Incorrect choice. Please try again.")

    # END OF FUNCTION


def get_id():
    '''
    This function requests the book id to be updated from the user. It will
    request an id continuously until a correct id is supplied or the user can
    choose to exit to the previous menu.

    RETURNS
    The function returns the book id.
    '''

    # Request the book id that requires an update:
    while True:
        try:
            bk_id = int(input('''Please insert the book ID you want
or 0 to exit to the previous menu: '''
                              ))

            # Check if the id is correct and in database:
            cursor.execute(
                '''
                SELECT * FROM book WHERE id = ?
                ''', (bk_id,)
            )

            result = cursor.fetchone()

            if len(str(bk_id)) == 4 and result is not None:
                break
            elif bk_id == 0:
                break
            elif result is None:
                print("\nThe id you provided does not exist in the database.")

            else:
                print("\nPlease provide a 4 digit book ID.")

        except ValueError:
            print("\nPlease provide a 4 digit book ID.")

    return bk_id

    # END OF FUNCTION


def update_qty(book_id):
    '''
    This function allows the user to update the quantity of books with a
    specific id. The function takes in a book id and requests the user to
    update the quantity to a new value.

    PARAMETERS
    The function takes in the book id specified by the user in the update_
    books() function.

    RETURNS
    The function does not return anything but updates the database with the
    new quantity provided by the user.
    '''

    # Request the new quantity from the user:
    while True:
        try:
            new_qty = int(input("\nPlease provide the new quantity: "))
            break

        except ValueError:
            print("\nThe quantity should be a whole number.")

    cursor.execute(
        '''
        UPDATE book SET qty = ? WHERE id = ?
        ''', (new_qty, book_id)
    )

    # Commit change to the database
    db.commit()

    print("\nDatabase updated.")

    # END OF FUNCTION


def update_other(book_id):
    '''
    This function will allow the user to ubdate either the book title or author
    id. It will first ask the user if they want to update the title and then
    ask if they want to update the author id. Based on the response, the
    relevant updates will be performed.

    PARAMETERS
    The function takes in the book id from the update_books() function.

    RETURNS
    The function does not return anything but will update the relevant fields
    in the database as per the user's choices.
    '''

    # Ask the user if they want to update the book title:
    while True:
        option = input('''Do you want to update the book title?
y - yes
n - no
: '''
                       ).lower()

        if option == 'y':
            n_title = input("\nPlease provide the updated title: ")

            # Update database
            cursor.execute(
                '''
                UPDATE book SET title = ? WHERE id = ?
                ''', (n_title, book_id)
            )

            db.commit()
            print("\nTitle updated.\n")
            break
        elif option == 'n':
            break
        else:
            print("\nIncorrect choice. Please try again.\n")

    # Ask the user if they want to update author ID
    while True:
        option = input('''Do you want to update the autor id?
y - yes
n - no
: '''
                       ).lower()

        if option == 'y':
            while True:
                try:
                    n_authorid = int(input("\nPlease provide the updated "
                                           "author id: "))

                    if len(str(n_authorid)) == 4:
                        break
                    else:
                        print("Please provide a 4 digit id.")

                except ValueError:
                    print("Please provide a 4 digit id.")

            # Update database
            cursor.execute(
                '''
                UPDATE book SET authorID = ? WHERE id = ?
                ''', (n_authorid, book_id)
            )

            db.commit()
            print("\nAuthor ID updated.\n")
            break
        elif option == 'n':
            break
        else:
            print("\nIncorrect choice. Please try again.\n")

    # END OF FUNCTION


def delete_book():
    '''
    This function will allow the user to delete a book from the database. The
    user must provide the book id using the get_id() function. Once the id has
    been confirmed, the user will be asked to confirm deletion.

    The function does not take in any parameters and does not return anything.
    If the user confirms the deletion, the book will be deleted from the data-
    base.
    '''

    # Get book id from the user:
    book_id = get_id()

    # Request deletion if user did not exit from the get_id() function
    if book_id != 0:
        while True:
            choice = input('''Are you sure you want to delete the book?
y - yes
n - no
: '''
                           ).lower()

            if choice == 'y':
                cursor.execute(
                    '''
                    DELETE FROM book WHERE id = ?
                    ''', (book_id,)
                )

                db.commit()
                print(f"Book id {book_id} has been deleted from the database")
                break

            elif choice == 'n':
                break

            else:
                print("\nIncorrect choice, please try again.\n")

    # END OF FUNCTION


def search_books():
    '''
    This function allows the user to search for a book in the database by
    providing keywords contained in the title of the book or the entire title.
    The function will search the keywords in the database and print out a re-
    sult if a match is found else it will let the user know that no results are
    found.
    '''

    # Ask the user for title or keywords
    words = input("Please provide the book title or keywords from the title: ")

    words = f'%{words}%'

    # Search the database for a match
    cursor.execute(
        '''
        SELECT * FROM book
        WHERE title LIKE ?
        ''', (words,)
    )

    result = cursor.fetchall()

    if result == []:
        print("No results found.")
    else:
        headers = ['Book ID', 'Title', 'Author ID', 'Quantity']
        print(tabulate(result, headers=headers, tablefmt='fancy_grid'))

    # END OF FUNCTION


def view_all_books():
    '''
    This function will display a list of all books in the database to the user.
    The function does not take in any parameters and also does not return
    anything.
    '''

    # Retreive relevant data from database
    cursor.execute(
        '''
        SELECT book.title, author.name, author.country
        FROM book
        INNER JOIN author
        ON book.authorID = author.id
        '''
    )

    result = cursor.fetchall()

    # Separate the results into three separate tuples
    title, name, country = zip(*result)

    # Print the data to the screen
    print("Book Details:")

    for i in range(len(title)):
        print("_" * 60, "\n\n",
              f"Book Title:\t{title[i]}\n"
              f"Author Name:\t{name[i]}\n"
              f"Author Country:\t{country[i]}")

    print("_" * 60)

    # END OF FUNCTION


def init_database():
    '''
    This function initializes the database and ensures the initial data is pre-
    pobulated. If data already exists, the error in handled to prevent that the
    program stops. The function does not take in any parameters and does not
    return anything.
    '''

    # Connect to or create the database file:
    db = sqlite3.connect('ebookstore.db')

    # Get cursor to interact with database
    cursor = db.cursor()

    # Create the book table if it does not exist
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS book (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            authorID INTEGER(4),
            qty INTEGER
            )
            '''
    )

    # Commit changes to save table to database
    db.commit()

    # Create the author table if it does not exist
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS author (
            id INTEGER PRIMARY KEY,
            name TEXT,
            country TEXT
            )
            '''
    )

    # Commit changes to save table to database
    db.commit()

    # Lists of initial book and author data
    book_data = [
        (3001, 'A Tale of Two Cities', 1290, 30),
        (3002, "Harry Potter and the Philosopher's Stone", 8937, 40),
        (3003, 'The Lion, the Witch and the Wardrobe', 2356, 25),
        (3004, 'The Lord of the Rings', 6380, 37),
        (3005, "Alice's Adventures in Wonderland", 5620, 12)
    ]

    author_data = [
        (1290, 'Charles Dickens', 'England'),
        (8937, 'J.K. Rowling', 'England'),
        (2356, 'C.S. Lewis', 'Ireland'),
        (6380, 'J.R.R. Tolkien', 'South Africa'),
        (5620, 'Lewis Carroll', 'England')
    ]

    # This try loops will attempt to enter the data into the database, if the
    # data already exists, the exeption will catch the error and pass out of
    # the function
    try:
        cursor.executemany(
            '''
            INSERT INTO book(id, title, authorID, qty)
            VALUES (?, ?, ?, ?)
            ''', book_data
        )

        # Commit changes to database
        db.commit()

    except sqlite3.IntegrityError:
        pass

    try:
        cursor.executemany(
            '''
            INSERT INTO author(id, name, country)
            VALUES (?, ?, ?)
            ''', author_data
        )

        # Commit changes to database
        db.commit()

    except sqlite3.IntegrityError:
        pass

    # Close the database
    db.close()

    # END OF FUNCTION


# Initialize the database:
init_database()

# Provide a menu to the user:
print("Welcome to Shelf Track. The program to help manage book inventory.\n")

while True:
    # Launch the main menu
    menu = input(
        '''\nSelect one of the following options:
1. Enter book
2. Update book
3. Delete book
4. Search books
5. View details of all books
0. Exit
: '''
        )

    if menu == '1':
        # Connect to database and create cursor
        db = sqlite3.connect('ebookstore.db')
        cursor = db.cursor()

        # Call the add_books() function
        add_books()

        # Close the database
        db.close()

    elif menu == '2':
        # Connect to database and create cursor
        db = sqlite3.connect('ebookstore.db')

        try:
            with db:
                cursor = db.cursor()

                # Call the update_book() function
                update_book()
        finally:
            # Close the database
            db.close()

    elif menu == '3':
        # Connect to database and create cursor
        db = sqlite3.connect('ebookstore.db')
        cursor = db.cursor()

        # Call the delete_book() function
        delete_book()

        # Close the database
        db.close()

    elif menu == '4':
        # Connect to database and create cursor
        db = sqlite3.connect('ebookstore.db')
        cursor = db.cursor()

        # Call the search_books() function
        search_books()

        # Close the database
        db.close()

    elif menu == '5':
        # Connect to database and create cursor
        db = sqlite3.connect('ebookstore.db')
        cursor = db.cursor()

        # Call the view_all_books() function
        view_all_books()

        # Close the database
        db.close()

    elif menu == '0':
        # Exit the program
        print("Goodbye!")
        raise SystemExit()

    else:
        print("Incorrect input. Please try again.")
