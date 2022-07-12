from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author

class Book:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.on_favorites = []

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO books (title, num_of_pages) values (%(title)s, %(num_of_pages)s);'
        return connectToMySQL('esquema_libros').query_db(query, data)

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM books;'
        results = connectToMySQL('esquema_libros').query_db(query)
        books = []
        for book in results:
            books.append(cls(book))
        return books

    @classmethod
    def get_book_with_on_favorites(cls, data):
        query = 'SELECT * FROM books LEFT JOIN favorites ON favorites.book_id = books.id LEFT JOIN authors ON authors.id = favorites.author_id WHERE books.id = %(id)s'
        results = connectToMySQL('esquema_libros').query_db(query, data)
        book = cls(results[0])
        for row_from_db in results:
            data = {
                'id':row_from_db['authors.id'],
                'name':row_from_db['name'],
                'created_at':row_from_db['authors.created_at'],
                'updated_at':row_from_db['authors.updated_at']
            }
            book.on_favorites.append(author.Author(data))
        return book