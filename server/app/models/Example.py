from flask_mongoengine import MongoEngine

db = MongoEngine()

from app.models.Label import Label

class Example(db.Document):
    sender = db.StringField()
    receiver = db.StringField()
    subject = db.StringField()
    content = db.StringField()
    label = db.ReferenceField(Label)