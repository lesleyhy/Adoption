from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class User:
    def __init__(self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save( cls , data ):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s,%(email)s, %(password)s);"
        user_id = connectToMySQL('adoption_db').query_db( query, data)
        return user_id

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('adoption_db').query_db( query, data)
        if result:
            return cls(result[0])
        return False

    @classmethod
    def get_one_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s";
        results = connectToMySQL('adoption_db').query_db( query, data)
        if results:
            return cls(results[0])
        return False

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('adoption_db').query_db(query) 
        if results:
            all_users = []
            for people in results:
                all_users.append( cls(people) )
            return all_users
        return False

    @classmethod
    def update(cls,data):
        query = "UPDATE users SET first_name=%(first_name)s,last_name=%(last_name)s,email=%(email)s WHERE id=%(id)s"
        return connectToMySQL('adoption_db').query_db( query,data)
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM users WHERE id = %(id)s"
        return connectToMySQL('adoption_db').query_db( query,data)

    @staticmethod
    def validate(data):
        is_valid = True
        
        if len(data['first_name']) < 1:
            flash('First name is reqired', 'err_user_first_name')
            is_valid = False

        if len(data['last_name']) < 1:
            flash('Last name is reqired','err_user_last_name')
            is_valid = False

        if len(data['email']) < 1:
            flash('Email is reqired','err_user_email')
            is_valid = False
        elif not EMAIL_REGEX.match(data['email']): 
            flash('Invalid email address!','err_user_email')
            is_valid = False
        else:
            protential_user = User.get_one_by_email({'email' : data['email']})
            if protential_user:
                flash('Email is already taken!','err_user_email')
                is_valid = False

        if len(data['password']) < 1:
            flash('password not valid','err_user_password')
            is_valid = False

        if len(data['cfm_pw']) < 1:
            flash('confirm password needed','err_user_cfm_pw')
            is_valid = False
        elif data['password'] != data['cfm_pw']:
            flash('password not match','err_user_cfm_pw')
            is_valid = False

        return is_valid
    
    @staticmethod
    def validate_login(data):
        is_valid = True

        if len(data['email']) < 1:
            flash('Email is reqired','err_user_email_login')
            is_valid = False
        elif not EMAIL_REGEX.match(data['email']): 
            flash('Invalid email address!','err_user_email_login')
            is_valid = False
        else:
            protential_user = User.get_one_by_email({'email' : data['email']})
            if not protential_user:
                flash('Something wrong!','err_user_email_login')
                is_valid = False
            elif not bcrypt.check_password_hash(protential_user.password, data['password']):
                flash('Something wrong!!','err_user_email_login')
                is_valid = False
            else:
                session['user_id'] = protential_user.id

        if len(data['password']) < 1:
            flash('password is reqired','err_user_password_login')
            is_valid = False
        
        return is_valid