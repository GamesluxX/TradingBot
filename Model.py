import sklearn
from keras.models import Sequential
from keras.layers import Dense
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler


class ModelDevelopment():
    def __init__(self):
        self.raw_data = pd.read_csv('src/dax_history_data.csv')
        self.raw_data = self.raw_data.dropna()
        X = self.raw_data[['Monday','Tuesday','Wednesday','Thursday']]
        scaler = MinMaxScaler()
        scaler.fit(X)
        X = scaler.transform(X)
        X = pd.DataFrame(X)

        Y = self.raw_data['y']

        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33)
        network = Sequential()

        network.add(Dense(4, input_shape=(4,), activation='tanh'))
        network.add(Dense(4, activation='tanh'))
        network.add(Dense(1, activation='tanh'))

        # Compile the model
        network.compile(
            optimizer='rmsprop',
            loss='hinge',
            metrics=['accuracy']
        )
        # Train the model
        network.fit(X_train.values, y_train.values, epochs=100)

        # Evaluate the predictions of the model
        y_pred = network.predict(X_test.values)
        y_pred = np.around(y_pred, 0)
        print(classification_report(y_test, y_pred))


ModelDevelopment()
