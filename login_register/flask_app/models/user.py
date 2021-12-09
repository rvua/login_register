from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = 'login_registration_schema'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def save_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW())"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_users(cls):
        query = "SELECT * FROM users"
        results = connectToMySQL(cls.db).query_db(query)
        user = []
        for r in results:
            user.append(cls(r)) 
        return user 
    
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False 
        return cls(results[0])
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])
    
    @staticmethod
    def is_valid_registration(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(User.db).query_db(query,user)
        if len(results) > 1:
            flash('This email is already taken, please enter another', 'registration')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('This email is invalid', 'registration')
            is_valid = False
        if len(user['first_name']) < 2:
            flash('Your first name must be at least 2 characters long', 'registration')
            is_valid = False
        if len(user['last_name']) < 2:
            flash('Your last name must be at least 2 characters long', 'registration')
            is_valid = False
        if len(user['password']) < 4:
            flash('Your password must be at least 4 characters long', 'registration')
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash('The password you entered does not match up', 'registration')
        return is_valid