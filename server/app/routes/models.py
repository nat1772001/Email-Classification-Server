from flask import jsonify, request, Blueprint
from app.models.Model import Model
from app.models.Example import Example
from app.machine_learning import *

models_blueprint = Blueprint('models_blueprint', __name__)

@models_blueprint.route('/models', methods=['GET'])
def get_models():
    models = Model.objects()
    preprocessing_data(models)
    return jsonify(models), 200


@models_blueprint.route('/models/<id>', methods=['GET'])
def get_one_model(id: str):
    model = Model.objects.get_or_404(id=id)
    return jsonify(model), 200


@models_blueprint.route('/models', methods=['POST'])
def create_model():
    examples = Example.objects()
    X_data, y_data = preprocessing_data(examples)
    X_data, y_data = feature_engineering(X_data, y_data)
    path, acc_score, pre_score, rec_score, f1_score = train_model(
        X_data, y_data)
    model = Model(
        example_quantity=len(examples),
        path=path,
        accuracy=acc_score,
        precision=pre_score,
        recall=rec_score,
        f1=f1_score
    ).save()
    return jsonify(model), 201


@models_blueprint.route('/models/<id>', methods=['DELETE'])
def delete_model(id):
    model = Model.objects.get_or_404(id=id)
    model.delete()
    return jsonify({"Message": f"Deleted {str(model.id)}"}), 200