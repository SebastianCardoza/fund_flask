from venv import create
from winreg import QueryInfoKey
from mysqlconnection import connectToMySQL

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.full_name = data['first_name'] + ' ' + data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all_users(cls):
        query = 'SELECT * FROM users;'
        result = connectToMySQL('esquema_usuarios').query_db(query)
        users = []
        for user in result:
            users.append(cls(user))
        return users

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO users(first_name, last_name, email) values(%(first_name)s, %(last_name)s, %(email)s);'
        return connectToMySQL('esquema_usuarios').query_db(query, data)

    @classmethod
    def delete(cls, id):
        query = 'DELETE FROM users WHERE id=%(id)s'
        data = {'id':id}
        connectToMySQL('esquema_usuarios').query_db(query, data)

    @classmethod
    def update(cls, data):
        query = 'UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, updated_at = NOW() WHERE id = %(id)s;'
        connectToMySQL('esquema_usuarios').query_db(query, data)

    @classmethod
    def get_user(cls, id):
        query = 'SELECT * FROM users WHERE id = %(id)s'
        data = {
            'id':id
        }
        result = connectToMySQL('esquema_usuarios').query_db(query, data)
        for lol in result:
            user = cls(lol)
        return user