from models.database import Database
from bson import json_util

class Student:

    def __init__(self):
        self.db = Database.instance().students

    def create_student(self, code, fullname, latitude, longitude):
        self.db.insert_one({
                        'code': code,
                        'fullname': fullname,
                        'location': {
                            'latitude': latitude,
                            'longitude': longitude
                        },
                        'status': False
                    })
    def update_status(self, student):
        new_status = not student['status']
        self.db.update_one({'_id': student['_id']}, {"$set": {'status': new_status}})
    
    def exist_with_code(self, code):
        return self.db.count_documents({ 'code': code }) > 0

    def get_all(self):
        return self.db.find()

    def find_by_code(self, code):
        data = self.db.find_one({ 'code': code})
        return data