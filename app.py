from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Lidhja me bazën e të dhënave
db_config = {
    'user': 'root',
    'password': 'Bora135.,.',
    'host': 'localhost',
    'database': 'librarybooks'
}

# Home route për shfaqjen e librave
@app.route('/')
def index():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', books=books)

#Shto një libër të ri
@app.route('/add', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO books (title, author) VALUES (%s, %s)", (title, author))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect('/')

# Fshi një libër
@app.route('/delete/<int:book_id>')
def delete_book(book_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect('/')

# Kërko për një libër
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query').lower()
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Përdor LOWER() në kolonat title dhe author për të bërë krahasimin jo të ndjeshëm ndaj shkronjave
    cursor.execute("SELECT * FROM books WHERE LOWER(title) LIKE %s OR LOWER(author) LIKE %s",
                   ('%' + query + '%', '%' + query + '%'))

    books = cursor.fetchall()
    cursor.close()
    connection.close()


    message = "The book is not in the library. Oppsss!" if not books else None

    return render_template('index.html', books=books, message=message)


# shfaq formularin e shtimit të përdoruesit
@app.route('/add_user', methods=['GET'])
def show_add_user_form():
    return render_template('add_user.html')

#Shtimi përdoruesin e ri
@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users1 (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect('/')

#shfaq formularin e huazimit të librit
@app.route('/loan_book', methods=['GET'])
def show_loan_book_form():
    return render_template('loan_book.html')

#Huazimi i librit
@app.route('/loan_book', methods=['POST'])
def loan_book():
    user_id = request.form['user_id']
    book_id = request.form['book_id']
    loan_date = request.form['loandate']
    return_date = request.form['returndate']
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO loans1 (user_id, book_id, loandate, returndate) VALUES (%s, %s, %s, %s)",
                   (user_id, book_id, loan_date, return_date))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
