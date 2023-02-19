from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
mydb = 'recipies_db'
class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save_user(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(fname)s, %(lname)s, %(email)s,%(password)s);'
        return connectToMySQL(mydb).query_db(query,data)

    @staticmethod
    def validate_user(user):
        is_valid = True
        if not str.isalpha(user['fname']):
            flash('First name must be letters only')
            is_valid = False
        if not str.isalpha(user['lname']):
            flash('First name must be letters only')
            is_valid = False
        if len(user['fname']) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False
        if len(user['lname']) < 2:
            flash("Last name must be at least 2 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be 8 characters or greater.")
            is_valid = False
        if user['password'] != user['confpassword']:
            flash("Passwords do not match!")
            is_valid = False
        return is_valid
    
    @classmethod
    def get_by_email(cls, data):
        query = '''
        SELECT *
        FROM users
        WHERE email = %(email)s;
        '''
        result = connectToMySQL(mydb).query_db(query,data)

        if len(result) < 1:
            return False
        return cls(result[0])