from pickle import GET
from flask import Flask, jsonify, request
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'email_classification',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)
####################################################################################
class Model(db.Document):
    trainedAt = db.StringField()
    exampleQuantity = db.IntField()
    path = db.FileField()
    accuracy = db.FloatField()
    precision = db.FloatField()
    recall = db.FloatField()
    f1 = db.FloatField()

class Label(db.Document):
    label = db.StringField()

class Example(db.Document):
    sender = db.StringField()
    receiver = db.StringField()
    subject = db.StringField()
    content = db.StringField()
    label = db.ReferenceField(Label)

class User(db.Document):
    name = db.StringField()
    email = db.StringField()
####################################################################################
# Users routes
@app.route('/users', methods=['GET'])
def get_users():
    users = User.objects()
    return jsonify(users), 200


@app.route('/users/<id>', methods=['GET'])
def get_one_user(id: str):
    user = User.objects.get_or_404(id=id)
    return jsonify(user), 200

@app.route('/users', methods=['POST'])
def create_user():
    body = request.get_json()
    user = User(**body).save()
    return jsonify(user), 201

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    body = request.get_json()
    user = User.objects.get_or_404(id=id)
    user.update(**body)
    return jsonify({"Message": f"Updated {str(user.id)}" }), 200

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.objects.get_or_404(id=id)
    user.delete()
    return jsonify({"Message": f"Deleted {str(user.id)}" }), 200

###
# Model routes
@app.route('/models', methods=['GET'])
def get_models():
    models = Model.objects()
    return jsonify(models), 200


@app.route('/models/<id>', methods=['GET'])
def get_one_model(id: str):
    model = Model.objects.get_or_404(id=id)
    return jsonify(model), 200

@app.route('/models', methods=['POST'])
def create_model():
    body = request.get_json()
    model = Model(**body).save()
    return jsonify(model), 201

@app.route('/models/<id>', methods=['PUT'])
def update_model(id):
    body = request.get_json()
    model = Model.objects.get_or_404(id=id)
    model.update(**body)
    return jsonify({"Message": f"Updated {str(model.id)}" }), 200

@app.route('/models/<id>', methods=['DELETE'])
def delete_model(id):
    model = Model.objects.get_or_404(id=id)
    model.delete()
    return jsonify({"Message": f"Deleted {str(model.id)}" }), 200

####################################################################################
# label router  
@app.route('/labels', methods=['GET'])
def get_labels():
    label = Label.objects()
    return jsonify(label), 200


@app.route('/label/<id>', methods=['GET'])
def get_one_label(id: str):
    label = Label.objects.get_or_404(id=id)
    return jsonify(label), 200

@app.route('/label', methods=['POST'])
def creat_label():
    body = request.get_json()
    label = Label(**body).save()
    return jsonify(label), 201

@app.route('/label/<id>', methods=['PUT'])
def update_label(id):
    body = request.get_json()
    label = Label.objects.get_or_404(id=id)
    label.update(**body)
    return jsonify({"Message": f"Updated {str(label.id)}" }), 200

@app.route('/label/<id>', methods=['DELETE'])
def delete_label(id):
    label = Label.objects.get_or_404(id=id)
    label.delete()
    return jsonify({"Message": f"Deleted {str(label.id)}" }), 200

####################################################################################

# Example routes
@app.route('/example',methods=['GET'])
def get_example():
    example = Example.objects()
    return jsonify(example), 200


@app.route('/example/<id>', methods=['GET'])
def get_one_example(id: str):
    example = Example.objects.get_or_404(id=id)
    return jsonify(example), 200

@app.route('/example', methods=['POST'])
def create_example():
    body = request.get_json()
    example = Example(**body).save()
    return jsonify(example), 201

@app.route('/example/<id>', methods=['PUT'])
def update_example(id):
    body = request.get_json()
    example = Example.objects.get_or_404(id=id)
    example.update(**body)
    return jsonify({"Message": f"Updated {str(example.id)}" }), 200

@app.route('/example/<id>', methods=['DELETE'])
def delete_example(id):
    example = Example.objects.get_or_404(id=id)
    example.delete()
    return jsonify({"Message": f"Deleted {str(example.id)}" }), 200

#######################################################
if __name__ == "__main__":
    app.run(debug=True)