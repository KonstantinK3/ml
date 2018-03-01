# Recurrent Neural Network

# Part 1 - Data Preprocessing

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the training set
dataset = pd.read_csv('data.csv')

series = dataset.iloc[:, 1:2].values #create a matrix, not a vector

from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range= (0,1))
series = sc.fit_transform(series)
X_train = series[0:1258]
y_train = series[1:1259]
X_test = series[1258:]

X_train = X_train.reshape(1258,1,1)
X_test = X_test.reshape(20,1,1)

from keras.models import Sequential
from keras.layers import Dense, LSTM

regressor = Sequential()

regressor.add(LSTM(input_shape=(None, 1), units=3, activation="sigmoid"))
regressor.add(Dense(units = 1, activation = 'tanh'))
regressor.compile(optimizer='rmsprop', loss = 'mean_squared_error')
regressor.fit(X_train, y_train, epochs = 1000, batch_size = 32)

training_set_pred = regressor.predict(X_train)
training_set_pred = sc.inverse_transform(training_set_pred)

test_set_pred = regressor.predict(X_test)
test_set_pred = sc.inverse_transform(test_set_pred)

real_results = sc.inverse_transform(series)
predicition = np.concatenate((training_set_pred, test_set_pred), axis=0)

plt.plot(real_results, color='red', label='real prices')
plt.plot(predicition, color='blue', label='predicted')
plt.title('predicitions for stock prices')
plt.xlabel('Time')
plt.ylabel('prices')
plt.legend()
plt.show()
#plt.savefig('1.png')