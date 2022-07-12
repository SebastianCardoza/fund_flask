from sqlite3 import connect
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book

class Author:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.favorites = []

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO authors (name) values (%(name)s);'
        return connectToMySQL('esquema_libros').query_db(query, data)

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM authors;'
        results = connectToMySQL('esquema_libros').query_db(query)
        authors = []
        for author in results:
            authors.append(cls(author))
        return authors

    @classmethod
    def get_author_with_favorites(cls, data):
        query = 'SELECT * FROM authors LEFT JOIN favorites ON favorites.author_id = authors.id LEFT JOIN books ON books.id = favorites.book_id WHERE authors.id = %(id)s'
        results = connectToMySQL('esquema_libros').query_db(query, data)
        author = cls(results[0])
        for row_from_db in results:
            data = {
                'id':row_from_db['books.id'],
                'title':row_from_db['title'],
                'num_of_pages':row_from_db['num_of_pages'],
                'created_at':row_from_db['books.created_at'],
                'updated_at':row_from_db['books.updated_at']
            }
            author.favorites.append(book.Book(data))
        return author

    @classmethod
    def add_favorites(cls, data):
        query = 'INSERT INTO favorites (book_id, author_id) VALUES (%(book_id)s, %(author_id)s);'
        return connectToMySQL('esquema_libros').query_db(query, data)
