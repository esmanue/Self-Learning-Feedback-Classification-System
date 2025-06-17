import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix, accuracy_score
from utils import clean_data
import pickle

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')


def clean_data(data):
    data=data.lower()

    data = re.sub(r'[^a-zA-Z0-9\s]', '', data) #özel  karakteri temizler
    
    stop_words = set(stopwords.words('english'))#gereksiz sözcüklerden kurtarır
    not_stopword=["not", "no", "never", "doesn't", "isn't", "don't", "wasn't", "won't", "didn't","can't"]

    for word in not_stopword:
        stop_words.discard(word)

    lemmatizer = WordNetLemmatizer() #kelimeyi kökenlerine indirger
    
    words = nltk.word_tokenize(data) #kelime kelime ayırır
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    clean_data = ' '.join(words)

    return clean_data



df=pd.read_csv("amazon.csv")
print(df.head(10))
print(df.shape)
print(df.size)

df['clean_data']=df['Text'].apply(clean_data)

X=df['clean_data']
Y=df['label']


X_train, X_test, Y_train, Y_test =train_test_split(X,Y, test_size=0.2,random_state=4)


vectorizer = TfidfVectorizer(max_features=10000, ngram_range=(1,2))
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

#support vector classifier
classifier=svm.SVC(kernel='linear',gamma='auto',C=2)
classifier.fit(X_train_vec,Y_train)
y_predict=classifier.predict(X_test_vec)

#karsılastırma yaptıgımız yer
classification_report(Y_test,y_predict)
print(classification_report(Y_test, y_predict))

print("Accuracy:", accuracy_score(Y_test, y_predict))
print("Confusion Matrix:\n", confusion_matrix(Y_test, y_predict))
print("Classification Report:\n", classification_report(Y_test, y_predict))

import os

with open("classifier.pkl", "wb") as f:
    pickle.dump(classifier, f)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)
