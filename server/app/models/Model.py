from flask_mongoengine import MongoEngine
import datetime

db = MongoEngine()

class Model(db.Document):
    trained_at = db.DateTimeField(default=datetime.datetime.utcnow)
    example_quantity = db.IntField()
    data_path = db.StringField()
    model_path = db.StringField()
    accuracy = db.FloatField()
    precision = db.FloatField()
    recall = db.FloatField()
    f1 = db.FloatField()