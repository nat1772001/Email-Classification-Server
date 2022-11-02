from bson import ObjectId
from flask import jsonify, request, Blueprint
from app.models.Model import Model
from app.models.Example import Example
from app.machine_learning import *

classification_blueprint = Blueprint('classification_blueprint', __name__)


@classification_blueprint.route('/classification', methods=['POST'])
def classify():
    data = request.get_json()
    model = Model.objects().order_by("-trained_at").first()
    model = json.loads(model.to_json())
    labels = predict(data, model.get("data_path"), model.get("model_path"))
    n = len(data)
    examples = []
    for i in range(n):
        email = data[i]
        label = labels[i]
        example = Example(
            sender=email.get("sender"),
            receiver=email.get("receiver"),
            subject=email.get("subject"),
            content=email.get("content"),
            date=email.get("date"),
            label=ObjectId(label[10:34]),
        )
        example.save()
        examples.append(example.populate_label())
    return jsonify(examples), 200
