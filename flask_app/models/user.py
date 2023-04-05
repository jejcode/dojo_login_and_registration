from flask_app.config.mysqlconnection import connectToMySQL # import function to connect to database
from flask import flash # flash stores messages for form validation
from datetime import datetime,date

import re # import regex to validate email
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') # string to ensure valid email address
PASS_REGEX = re.compile(r'^(?!^[0-9]*$)(?!^[a-zA-Z]*$)^([a-zA-Z0-9!@#$%^&*()]{8,})$') # string to check password for letters and numbers
class User:
    DB = 'login_and_registration_schema'
    def __init__(self, data) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.birthday = data['birthday']
        self.fav_lang = data['fav_lang']
        self.fav_os = data['fav_os']
        self.strategies = data['strategies']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    # Class methods for CRUD
    # CREATE
    @classmethod
    def add_new_user(cls, data): # query to add user to users table
        query = """INSERT INTO users (first_name, last_name, email, password, birthday, fav_lang, fav_os, strategies)
                VALUES (%(fname)s, %(lname)s, %(email)s, %(password)s, %(birthday)s, %(lang)s, %(os)s, %(strategies)s)"""
        return connectToMySQL(cls.DB).query_db(query, data) # returns id of new user
    # READ
    @classmethod
    def get_user_data(cls,data):
        query = "SELECT * FROM users WHERE id=%(id)s"
        results = connectToMySQL(cls.DB).query_db(query, data) # results is a single item list
        return cls(results[0]) # create instance of result and return it
    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email=%(email)s"
        results = connectToMySQL(cls.DB).query_db(query, data) # returns a list of 1 (or 0 if null)
        if len(results) < 1:
            return 0
        return cls(results[0]) # create instance of user and return it
    # Static methods for validation
    @staticmethod
    def determine_age(birthday): # function found at https://www.geeksforgeeks.org/python-program-to-calculate-age-in-year/
        if not birthday:
            return False
        today = date.today()
        birthday = datetime.strptime(birthday, '%Y-%m-%d')
        age = today.year - birthday.year 
        # compare months, then days in tuple
        # True = 1 and False = 0. So if this statement is true, it's value becomes one
        - ((today.month,today.day) < (birthday.month,birthday.day))
        return age
    @staticmethod
    def validate_registration(data): # all validations for registration form
        is_valid = True
        if len(data['fname']) < 3:
            flash('First name must have at least 3 characters.', 'registration')
            is_valid = False
        if len(data['lname']) < 3:
            flash('Last name must have at least 3 characters.', 'registration')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): 
            flash('Invalid email address!', 'registration')
            is_valid = False
        if User.get_user_by_email({'email': data['email']}):
            flash('Email is already in use.', 'registration')
            is_valid = False
        if not PASS_REGEX.match(data['password']):
            flash('Password must contain at least one letter, one number, and be at least 8 characters long.', 'registration')
            is_valid = False
        if data['confirm_password'] != data['password']:
            flash('Password does not match confirm password', 'registration')
            is_valid = False
        if User.determine_age(data['birthday']) < 10:
            flash('Must be 10 years or older to join.', 'registration')
            is_valid = False
        if len(data['lang']) < 2:
            flash('A favorite langauge must be selected.', 'registration')
            is_valid = False
        if 'os' not in data:
            flash('An operating system must be selected.', 'registration')
            is_valid = False
        if 'strat1' not in data and 'strat2' not in data and 'strat3' not in data and 'strat4' not in data:
            flash('At least one learning strategy must be selected.', 'registration')
            is_valid = False
        return is_valid
    @staticmethod
    def validate_login(data):
        pass