import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

# Importing the dataset
dataset = pd.read_csv("train.csv")

y = dataset.iloc[:, 1].values #Survived
X = dataset.iloc[:, [2, 4, 5, 6, 7]].values #Pclass, Sex, Age, SibSp, Parch

for i in range(len(X[:,2])):
    if (X[:,2][i] != X[:,2][i]):
        X[:,2][i] = 0

# Encoding categorical data
# Encoding the Independent Variable
labelencoder_X_gender = LabelEncoder()
X[:, 1] = labelencoder_X_gender.fit_transform(X[:, 1]) #пол - присваивается 0 или 1, больше переделывать не надо

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.01, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test) #фит уже сделан, нужен только трансформ

#ANN imports and init
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout

classifier = Sequential()
classifier.add(Dense(output_dim = 20, init = 'uniform', activation='relu', input_dim=5))
#добавление дропаута в районе 0,1-0,3 
classifier.add(Dropout(p = 0.1))
classifier.add(Dense(output_dim = 50, init = 'uniform', activation='relu'))
classifier.add(Dense(output_dim = 1, init = 'uniform', activation='sigmoid'))
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics=['accuracy'])
classifier.fit(X_train, y_train, batch_size=10, epochs=100)

#make predicitons and evaluate
#за счет сигмоида рассчитывается вероятность наступления события 1 (выживания)
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
y_pred = (y_pred>0.5) #конвертирует в булевый массив с порогом 0,5

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

print(cm) #матрица успешных предсказаний
print((cm[0,0]+cm[1,1])/np.sum(cm)*100) #процент успешных предсказаний

#---------------test dataset-------------------

test_dataset = pd.read_csv("test.csv")
Z = test_dataset.iloc[:, [1, 3, 4, 5, 6]].values #Pclass, Sex, Age, SibSp, Parch
Z_numbers = test_dataset.iloc[:, 0].values #PassengerId

for i in range(len(Z[:,2])):
    if (Z[:,2][i] != Z[:,2][i]):
        Z[:,2][i] = 0

# Encoding the Independent Variable
labelencoder_X_gender = LabelEncoder()
Z[:, 1] = labelencoder_X_gender.fit_transform(Z[:, 1]) #пол - присваивается 0 или 1, больше переделывать не надо

# Feature Scaling
Z = sc.transform(Z) #фит уже сделан, нужен только трансфор

#Predict
z_pred = classifier.predict(Z)
z_pred = (z_pred>0.5)
z_pred = z_pred.astype(int) #convert to 0 and 1
z_res = np.zeros((418,2))
z_res[:,0] = Z_numbers
z_res[:,1] = z_pred[:,0]
z_res = z_res.astype(int)
np.savetxt("answer.csv", z_res, fmt='%.f', delimiter=",")
