import numpy as np 
import math
import pandas as pd 
from sklearn import svm 
#from sklearn.cross_validation import test_train_split
#from sklearn.preprocessing import scale

input_data = pd.read_csv("final_dataset.csv")
training_set_size = len(input_data)
print training_set_size
X_in = np.zeros(shape = (5, training_set_size))
cols = ['HTGD', 'ATGD', 'HTP','ATP', 'DiffLP']
for i in range(len(cols)):
	X_in[i] = (input_data[cols[i]])

Y_train = input_data['FTR']
print np.shape(X_in.transpose())
classifier = svm.SVC(gamma = 1, kernel = 'rbf', C = 1000)
classifier.fit(X_in.transpose(), Y_train)
Y_out = classifier.predict(X_in.transpose())
print Y_out
