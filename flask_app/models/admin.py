from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt 
from flask import flash       
bcrypt = Bcrypt(app)  
adminCode = "8d1s6a0807,456"
class Admin:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.password = data['password']


    @classmethod
    def save(cls,data):
        query = "INSERT INTO admins (name,email,password) VALUES (%(name)s,%(email)s,%(password)s);"
        return connectToMySQL('cowboyroofing').query_db(query,data)
    @classmethod
    def getByEmail(cls,data):
        query = "SELECT * FROM admins WHERE email = %(email)s;"
        results = connectToMySQL('cowboyroofing').query_db(query,data)
        return cls(results[0])
    @classmethod
    def getById(cls,data):
        query = "SELECT * FROM admins WHERE id = %(id)s;"
        results = connectToMySQL('cowboyroofing').query_db(query,data)
        return cls(results[0])
    @classmethod
    def update(cls,data):
        query = "UPDATE admins SET name=%(name)s,email=%(email)s,address=%(address)s,updated_at=NOW() WHERE id = %(id)s"
        return connectToMySQL('cowboyroofing').query_db(query,data)
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM admins WHERE id=%(id)s;"
        return connectToMySQL('cowboyroofing').query_db(query,data)
    @staticmethod
    def validate_admin(data):
        is_valid = True
        print(adminCode == data['adminCode'], adminCode, data['adminCode'])
        if adminCode != data['adminCode']:
            print('line 39')
            flash('invalid admin code',"logError")
            is_valid = False
        pAdmin = Admin.getByEmail({"email" : data['email']})
        print(pAdmin)
        if not pAdmin:
            print("here")
            flash('email does not exist',"logError")
            is_valid = False
            return is_valid
        if not bcrypt.check_password_hash(pAdmin.password,data['password']):
            print('line 44')
            flash('invalid cedentials',"logError")
            is_valid = False
        if not is_valid:
            return is_valid
        return pAdmin
    @staticmethod
    def validate_reg(data):
        is_valid = True
        print(adminCode == data['adminCode'], adminCode, data['adminCode'])
        if adminCode != data['adminCode']:
            print('line 39')
            flash('invalid admin code', "regError")
            is_valid = False
        if len(data['email']) < 5:
            is_valid = False
            flash('please enter a valid email', "regError")
        if data['password'] != data['confirmPassword']:
            is_valid = False
            flash('passwords do not match', "regError")
        return is_valid





