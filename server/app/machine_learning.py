import datetime
import json

import gensim
import pickle
from pyvi import ViTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn import metrics, linear_model

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

    now = (datetime.datetime.now()).strftime("%d_%m_%Y_%H_%M_%S")
    path = f'server/machine_learning_models/{now}.pkl'

    pickle.dump(classifier, open(path, 'wb'))
    return path, acc, pre, rec, f1