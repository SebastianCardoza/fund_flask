from winreg import QueryInfoKey
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.ninja import Ninja

class Dojo:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.ninjas = []

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO dojos (name) values (%(name)s);'
        return connectToMySQL('dojo_ninja').query_db(query, data)

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM dojos;'
        results = connectToMySQL('dojo_ninja').query_db(query)
        dojos = []
        for dojo in results:
            dojos.append(cls(dojo))
        return dojos

    @classmethod
    def get_dojo_with_ninjas(cls, data):
        query = 'SELECT * FROM dojos WHERE id = %(id)s;'
        results = connectToMySQL('dojo_ninja').query_db(query, data)
        dojo = cls(results[0])
        dojo.ninjas = Ninja.get_ninjas_by_dojo({'dojo_id': data['id']})
        return dojo
