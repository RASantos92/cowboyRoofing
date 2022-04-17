from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

class DSAinfo:
    def __init__(self,data):
        self.address = data['address']
        self.email = data['email']
        self.phone = data['phone']
        self.linkedin = data['linkedin']
        self.siteVideo = data['site_video']
        self.facebook = data['facebook']
        self.siteVisits = data['site_visits']


    @classmethod
    def update(cls,data):
        query = "UPDATE dsa_info SET address = %(address)s,email = %(email)s,phone = %(phone)s,linkedin = %(linkedin)s,facebook = %(facebook)s, site_video = %(siteVideo)s WHERE id = 2"
        return connectToMySQL('cowboyroofing').query_db(query,data)
    @classmethod
    def getInfo(cls):
        query = "SELECT * FROM dsa_info WHERE id = 2;"
        results = connectToMySQL('cowboyroofing').query_db(query)
        return cls(results[0])
    @classmethod
    def addVisit(cls):
        obj = cls.getInfo()
        visits = obj.siteVisits + 1
        data = {
            "visits" : visits
        }
        query = "UPDATE dsa_info SET site_visits = %(visits)s WHERE id = 2"
        return connectToMySQL('cowboyroofing').query_db(query,data)
        