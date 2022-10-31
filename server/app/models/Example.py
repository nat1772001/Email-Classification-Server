from app.models.Label import Label
from flask_mongoengine import MongoEngine

db = MongoEngine()


class Example(db.Document):
    sender = db.StringField()
    receiver = db.StringField()
    subject = db.StringField()
    content = db.StringField()
    label = db.ReferenceField(Label)

    def populate_label(self):
        result = {
            'sender': self.sender,
            'receiver': self.receiver,
            'subject': self.subject,
            'content': self.content,
        }
        result['label'] = self.label.label
        return result
