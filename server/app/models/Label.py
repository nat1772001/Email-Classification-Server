from flask_mongoengine import MongoEngine

db = MongoEngine()

class Label(db.Document):
    label = db.StringField()