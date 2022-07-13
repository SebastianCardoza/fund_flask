from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

class Dojo:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.ubicacion = data['ubicacion']
        self.idioma = data['idioma']
        self.comentario = data['comentario']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO dojos (nombre, ubicacion, idioma, comentario) VALUES (%(nombre)s, %(ubicacion)s, %(idioma)s, %(comentario)s);'
        return connectToMySQL('esquema_encuesta_dojo').query_db(query, data)

    @classmethod
    def get_dojo_by_id(cls, id):
        query = 'SELECT * FROM dojos WHERE id = %(id)s;'
        data = {'id': id}
        results = connectToMySQL('esquema_encuesta_dojo').query_db(query, data)
        return results[0]

    @staticmethod
    def validate_dojo(dojo):
        is_valid = True
        if len(dojo['nombre']) < 1: 
            flash('Name is obligatory')
            is_valid = False
        if len(dojo['idioma']) < 1: 
            flash('Language is obligatory')
            is_valid = False
        if len(dojo['ubicacion']) < 1: 
            flash('Location is obligatory')
            is_valid = False
        if len(dojo['comentario']) < 1: 
            flash('comment is obligatory')
            is_valid = False
        return is_valid