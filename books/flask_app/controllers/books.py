from flask_app import app
from flask import redirect, request, render_template
from flask_app.models import book, author

@app.route('/')
def index():
    return redirect('/authors')

@app.route('/authors')
def authors():
    authors1 = author.Author.get_all()
    return render_template('authors.html', authors=authors1)

@app.route('/books')
def books():
    books1 = book.Book.get_all()
    return render_template('books.html', books=books1)

@app.route('/process', methods=['POST'])
def process():
    print(request.form)
    if request.form['type'] == 'create_author':
        data = {
            'name': request.form['name']
        }
        author.Author.save(data)
        return redirect('/authors')
    if request.form['type'] == 'create_book':
        data = {
            'title': request.form['title'],
            'num_of_pages': request.form['num_of_pages']
        }
        book.Book.save(data)
        return redirect('/books')
    if request.form['type'] == 'add_favorite':
        data = {
            'book_id':request.form['book_id'],
            'author_id':request.form['author_id']
        }
        author.Author.add_favorites(data)
        if request.form['ftype'] == 'author':
            return redirect(f'/authors/{request.form["author_id"]}')
        elif request.form['ftype'] == 'book':
            return redirect(f'/books/{request.form["book_id"]}')
        return redirect('/')

@app.route('/authors/<int:id>')
def get_author(id):
    data = {'id':id}
    author1 = author.Author.get_author_with_favorites(data)
    books = book.Book.get_all()
    print(books)
    return render_template('author.html', author = author1, books = books)

@app.route('/books/<int:id>')
def get_book(id):
    data = {'id':id}
    book1 = book.Book.get_book_with_on_favorites(data)
    authors = author.Author.get_all()
    return render_template('book.html', book = book1, authors = authors)