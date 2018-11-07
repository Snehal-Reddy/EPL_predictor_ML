import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import math
import operator
from sklearn.preprocessing import scale
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import xgboost as xgb
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import make_scorer
from sklearn.metrics import f1_score

data = pd.read_csv('new_final_dataset.csv')

#x and y spli
teams = {}
for i in data.groupby('HomeTeam').mean().T.columns:
	teams[i] = 0
y_all = data['FTR']

#sclaing
cols = ['HTGS','HTGC','ATGS','ATGC','HTP','ATP','DiffFormPts','DiffLP','HTWinStreak3','ATWinStreak3','HTLossStreak3','ATLossStreak3']
X_in = np.zeros(shape = (len(cols), len(data)))
for i in range(len(cols)):
	X_in[i] = (data[cols[i]])
X_all = pd.DataFrame(data = X_in.transpose(),columns=cols)
for col in cols:
    X_all[col] = scale(X_all[col])

output = pd.DataFrame(index = X_all.index)

# Investigate each feature column for the data
for col, col_data in X_all.iteritems():

    # If data type is categorical, convert to dummy variables
    if col_data.dtype == object:
        col_data = pd.get_dummies(col_data, prefix = col)
                
    # Collect the revised columns
    output = output.join(col_data)
X_all = output

#X_train, X_test, y_train, y_test = train_test_split(X_all, y_all, test_size = ,random_state = 2,stratify = y_all)
x_train = X_all.loc[0:6459,:]
y_train = y_all[0:6460]
x_test = X_all.loc[6460:6840,:]
y_test = y_all[6460:6840]
# forest_clf = RandomForestClassifier(n_estimators = 100, max_depth = 10, random_state = 0)
# forest_clf.fit(x_train, y_train)
# Y_out = forest_clf.predict(x_test)

clf = xgb.XGBClassifier(seed = 82)
parameters = {'learning_rate':[0.1], 'n_estimators':[40],'max_depth':[3],'min_child_weight':[3], 'gamma':[0.4],'subsample':[0.8], 'colsample_bytree':[0.8], 'scale_pos_weight' : [1], 'reg_alpha' : [1e-5]}
f1_scorer = make_scorer(f1_score,pos_label='H', average = 'weighted') 

grid_obj = GridSearchCV(clf, scoring = f1_scorer, param_grid = parameters, cv = 5)
grid_obj = grid_obj.fit(x_train, y_train)
clf = grid_obj.best_estimator_
clf.fit(x_train, y_train)
Y_out = clf.predict(x_test)


correct_pred = 0
for i in range(len(Y_out)):
	if Y_out[i] == y_test[i+6460]:
		correct_pred+=1

print(float(correct_pred/3.8))
# from sklearn.metrics import f1_score
for i in range(len(Y_out)):
	if Y_out[i] == 'H':
		teams[data.loc[6460+i, 'HomeTeam']] += 3
	if Y_out[i] == 'A':
		teams[data.loc[6460+i, 'AwayTeam']] += 3
	if Y_out[i] == 'D':
		teams[data.loc[6460+i, 'HomeTeam']] += 1
		teams[data.loc[6460+i, 'AwayTeam']] += 1

sorted_teams = sorted( ((value,key) for (key,value) in teams.items()), reverse = True)
print sorted_teams


plt.bar(range(len(sorted_teams)), list(sorted_teams.values()), align = 'center', width = 0.8)
plt.xticks(range(len(sorted_teams)), list(sorted_teams.keys()))
plt.xticks(rotation = 90)
plt.show()


# SVC(random_state = 912, kernel='rbf').fit(X_train, y_train)

# y_pred = clf.predict(X_train)
    
# Print the results of prediction for both training and testing
#f1 = f1_score(y_train, y_pred, pos_label='H')
#acc = sum(target == y_pred) / float(len(y_pred))
#print(f1, acc)
#print("F1 score and accuracy score for training set: {:.4f} , {:.4f}.".format(f1 , acc))

#y_pred = clf.predict(X_test)

#f1 = f1_score(y_test, y_pred, pos_label='H')
#acc = sum(target == y_pred) / float(len(y_pred)
#print(f1, acc)
#print("F1 score and accuracy score for training set: {:.4f} , {:.4f}.".format(f1 , acc))
