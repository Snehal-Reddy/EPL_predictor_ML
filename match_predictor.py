import numpy as np 
import math
import pandas as pd 
from sklearn import svm 
from sklearn.preprocessing import scale
#from sklearn.cross_validation import test_train_split
#from sklearn.preprocessing import scale

input_data = pd.read_csv("final_dataset.csv")
training_set_size = len(input_data)

teams = {}
for i in input_data.groupby('HomeTeam').mean().T.columns:
	teams[i] = 0

X_in = np.zeros(shape = (5, training_set_size))
cols = ['HTGD', 'ATGD', 'HTP','ATP', 'DiffLP']
for i in range(len(cols)):
	X_in[i] = (input_data[cols[i]])

ipdf = pd.DataFrame(data = X_in.transpose(),columns=cols)

#X_train, X_test, y_train, y_test = train_test_split(X_all, y_all, test_size = 50,random_state = 2,stratify = y_all)
#print(ipdf)

# for i in range(5):
# 	ipdf[i] = scale(ipdf[i])

#scaling:
for i in range(len(ipdf)):
	ipdf['DiffLP'][i] = ipdf['DiffLP'][i] /5

y_all = input_data.loc[:,'FTR']
x_train = ipdf.loc[0:5699,:]
y_train = y_all[0:5700]
x_test = ipdf.loc[5700:6460,:]
y_test = y_all[5700:6460]
#print(y_test[5702])

#print np.shape(X_in.transpose())
classifier = svm.SVC(gamma = 1, kernel = 'rbf', C = 1000000)
classifier.fit(x_train,y_train)
Y_out = classifier.predict(x_test)
#print Y_out
correct_pred = 0
for i in range(len(Y_out)):
	if Y_out[i] == y_test[i+5700]:
		correct_pred+=1

print(float(correct_pred)/7.60)
