from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

class Certification:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.photo = data['photo']



    @classmethod
    def add(cls,data):
        query = "INSERT INTO certifications (name,description,photo) VALUES (%(name)s, %(description)s,%(photo)s)"
        return connectToMySQL('cowboyroofing').query_db(query,data)
    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM certifications WHERE id = %(id)s'
        return connectToMySQL('cowboyroofing').query_db(query,data)
    @classmethod
    def getAll(cls):
        query = "SELECT * FROM certifications;"
        results = connectToMySQL('cowboyroofing').query_db(query)
        certifications = []
        for x in results:
            certifications.append(cls(x))
        return certifications
