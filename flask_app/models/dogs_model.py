from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import user_model

class Dog:
    def __init__(self , data ):
        self.id = data['id']
        self.name = data['name']
        self.age = data['age']
        self.sex = data['sex']
        self.color = data['color']
        self.breed = data['breed']
        self.health = data['health']
        self.other_info = data['other_info']
        self.pic = data['pic']
        self.location = data['location']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.post = {}

    @classmethod
    def save( cls , data ):
        query = "INSERT INTO dogs (name, age, sex,color,breed,health,other_info,pic,location,user_id) VALUES (%(name)s, %(age)s,%(sex)s,%(color)s,%(breed)s,%(health)s,%(other_info)s,%(pic)s,%(location)s, %(user_id)s);"
        user_id = connectToMySQL('adoption_db').query_db( query, data)
        return user_id

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM dogs JOIN users ON dogs.user_id = users.id WHERE dogs.id = %(id)s";
        results = connectToMySQL('adoption_db').query_db( query, data)
        if results:
            dog = cls(results[0])
            user_data = {
                    'id':results[0]['users.id'],
                    'created_at':results[0]['users.created_at'],
                    'updated_at':results[0]['users.updated_at'],
                    'first_name':results[0]['first_name'],
                    'last_name':results[0]['last_name'],
                    'email':results[0]['email'],
                    'password':results[0]['password'],
                }
            user = user_model.User(user_data)
            dog.post = user
            return dog
        return []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dogs JOIN users ON dogs.user_id = users.id;"
        results = connectToMySQL('adoption_db').query_db(query) 
        if results:
            all_dogs = []
            for dict in results:
                dog = cls(dict)
                user_data = {
                    'id':dict['users.id'],
                    'created_at':dict['users.created_at'],
                    'updated_at':dict['users.updated_at'],
                    'first_name':dict['first_name'],
                    'last_name':dict['last_name'],
                    'email':dict['email'],
                    'password':dict['password'],
                }
                user1 = user_model.User(user_data)
                dog.post = user1

                all_dogs.append(dog)
            return all_dogs
        return []

    @classmethod
    def update(cls,data):
        query = "UPDATE dogs SET name=%(name)s,age=%(age)s,sex=%(sex)s,color=%(color)s,breed=%(breed)s,health=%(health)s,other_info=%(other_info)s,pic=%(pic)s,location=%(location)s WHERE id=%(id)s"
        return connectToMySQL('adoption_db').query_db( query,data)
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM dogs WHERE id = %(id)s"
        return connectToMySQL('adoption_db').query_db(query,data)