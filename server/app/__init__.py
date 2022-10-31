from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask
from flask_mongoengine import MongoEngine

from app.routes.examples import examples_blueprint
from app.routes.labels import labels_blueprint
from app.routes.models import models_blueprint
from app.routes.classification import classification_blueprint

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': os.getenv("DB"),
    'host': os.getenv("HOST"),
    'port': int(os.getenv("PORT"))
}
db = MongoEngine()
db.init_app(app)

app.register_blueprint(examples_blueprint)
app.register_blueprint(labels_blueprint)
app.register_blueprint(models_blueprint)
app.register_blueprint(classification_blueprint)

#######################################################
if __name__ == "__main__":
    app.run(debug=True)
