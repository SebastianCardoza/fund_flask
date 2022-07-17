from flask import flash
import re
from flask_app.config.mysqlconnection import connectToMySQL

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class Mail:
    def __init__(self, data):
        self.id = data['id']
        self.address = data['address']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO mails (address) values (%(address)s);'
        return connectToMySQL('mail_schema').query_db(query,data)

    @classmethod
    def get_mail_by_id(cls, id):
        query = 'SELECT * FROM mails WHERE id = %(id)s;'
        data = {'id':id}
        results = connectToMySQL('mail_schema').query_db(query, data)
        return results[0]

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM mails;'
        results = connectToMySQL('mail_schema').query_db(query)
        mails = []
        for mail in results:
            mails.append(cls(mail))
        return mails

    @classmethod
    def delete(cls, id):
        query = 'DELETE FROM mails WHERE id = %(id)s;'
        data = {'id': id}
        connectToMySQL('mail_schema').query_db(query, data)

    @staticmethod
    def mail_exists(mail):
        query = 'SELECT * FROM mails WHERE address = %(address)s'
        data = {'address': mail}
        results = connectToMySQL('mail_schema').query_db(query, data)
        if len(results) > 0:
            return True
        else:
            return False


    @staticmethod
    def validate_mail (mail):
        is_valid = True
        
        if not EMAIL_REGEX.match(mail['address']):
            flash('Invalid email address!', category = 'error')
            is_valid = False
        elif Mail.mail_exists(mail['address']):
            flash('Mail address already exists!', category = 'error')
            is_valid = False
        elif is_valid:
            flash(f'The email you entered {mail["address"]} is a VALID email address! Thank You!', category = 'success')
        return is_valid