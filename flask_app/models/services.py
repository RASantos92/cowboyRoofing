from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

class Services:
    def __init__(self,data):
        self.serv1info = data['serv1info']
        self.serv2info = data['serv2info']
        self.serv3info = data['serv3info']
        self.serv4info = data['serv4info']
        self.serv1photo = data['serv1photo']
        self.serv2photo = data['serv2photo']
        self.serv3photo = data['serv3photo']
        self.serv4photo = data['serv4photo']
        self.serv1 = data['serv1']
        self.serv2 = data['serv2']
        self.serv3 = data['serv3']
        self.serv4 = data['serv4']



    @classmethod
    def update(cls,data):
        query = "UPDATE services SET serv1info = %(serv1info)s,serv2info = %(serv2info)s, serv3info = %(serv3info)s,serv4info = %(serv4info)s, serv4 = %(serv4)s , serv2 = %(serv2)s , serv3 = %(serv3)s , serv1 = %(serv1)s, serv1photo = %(file1)s,serv2photo = %(file2)s, serv3photo = %(file3)s, serv4photo = %(file4)s WHERE id = 2"
        return connectToMySQL('cowboyroofing').query_db(query,data)
    @classmethod
    def getInfo(cls):
        query = "SELECT * FROM services WHERE id = 2;"
        results = connectToMySQL('cowboyroofing').query_db(query)
        return cls(results[0])