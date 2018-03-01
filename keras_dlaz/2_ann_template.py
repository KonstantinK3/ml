# Classification template

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('Churn_Modelling.csv')

X = dataset.iloc[:, 3:-1].values
y = dataset.iloc[:, -1].values

# Encoding categorical data
# Encoding the Independent Variable
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
labelencoder_X_1 = LabelEncoder()
X[:, 1] = labelencoder_X_1.fit_transform(X[:, 1]) #кодируется страна
labelencoder_X_2 = LabelEncoder()
X[:, 2] = labelencoder_X_2.fit_transform(X[:, 2]) #пол - присваивается 0 или 1, больше переделывать не надо
onehotencoder = OneHotEncoder(categorical_features = [1])
X = onehotencoder.fit_transform(X).toarray()
X = X[:, 1:] #один столбец категориальных данных можно убрать

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test) #фит уже сделан, нужен только трансформ

#ANN imports and init
import keras
from keras.models import Sequential
from keras.layers import Dense

classifier = Sequential()
classifier.add(Dense(output_dim = 6, init = 'uniform', activation='relu', input_dim=11))
classifier.add(Dense(output_dim = 6, init = 'uniform', activation='relu'))
classifier.add(Dense(output_dim = 1, init = 'uniform', activation='sigmoid'))
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics=['accuracy'])
classifier.fit(X_train, y_train, batch_size=10, epochs=100)

#make predicitons and evaluate
#за счет сигмоида рассчитывается вероятность наступления события 1 (ухода)
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
y_pred = (y_pred>0.5) #конвертирует в булевый массив с порогом 0,5

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

print(cm) #матрица успешных предсказаний
print((cm[0,0]+cm[1,1])/2000*100) #процент успешных предсказаний

# Predicting a single new observation
"""Predict if the customer with the following informations will leave the bank:
Geography: France
Credit Score: 600
Gender: Male
Age: 40
Tenure: 3
Balance: 60000
Number of Products: 2
Has Credit Card: Yes
Is Active Member: Yes
Estimated Salary: 50000"""
new_prediction = classifier.predict(sc.transform(np.array([[0.0, 0, 600, 1, 40, 3, 60000, 2, 1, 1, 50000]])))
print(new_prediction)
new_prediction = (new_prediction > 0.5)
print(new_prediction)
