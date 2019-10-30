import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)



import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler


import numpy as np 
import pandas as pd 
import pandas as pd 
import numpy as np 
import scipy as sp 
import sklearn
import random 
import time 

from sklearn import preprocessing, model_selection


from keras.models import Sequential 
from keras.layers import Dense 
from keras.utils import np_utils
from sklearn.preprocessing import LabelEncoder
from keras.utils.np_utils import to_categorical
from sklearn.utils import shuffle
from keras.optimizers import SGD

inputs = np.loadtxt('boardLayouts.txt')
#inputs = pd.read_csv('boardOptions.csv', delimiter = ',')


#classes = np.loadtxt('bestMove.csv').astype("float")
classes = np.loadtxt('MiniMaxMove.txt')

#Initialize array to tranfor the classes to an array of 8 zeros and one 1 
#at the location of the optimal move
y =  []

#manipulate data to create multi-class array2D-array 
for i in range(35745):
	multi_class = []
	num = classes[i]
	for j in range(9):
		if num != j:
			multi_class.append(0)
		else:
			multi_class.append(1)
		#print(multi_class)
	y.append(multi_class)
np.asarray(y)

#Set inputs for the training
x_train = inputs
y_train = y

#Uses the last 2,500 data points to test the model
x_test = inputs[33000: 35745]
y_test = y[33000: 35745]

#Initialize the model
model = Sequential()
#Add 2 hidden layer to interperet the input
model.add(Dense(9, input_dim = 9, activation = 'relu'))
model.add(Dense(9, activation = 'relu'))

#Use softmax to find the location of the optimal move
model.add(Dense(9, activation = 'softmax'))

#compile the model
model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

#Train the model
model.fit(np.array(x_train), np.array(y_train), epochs = 1000, batch_size = 512)

#Print the accuracy on each epoch
scores = model.evaluate(np.array(x_test),np.array(y_test))
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))


#Plots the graph of the accuracy and loss through the epochs
#plt.plot(history.history['acc'])
#plt.plot(history.history['val_acc'])
#plt.title('Model accuracy')
#plt.ylabel('Accuracy')
#plt.xlabel('Epoch')
#plt.legend(['Train', 'Test'], loc='upper left')
#plt.show()

# Plot training & validation loss values
#plt.plot(history.history['loss'])
#plt.plot(history.history['val_loss'])
#plt.title('Model loss')
#plt.ylabel('Loss')
#plt.xlabel('Epoch')
#plt.legend(['Train', 'Test'], loc='upper left')
#plt.show()

#Save Trained Model
model.save('model.TicTacToe')
