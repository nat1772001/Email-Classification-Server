from flask import jsonify, request, Blueprint
from app.models.Label import Label

labels_blueprint = Blueprint('labels_blueprint', __name__)

@labels_blueprint.route('/labels', methods=['GET'])
def get_labels():
    labels = Label.objects()
    return jsonify(labels), 200


@labels_blueprint.route('/labels/<id>', methods=['GET'])
def get_one_label(id: str):
    label = Label.objects.get_or_404(id=id)
    return jsonify(label), 200


@labels_blueprint.route('/labels', methods=['POST'])
def creat_label():
    body = request.get_json()
    label = Label(**body).save()
    return jsonify(label), 201


@labels_blueprint.route('/labels/<id>', methods=['PUT'])
def update_label(id):
    body = request.get_json()
    label = Label.objects.get_or_404(id=id)
    label.update(**body)
    return jsonify({"Message": f"Updated {str(label.id)}"}), 200


@labels_blueprint.route('/labels/<id>', methods=['DELETE'])
def delete_label(id):
    label = Label.objects.get_or_404(id=id)
    label.delete()
    return jsonify({"Message": f"Deleted {str(label.id)}"}), 200