from flask import jsonify, request, Blueprint
from app.models.Example import Example

examples_blueprint = Blueprint('examples_blueprint', __name__)


@examples_blueprint.route('/examples', methods=['GET'])
def get_examples():
    examples = []
    for example in Example.objects[:100]:
        examples.append(example.populate_label())
    return jsonify(examples), 200


@examples_blueprint.route('/examples/<id>', methods=['GET'])
def get_one_example(id: str):
    example = Example.objects.get_or_404(id=id)
    return jsonify(example), 200


@examples_blueprint.route('/examples', methods=['POST'])
def create_example():
    body = request.get_json()
    example = Example(**body).save()
    return jsonify(example), 201


@examples_blueprint.route('/examples/<id>', methods=['PUT'])
def update_example(id):
    body = request.get_json()
    example = Example.objects.get_or_404(id=id)
    example.update(**body)
    return jsonify({"Message": f"Updated {str(example.id)}"}), 200


@examples_blueprint.route('/examples/<id>', methods=['DELETE'])
def delete_example(id):
    example = Example.objects.get_or_404(id=id)
    example.delete()
    return jsonify({"Message": f"Deleted {str(example.id)}"}), 200
