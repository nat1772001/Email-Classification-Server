import datetime
import json
from pyexpat import model
from flask import Flask, jsonify, request
from flask_mongoengine import MongoEngine

import gensim
import pickle
from pyvi import ViTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn import metrics, linear_model


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
    trained_at = db.DateTimeField(default=datetime.datetime.utcnow)
    example_quantity = db.IntField()
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
####################################################################################
# label router


@app.route('/labels', methods=['GET'])
def get_labels():
    labels = Label.objects()
    return jsonify(labels), 200


@app.route('/labels/<id>', methods=['GET'])
def get_one_label(id: str):
    label = Label.objects.get_or_404(id=id)
    return jsonify(label), 200


@app.route('/labels', methods=['POST'])
def creat_label():
    body = request.get_json()
    label = Label(**body).save()
    return jsonify(label), 201


@app.route('/labels/<id>', methods=['PUT'])
def update_label(id):
    body = request.get_json()
    label = Label.objects.get_or_404(id=id)
    label.update(**body)
    return jsonify({"Message": f"Updated {str(label.id)}"}), 200


@app.route('/labels/<id>', methods=['DELETE'])
def delete_label(id):
    label = Label.objects.get_or_404(id=id)
    label.delete()
    return jsonify({"Message": f"Deleted {str(label.id)}"}), 200

####################################################################################

# Example routes


@app.route('/examples', methods=['GET'])
def get_examples():
    examples = Example.objects()
    return jsonify(examples), 200


@app.route('/examples/<id>', methods=['GET'])
def get_one_example(id: str):
    example = Example.objects.get_or_404(id=id)
    return jsonify(example), 200


@app.route('/examples', methods=['POST'])
def create_example():
    body = request.get_json()
    example = Example(**body).save()
    return jsonify(example), 201


@app.route('/examples/<id>', methods=['PUT'])
def update_example(id):
    body = request.get_json()
    example = Example.objects.get_or_404(id=id)
    example.update(**body)
    return jsonify({"Message": f"Updated {str(example.id)}"}), 200


@app.route('/examples/<id>', methods=['DELETE'])
def delete_example(id):
    example = Example.objects.get_or_404(id=id)
    example.delete()
    return jsonify({"Message": f"Deleted {str(example.id)}"}), 200

####################################################################################

# Model routes


@app.route('/models', methods=['GET'])
def get_models():
    models = Model.objects()
    preprocessing_data(models)
    return jsonify(models), 200


@app.route('/models/<id>', methods=['GET'])
def get_one_model(id: str):
    model = Model.objects.get_or_404(id=id)
    return jsonify(model), 200


@app.route('/models', methods=['POST'])
def create_model():
    examples = Example.objects()
    X_data, y_data = preprocessing_data(examples)
    X_data, y_data = feature_engineering(X_data, y_data)
    saved_model, acc_score, pre_score, rec_score, f1_score = train_model(X_data, y_data)
    model = Model(
        example_quantity=len(examples),
        path=saved_model,
        accuracy=acc_score,
        precision=pre_score,
        recall=rec_score,
        f1=f1_score
    ).save()
    return jsonify(model), 201


@app.route('/models/<id>', methods=['DELETE'])
def delete_model(id):
    model = Model.objects.get_or_404(id=id)
    model.delete()
    return jsonify({"Message": f"Deleted {str(model.id)}"}), 200

#######################################################
# Utils


def preprocessing_data(examples):
    X = []
    y = []
    for example in examples:
        data = json.loads(example.to_json())
        process_data = str(data.get("subject")) + ' ' + \
            str(data.get("content"))
        process_data = gensim.utils.simple_preprocess(process_data)
        process_data = ' '.join(process_data)
        process_data = ViTokenizer.tokenize(process_data)
        X.append(process_data)
        y.append(str(data.get("label")))
    return X, y


def feature_engineering(X_data, y_data):
    tfidf_vect_ngram = TfidfVectorizer(
        analyzer='word', max_features=30000, ngram_range=(2, 3))
    tfidf_vect_ngram.fit(X_data)
    X_data_tfidf_ngram = tfidf_vect_ngram.transform(X_data)

    encoder = LabelEncoder()
    y_data_n = encoder.fit_transform(y_data)

    return X_data_tfidf_ngram, y_data_n


def train_model(X_data, y_data):
    classifier = linear_model.LogisticRegression()
    X_train, X_test, y_train, y_test = train_test_split(
        X_data, y_data, test_size=0.3, random_state=42)
    classifier.fit(X_train, y_train)

    test_predictions = classifier.predict(X_test)

    acc = metrics.accuracy_score(y_test, test_predictions)
    pre = metrics.precision_score(y_test, test_predictions, average='micro')
    rec = metrics.recall_score(y_test, test_predictions, average='micro')
    f1 = metrics.f1_score(y_test, test_predictions, average='micro')

    saved_model = pickle.dumps(classifier)
    return saved_model, acc, pre, rec, f1


def eliminate_stopword(data):
    return data


#######################################################
if __name__ == "__main__":
    app.run(debug=True)
