# Import libraries we will use for project - sqlite and tabulate.
import sqlite3
from tabulate import tabulate

# Creating initial table within try - except statement to catch exceptions.
try:
    # Create and connect to our database.
    db = sqlite3.connect('ebookstore.db')

    # Create our cursor object.
    cursor = db.cursor()

    # Create initial table with our rows, using id as the primary key.
    cursor.execute('''
               CREATE TABLE IF NOT EXISTS book(id INTEGER PRIMARY KEY, title TEXT,
                author TEXT, qty INTEGER)
               ''')
    db.commit()

    # Populate table with first books.
    id1 = 3001
    title1 = 'A Tale of Two Cities'
    author1 = 'Charles Dickens'
    qty1 = 30

    id2 = 3002
    title2 = 'Harry Potter and the Philosophers Stone'
    author2 = 'J.K. Rowling'
    qty2 = 40

    id3 = 3003
    title3 = 'The Lion, the Witch and the Wardrobe'
    author3 = 'C.C Lewis'
    qty3 = 25

    id4 = 3004
    title4 = 'The Lord of the Rings'
    author4 = 'J.R.R Tolkien'
    qty4 = 37

    id5 = 3005
    title5 = 'Alice in Wonderland'
    author5 = 'Lewis Carroll'
    qty5 = 12

    # Create table contents and insert these into the table using executemany.
    table_contents = [(id1, title1, author1, qty1), (id2, title2, author2, qty2),
                    (id3, title3, author3, qty3), (id4, title4, author4, qty4),
                     (id5, title5, author5, qty5)]

    cursor.executemany('''
                   INSERT OR REPLACE INTO book(id, title, author, qty) VALUES(?,?,?,?)''',
                   table_contents)
    db.commit()
except Exception as e:
    db.rollback()
    raise e


# Create enter book function asking for user inputs for rows.
def enter_book():
    try:
        new_id = int(input('Please enter book id: '))
        new_title = input('Please enter the title: ')
        new_author = input('Please enter the author: ')
        new_qty = input('Please enter the quantity: ')
        cursor.execute('''
                   INSERT INTO book(id, title, author, qty)
                   VALUES(?,?,?,?)''', (new_id, new_title, new_author, new_qty))
        db.commit()
    except ValueError:
        print('Error. Please try again.')


# Update function which takes in id of book to change and new quantity of book.
def update_book():
    select_id = int(input('Please enter the id of the book you wish to update: '))
    update_qty = int(input('Please enter the new quantity: '))
    cursor.execute('''
                   UPDATE book SET qty = ? WHERE id = ? ''', (update_qty, select_id))
    db.commit()


# Create delete book function. Takes in id of book to be deleted from db.
def delete_book():
    delete_id = int(input('Please enter the id of the book you wish to delete: '))
    cursor.execute('''
                   DELETE FROM book WHERE id = ? ''', (delete_id,))
    print('Book successfully deleted.')
    db.commit()


# Create search book function, using partial searching for the title
# for better functionality and printing result using tabulate.
def search_book():
    search_title = (input('Please enter the title of the book you are searching for: '))
    cursor.execute('''
                   SELECT id, author, qty FROM book WHERE title LIKE '%' || ? || '%' ''', (search_title,))
    book = cursor.fetchall()
    print(tabulate(book, headers=["ID", "Author", "Quantity"]))


# Create function to view all books in db, using loop to print
# all data.
def view_all():
    cursor.execute('''
                   SELECT * FROM book''')
    for row in cursor:
        print('{0} : {1} : {2} : {3}'.format(row[0], row[1], row[2], row[3]))


# Create menu within while loop.
# Have menu options in if statement, calling appropriate function depending
# on user choice.
while True:
    print('\nMENU')
    print('1) Enter book')
    print('2) Update book')
    print('3) Delete book ')
    print('4) Search books')
    print('5) View all books')
    print('0) Exit')
    menu = int(input('Please choose from the menu option above: '))
    if menu == 1:
        enter_book()
    elif menu == 2:
        update_book()
    elif menu == 3:
        delete_book()
    elif menu == 4:
        search_book()
    elif menu == 5:
        view_all()
    elif menu == 0:
        db.close()
        exit()
    else:
        print('Error. Please try again.')