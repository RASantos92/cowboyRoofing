from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

class RecentProject:
    def __init__(self,data):
        self.id = data['id']
        self.photos = []
        self.location = data['location']
        self.description = data['description']
        self.cost = data['cost']
        self.tCost = data['cost']
        self.mainPhoto = data['main_photo']
        self.allPhotosStr = data['photos']

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO recent_projects (photos,location,description,cost,main_photo) VALUES (%(photos)s,%(location)s,%(description)s,%(cost)s,%(mainPhoto)s)'
        return connectToMySQL('cowboyroofing').query_db(query,data)
    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM recent_projects WHERE id = %(id)s'
        return connectToMySQL('cowboyroofing').query_db(query,data)
    @classmethod
    def update(cls,data):
        query = "UPDATE recent_projects SET location = %(location)s,description = %(description)s,cost = %(cost)s,main_photo = %(mainPhoto)s,photos = %(allPhotos)s WHERE id = %(id)s"
        return connectToMySQL('cowboyroofing').query_db(query,data)
    @classmethod
    def getAll(cls):
        query = 'SELECT * FROM recent_projects'
        results = connectToMySQL('cowboyroofing').query_db(query)
        projects = []
        for row in results:
            project = cls(row)
            project.cost = cls.getProjectCost(project)
            pics = row['photos'].split(",")
            pics.pop(len(pics)-1)
            print(pics)
            for pic in pics:
                project.photos.append(pic)
            projects.append(project)
        return projects
    @classmethod
    def get_5(cls):
        query = 'SELECT * FROM recent_projects'
        results = connectToMySQL('cowboyroofing').query_db(query)
        projects = []
        counter = 5
        for row in results:
            project = cls(row)
            project.cost = cls.getProjectCost(project)
            pics = row['photos'].split(",")
            pics.pop(len(pics)-1)
            print(pics)
            for pic in pics:
                project.photos.append(pic)
            if counter < 6:
                projects.append(project)
        return projects
    @classmethod
    def get_one(cls,data):
        query = 'SELECT * FROM recent_projects WHERE id = %(id)s'
        results = connectToMySQL('cowboyroofing').query_db(query,data)
        project = cls(results[0])
        project.cost = cls.getProjectCost(project)
        pics = results[0]['photos'].split(",")
        if pics[len(pics)-1] == " ":
            pics.pop(len(pics)-1)
        print(pics)
        for pic in pics:
            if pic != "":
                project.photos.append(pic)
        return project    
    @staticmethod
    def getProjectCost(project):
        if len(str(project.cost)) > 3 and len(str(project.cost)) < 7:
            new_cost = f"{str(project.cost)[slice(0,(len(str(project.cost))-3))]}K"
            print(new_cost)
        if len(str(project.cost)) >= 8 and len(str(project.cost)) < 10:
            new_cost = f"{str(project.cost)[slice(0,(len(str(project.cost))-6))]}Mil"
            print(new_cost)
        if len(str(project.cost)) == 7:
            print(str(project.cost)[6])
            new_cost = f"{str(project.cost)[slice(0,(len(str(project.cost))-6))]}.{str(project.cost)[1]}Mil"
        return new_cost

# test = 80000000
# print()
# if len(str(test)) > 3 and len(str(test)) < 7:
#     print("here")
#     print(f"{str(test)[slice(0,(len(str(test))-3))]}K")
# if len(str(test)) >= 7 and len(str(test)) < 10:
#     print("here")
#     print(f"{str(test)[slice(0,(len(str(test))-6))]}Mil")
