import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import time
import calendar

from numpy import concatenate

import tensorflow as tf

from matplotlib.pylab import rcParams
rcParams['figure.figsize']=20,10
from keras.models import Sequential
from keras.layers import LSTM, Dropout, Dense
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

def convert_zulu_to_epoch(zulu):
    timestamp = time.strptime(zulu, "%Y-%m-%dT%H:%M:%SZ")
    unix_time_local = time.mktime(timestamp)
    unix_time_utc = calendar.timegm(timestamp)
    return unix_time_utc

df = pd.read_csv('data.csv', usecols=[0, 1], engine='python', index_col=False)

df['t'] = df['t'].apply(lambda x: convert_zulu_to_epoch(x))
# df.reset_index(drop=True, inplace=True)
# df = df.drop(df.columns[0], axis=1)

print(df)

# plt.plot(df)
# plt.show()

# ------------------

# fix random seed for reproducability
tf.random.set_seed(7)

dataset = df.values
dataset = dataset.astype('float32')

print(dataset)

#  normalize dataset
time_val = list(df.loc[:, 't'])
min_val, max_val = time_val[0], time_val[-1]
scaler = MinMaxScaler(feature_range=(0, 1))
dataset = scaler.fit_transform(dataset)

# split into train and test sets
train_size = int(len(dataset) * 0.67)
test_size = len(dataset) - train_size
train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]
print(len(train), len(test))


# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back-1):
        # a = dataset[i:(i+look_back)]
        # dataX.append(a)
        dataY.append(dataset[i + look_back, 0])
    
    dataX = dataset[:len(dataset)-look_back-1]
    
    return np.array(dataX), np.array(dataY)


# reshape into X=t and Y=t+1
look_back = 1
trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)

print(trainX)
print(trainX.shape, trainY.shape, dataset.shape)

# reshape input to be [samples, time steps, features]
trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

# create and fit the LSTM network
model = Sequential()
model.add(LSTM(4, input_shape=(1, 2))) # input shape is (, features)
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
history = model.fit(trainX, trainY, epochs=100, batch_size=1, verbose=2, validation_data=(testX, testY))


plt.plot(history.history['loss'], label='train')
plt.plot(history.history['val_loss'], label='test')
plt.legend()
plt.show()

# make predictions
trainPredict = model.predict(trainX)
train_X = trainX.reshape((trainX.shape[0], trainX.shape[2]))
inv_yhat = concatenate((trainPredict, train_X[:, 1:]), axis=1)
inv_yhat = scaler.inverse_transform(inv_yhat)
inv_yhat = inv_yhat[:,0]

# invert scaling for actual
test_y = trainY.reshape((len(trainY), 1))
inv_y = concatenate((test_y, train_X[:, 1:]), axis=1)
inv_y = scaler.inverse_transform(inv_y)
inv_y = inv_y[:,0]
# calculate RMSE
rmse = np.sqrt(mean_squared_error(inv_y, inv_yhat))
print('Test RMSE: %.3f' % rmse)

# invert predictions
# trainPredict = scaler.inverse_transform(inv_yhat)
# trainY = scaler.inverse_transform([trainY])
# testPredict = scaler.inverse_transform(testPredict)
# testY = scaler.inverse_transform([testY])
# # calculate root mean squared error
# trainScore = np.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))
# print('Train Score: %.2f RMSE' % (trainScore))
# testScore = np.sqrt(mean_squared_error(testY[0], testPredict[:,0]))
# print('Test Score: %.2f RMSE' % (testScore))
