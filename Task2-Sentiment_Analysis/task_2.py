# -*- coding: utf-8 -*-
"""Task 2

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/164vJk7I9G3_yk_WzS7Yzp3-qGXR6S1DK
"""

import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from sklearn.metrics import classification_report,confusion_matrix,accuracy_score
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LogisticRegression as LR
from sklearn.metrics import cohen_kappa_score
from sklearn.preprocessing import LabelEncoder
import numpy as np

from google.colab import drive

drive.mount('/content/gdrive')

val=pd.read_csv(r'/content/gdrive/My Drive/csv/twitter_validation.csv', header=None)
#full dataset for train-test
train=pd.read_csv(r'/content/gdrive/My Drive/csv/twitter_training.csv', header=None)

nltk.download("stopwords")
stop_words = [elements.lower() for elements in set(stopwords.words("english"))]

# Giving columns understandible names
train.rename(columns={2:"labels",1:"names",3:"tweets"}, inplace=True)

y = train["labels"]
X = train["tweets"]

X

print(len(y))
print(len(X))

y.value_counts()

# Encoding labels name using label encoder from sklearn.preprocessing
encoder = LabelEncoder()
y = encoder.fit_transform(y)

np.unique(y)

np.unique(encoder.inverse_transform(y))

# Lowering text (tweets) and  replacing any extra/special/digits from tweets using regex
X = X.str.lower()
X.replace("[^a-zA-Z]"," ", regex=True, inplace=True)
X.head()

# Removing stop words from the tweets
def remove_stop (x):
    return ",".join([words for words in str(x).split() if words not in stop_words])

X = X.apply(lambda x: remove_stop(x))
X.head()

X_train, X_test, y_train, y_test = train_test_split(X,y,
    test_size=0.2,shuffle = True, random_state = 42)

print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

# creating array/list of the tweets (train and test)
x_train_array = []
for row in range(0, len(X_train.index)):
    x_train_array.append("".join(x for x in X_train.iloc[row] ))
    
    
x_test_array = []
for row in range (0, len(X_test.index)):
    x_test_array.append("".join(x for x in X_test.iloc[row]))

# converting arrays of tweets into vector form
tfidfvector = TfidfVectorizer()
tfidf_train_dataset = tfidfvector.fit_transform(x_train_array)
tfidf_test_dataset = tfidfvector.transform(x_test_array)

"""Logistic Regression Model"""

# Model decleration
lr_model = LR(C=10.0, max_iter=100,
                penalty='l2',
                   random_state=10, solver='liblinear' )

# training the model
lr_model.fit(tfidf_train_dataset,y_train)

# testing the model
predictions = lr_model.predict(tfidf_test_dataset)

matrix=confusion_matrix(y_test,predictions)
print(matrix)
score=accuracy_score(y_test,predictions)
print(score)
report=classification_report(y_test,predictions)
print(report)
kappa = cohen_kappa_score(y_test, predictions)
print(kappa)

"""Testing the Model"""

test =  ["Its ok eluno musk given every one a good space to talk","I am ok whatever people will say about anyone","It depends on peoples mind set how they talk either dirty or good mind","pakistans politicians are not doing good job in their country"]
tes = tfidfvector.transform(test)

pre = lr_model.predict(tes)

print(encoder.inverse_transform(pre))

from sklearn.ensemble import RandomForestClassifier

forest_model = RandomForestClassifier()
forest_model.fit(tfidf_train_dataset, y_train)

prediction = forest_model.predict(tfidf_test_dataset)

matrix=confusion_matrix(y_test,predictions)
print(matrix)
score=accuracy_score(y_test,predictions)
print(score)
report=classification_report(y_test,predictions)
print(report)
kappa = cohen_kappa_score(y_test, predictions)
print(kappa)

