import sqlite3

#The database is created and cursor initialised.
db = sqlite3.connect('ebookstore')
cursor = db.cursor()

#The book table is created
cursor.execute('''
    CREATE TABLE books(
    id INTEGER PRIMARY KEY,
    Title TEXT,
    Author TEXT, 
    Qty INTEGER)
    ''')
db.commit()

#The 'Book' class is defined to contain all of the info for each book. 
class Book():
    def __init__(self, id, Title, Author, Qty):
        self.id = id
        self.Title = Title
        self.Author = Author
        self.Qty = Qty

#The initial book information is entered. 
two_cities = Book(3001, 'A Tale of Two Cities', 'Charles Dickens', 30)
harry_potter = Book(3002, 'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 40)
narnia = Book(3003, 'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 25)
lotr = Book(3004, 'The Lord of the Rings', 'J.R.R. Tolkein', 37)
alice = Book(3005, 'Alice in Wonderland', 'Lewis Carroll', 12)

#Each Book object is added to the table
book_list = [two_cities, harry_potter, narnia, lotr, alice]
for book in book_list:
    book_data = [int(book.id), book.Title, book.Author, int(book.Qty)]
    cursor.execute('''INSERT INTO books(id, Title, Author, Qty) VALUES(?,?,?,?)''', book_data)
    db.commit()

#This function allows new books to be added.
#The current max id is found and incremented by 1 to give the new id.
def add_book():
    cursor.execute('''SELECT MAX(id) FROM books''')
    max_id = cursor.fetchone()[0]    
    new_id = max_id + 1
    new_title = input("Enter the title of the book to be added: ")
    new_author = input("Enter the author: ")
    new_qty = int(input("Enter the quantity: "))
    new_book = Book(new_id, new_title, new_author, new_qty)
    book_data = [new_book.id, new_book.Title, new_book.Author, new_book.Qty]
    cursor.execute('''INSERT INTO books(id, Title, Author, Qty) VALUES(?,?,?,?)''', book_data)
    db.commit()
    print(f'{new_title} has been successfully added to the database')
    print()

#This allows existing books to be updated by reference to their id, which is the primary key.
def update_book():
    book_to_update = int(input("Enter the id of the book to be updated: "))
    field_to_update = input("Enter the field to be updated (id, Title, Author or Qty (case sensitive): ")
    new_value = input('Enter the new value for the updated field: ')
    cursor.execute(f'''UPDATE books SET {field_to_update} = ? WHERE id = ?''', (new_value, book_to_update))
    db.commit()
    print('Update Successful')
    print()

#This allows deletion of books. 
def delete_book():
    book_to_delete = (input("Enter the id of the book to be deleted: "))
    cursor.execute('''DELETE FROM books WHERE id = ?''', ((book_to_delete,)))
    db.commit()
    print('Book successfully deleted')

#This allows the database to be searched for books. 
#id and Qty are integers, so the input is cast to int if these fields are being searched. 
def search_books():
    search_field = input("Enter the field you wish to search (id, Title, Author or Qty (case sensitive): ")
    valid_fields = ['id', 'Title', 'Author', 'Qty']
    #An error is returned if an invalid field is searched. 
    if search_field not in valid_fields:
        print('That field does not exist')
        print()
    else:
        if search_field == 'id' or search_field == 'Qty':
            search_term = int(input("Enter the value to search for: "))
        else:
            search_term = input("Enter the value to search for: ")
        cursor.execute(f'''SELECT * FROM books WHERE {search_field} = ?''', (search_term,))
        #This allows multiple results to be returned, for example if the user searches for all books by a given author.
        output = cursor.fetchall()
        #An error is returned if no records are found. 
        if output == []:
            print('No matching records found')
            print()
        else:
            for result in output:
                print(result)
            print()

user_choice = ""

#Each of the functions above are called depending on the user input. 
while user_choice != "0":
    user_choice = input('''What would you like to do?
1 - Enter Book
2 - Update Book
3 - Delete Book
4 - Search Books
5 - Print Database
0 - Exit
''')

    if user_choice == '1':
        add_book()

    elif user_choice == '2':
        update_book()
    
    elif user_choice == '3':
        delete_book()

    elif user_choice == '4':
        search_books()

    elif user_choice == '5':
        cursor.execute('''SELECT * FROM books''')
        for row in cursor:
            print(row)

    elif user_choice == '0':
        print("Goodbye")

    else:
        print("Oops - incorrect input")
