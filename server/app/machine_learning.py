import os
import json

import gensim
import pickle
from pyvi import ViTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn import metrics, linear_model

def preprocessing_data(examples, now):
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
    pickle.dump(X, open(f'{os.getenv("TRAIN_DATA_PATH")}/{now}.pkl','wb'))
    return X, y


def feature_engineering(X_data, y_data):
    tfidf_vect_ngram = TfidfVectorizer(
        analyzer='word', max_features=30000, ngram_range=(2, 3))
    tfidf_vect_ngram.fit(X_data)
    X_data_tfidf_ngram = tfidf_vect_ngram.transform(X_data)

    return X_data_tfidf_ngram, y_data


def train_model(X_data, y_data, now):
    classifier = linear_model.LogisticRegression()
    X_train, X_test, y_train, y_test = train_test_split(
        X_data, y_data, test_size=0.3, random_state=42)
    classifier.fit(X_train, y_train)

    test_predictions = classifier.predict(X_test)

    acc = metrics.accuracy_score(y_test, test_predictions)
    pre = metrics.precision_score(y_test, test_predictions, average='micro')
    rec = metrics.recall_score(y_test, test_predictions, average='micro')
    f1 = metrics.f1_score(y_test, test_predictions, average='micro')

    pickle.dump(classifier, open(f'{os.getenv("TRAIN_MODEL_PATH")}/{now}.pkl', 'wb'))
    return acc, pre, rec, f1


def preprocessing_X(data):
    # preprocess X
    X_data = []
    for email in data:
        process_data = str(email.get("subject")) + ' ' + str(email.get("content"))
        process_data = gensim.utils.simple_preprocess(process_data)
        process_data = ' '.join(process_data)
        process_data = ViTokenizer.tokenize(process_data)

        X_data.append(process_data)

    return X_data


def predict(data, data_path, model_path):
    saved_data = pickle.load(open(data_path, 'rb'))
    saved_model = pickle.load(open(model_path, 'rb'))
    X_data = preprocessing_X(data)
    
    tfidf_vect_ngram = TfidfVectorizer(
        analyzer='word', max_features=30000, ngram_range=(2, 3))
    tfidf_vect_ngram.fit(saved_data)
    X_data_tfidf_ngram = tfidf_vect_ngram.transform(X_data)

    y_predict = saved_model.predict(X_data_tfidf_ngram)
    return y_predict

