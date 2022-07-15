from datetime import datetime
from unicodedata import category
from flask import flash
import re
from flask_app.config.mysqlconnection import connectToMySQL

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.password = data['password']
        self.email = data['email']
        self.has_belt = data['has_belt']
        self.belt_date = data['belt_date']
        self.belt_color = data['belt_color']

    @classmethod
    def save(cls, data):
        data['has_belt'] = int(data['has_belt'])
        query = 'INSERT INTO users (first_name, last_name, email, password, has_belt, belt_date, belt_color) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(has_belt)s, %(belt_date)s, %(belt_color)s);'
        return connectToMySQL('login').query_db(query, data)

    @classmethod
    def get_user_by_id(cls, id):
        query = 'SELECT * FROM users WHERE id = %(id)s;'    
        data = {'id': id}
        results = connectToMySQL('login').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def email_in_db(cls, email):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        data = {'email': email}
        results = connectToMySQL('login').query_db(query, data)
        if len(results) < 1:
            return 0
        return cls(results[0])

    @staticmethod
    def validate_register(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash('First name has to be at least 2 characters', category='register')
            is_valid = False
        if len(user['last_name']) < 2:
            flash('Last name has to be at least 2 characters', category='register')
            is_valid = False
        if User.email_in_db(user['email']) != 0:
            flash('Email already exists', category='register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Email is not valid', category='register')
            is_valid = False
        if len(user['password']) < 8:
            flash('Password has to be at least 8 characters', category='register')
            is_valid = False
        if user['password'] != user['confirmation']:
            flash('Passwords doesnt match', category='register')
            is_valid = False
        if 'has_belt' in user and not 'belt_color' in user:
            flash('Need to choose a belt color!', category='register')
            is_valid = False
        if not 'has_belt' in user and 'belt_color' in user:
            flash('Need to have a belt! (mark the checkbox)', category='register')
            is_valid = False
        if len(user['belt_date']) > 1:
            values = user['belt_date'].split('-')
            present = datetime.now()
            if datetime(int(values[0]), int(values[1]), int(values[2])) > present:
                flash('Belt exam date cant be in the future!', category='register')
                is_valid = False

        return is_valid