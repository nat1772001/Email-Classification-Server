from flask import Flask
from flask_mongoengine import MongoEngine

from app.routes.examples import examples_blueprint
from app.routes.labels import labels_blueprint
from app.routes.models import models_blueprint

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'email_classification',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)

app.register_blueprint(examples_blueprint)
app.register_blueprint(labels_blueprint)
app.register_blueprint(models_blueprint)

# @app.route('/predict', methods=['GET'])
# def predict_example():
#     data = request.get_json()
#     label = predict(data)
#     example = Example(
#         sender=data.get("sender"),
#         receiver=data.get("receiver"),
#         subject=data.get("subject"),
#         content=data.get("content"),
#         label= ObjectId(label)
#     ).save()
#     return jsonify(example), 200

#######################################################
# Utils


# def preprocessing_data(examples):
#     X = []
#     y = []
#     for example in examples:
#         data = json.loads(example.to_json())
#         process_data = str(data.get("subject")) + ' ' + \
#             str(data.get("content"))
#         process_data = gensim.utils.simple_preprocess(process_data)
#         process_data = ' '.join(process_data)
#         process_data = ViTokenizer.tokenize(process_data)
#         X.append(process_data)
#         y.append(str(data.get("label")))
#     return X, y


# def feature_engineering(X_data, y_data):
#     tfidf_vect_ngram = TfidfVectorizer(
#         analyzer='word', max_features=30000, ngram_range=(2, 3))
#     tfidf_vect_ngram.fit(X_data)
#     X_data_tfidf_ngram = tfidf_vect_ngram.transform(X_data)

#     encoder = LabelEncoder()
#     y_data_n = encoder.fit_transform(y_data)

#     return X_data_tfidf_ngram, y_data_n


# def train_model(X_data, y_data):
#     classifier = linear_model.LogisticRegression()
#     X_train, X_test, y_train, y_test = train_test_split(
#         X_data, y_data, test_size=0.3, random_state=42)
#     classifier.fit(X_train, y_train)

#     test_predictions = classifier.predict(X_test)

#     acc = metrics.accuracy_score(y_test, test_predictions)
#     pre = metrics.precision_score(y_test, test_predictions, average='micro')
#     rec = metrics.recall_score(y_test, test_predictions, average='micro')
#     f1 = metrics.f1_score(y_test, test_predictions, average='micro')

#     now = (datetime.datetime.now()).strftime("%d_%m_%Y_%H_%M_%S")
#     path = f'models/{now}.pkl'

#     id = '6345b1d1b79b60e89fb93f15'

#     examples = Example.objects()

#     result = classifier.predict(preprocessing_X(examples))

#     print(result, len(result))

#     # pickle.dumps(classifier, open(path, 'wb'))
#     return path, acc, pre, rec, f1


# def preprocessing_X(data):
#     # preprocess X
#     X_data = []
#     for email in data:
#         email = json.loads(email.to_json())
#         process_data = str(email.get("subject")) + ' ' + str(email.get("content"))
#         process_data = gensim.utils.simple_preprocess(process_data)
#         process_data = ' '.join(process_data)
#         process_data = ViTokenizer.tokenize(process_data)

#         X_data.append(process_data)

#     # feature engineering X
#     tfidf_vect_ngram = TfidfVectorizer(
#         analyzer='word', max_features=30000, ngram_range=(2, 3))
#     tfidf_vect_ngram.fit(X_data)
#     X_data_tfidf_ngram = tfidf_vect_ngram.transform(X_data)
#     return X_data_tfidf_ngram


# def predict(example):
#     model = Model.objects().order_by('-trained_at').first()
#     model = json.loads(model.to_json())
#     saved_model = pickle.loads(model.get("path"))
#     data = json.loads(example.to_json())
#     X_predict = preprocessing_X(data)
#     y_predict = saved_model.predict(X_predict)
#     return y_predict[0]


# def eliminate_stopword(data):
#     return data


#######################################################
if __name__ == "__main__":
    app.run(debug=True)
