from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
mydb = 'recipies_db'

class Recipie:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['recipie_name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.password = data['date_made']
        self.under_thrity = data['under_thrity']
        self.created_at = data['created_at']        
        self.updated_at = data['updated_at']
        self.creator = data['first_name']        

    @classmethod
    def save_recipie(cls, data):
        query = 'INSERT INTO recipies (recipie_name, description, instructions, date_made, under_thrity, created_at, updated_at, users_id) VALUES (%(recipie_name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_thirty)s,NOW(),NOW(),%(users_id)s);'
        return connectToMySQL(mydb).query_db(query,data)

    @staticmethod
    def validate_recipie(recipie):
        print (recipie)
        is_valid = True
        if len(recipie['recipie_name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        if len(recipie['description']) < 3:
            flash("Description must be at least 3 characters.")
            is_valid = False
        if len(recipie['instructions']) < 3:
            flash("Instructions must be at least 3 characters.")
            is_valid = False
        if recipie['date_made'] == '':
            flash("Must include date.")
            is_valid = False
        return is_valid

    @staticmethod
    def getAllRecipies():
        query = '''
        SELECT * FROM recipies
        LEFT JOIN users on users.id = recipies.users_id;
        '''
        return connectToMySQL(mydb).query_db(query)

    @classmethod
    def delete(cls, id):
        query = '''
        DELETE FROM recipies 
        WHERE id = %(id)s;
        '''
        return connectToMySQL(mydb).query_db(query,id)
    
    @classmethod
    def getRecipieByID(cls, id):
        query = '''
        SELECT *
        FROM recipies
        LEFT JOIN users on users.id = recipies.users_id
        WHERE recipies.id = %(id)s;
        
        '''
        results = connectToMySQL(mydb).query_db(query,id)
 
        return cls(results[0])

    @classmethod
    def edit(cls, id):
        query = '''
        UPDATE recipies
        SET recipie_name = %(recipie_name)s,
        description = %(description)s,instructions = %(instructions)s,
        date_made = %(date_made)s, under_thrity = %(under_thirty)s,
        updated_at = NOW()
        WHERE id = %(id)s;
        '''
        return connectToMySQL(mydb).query_db(query,id)