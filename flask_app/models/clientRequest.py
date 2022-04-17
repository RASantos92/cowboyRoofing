from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

class ClientRequest:
    def __init__(self,data):
        self.id = data['id']
        self.clientName = data['name']
        self.email = data['email']
        self.phone = data['phone']
        self.message = data['message']
        self.opened_request = data['opened_request']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO requests (name,email,phone,message) VALUES (%(name)s,%(email)s,%(phone)s,%(message)s);"
        return connectToMySQL('cowboyroofing').query_db(query,data)
    @classmethod
    def getById(cls,data):
        query = "SELECT * FROM requests WHERE id = %(id)s;"
        results = connectToMySQL('cowboyroofing').query_db(query,data)
        return cls(results[0])
    @classmethod
    def markOpen(cls,data):
        query = "UPDATE requests SET opened_request = 1,updated_at = NOW() WHERE id = %(id)s"
        return connectToMySQL('cowboyroofing').query_db(query,data)
    @classmethod
    def getall(cls):
        query="SELECT * FROM requests"
        results = connectToMySQL('cowboyroofing').query_db(query)
        requests = []
        for x in results:
            requests.append(cls(x))
        return requests
    @staticmethod
    def validate_request(data):
        is_valid=True
        if len(data['name']) == 0:
            flash( 'Please enter your name')
            is_valid=False
        if len(data['phone']) < 8:
            flash('Please enter a phone number')
            is_valid = False
        # Need to validate with regex
        if len(data['email']) == 0:
            flash('Please enter an email')
            is_valid=False
        return is_valid