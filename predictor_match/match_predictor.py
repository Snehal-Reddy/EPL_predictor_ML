import numpy as np 
import math
import pandas as pd 
from sklearn import svm 
from sklearn.preprocessing import scale
import xgboost as xgb 
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import make_scorer
from sklearn.metrics import f1_score
from sklearn.ensemble import RandomForestClassifier
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
x_train = ipdf.loc[0:6079,:]
y_train = y_all[0:6080]
x_test = ipdf.loc[6080:6460,:]
y_test = y_all[6080:6460]

# classifier = svm.SVC(gamma = 1, kernel = 'rbf', C = 500)
# classifier.fit(x_train,y_train)
# Y_out = classifier.predict(x_test)
#print Y_out

# clf = xgb.XGBClassifier(seed = 82)
# parameters = {'learning_rate':[0.1], 'n_estimators':[40],'max_depth':[3],'min_child_weight':[3], 'gamma':[0.4],'subsample':[0.8], 'colsample_bytree':[0.8], 'scale_pos_weight' : [1], 'reg_alpha' : [1e-5]}
# f1_scorer = make_scorer(f1_score,pos_label='H', average = 'weighted') 

# grid_obj = GridSearchCV(clf, scoring = f1_scorer, param_grid = parameters, cv = 5)
# grid_obj = grid_obj.fit(x_train, y_train)
# clf = grid_obj.best_estimator_
# clf.fit(x_train, y_train)
# Y_out = clf.predict(x_test)
forest_clf = RandomForestClassifier(n_estimators = 100, max_depth = 20, random_state = 0)
forest_clf.fit(x_train, y_train)
Y_out = forest_clf.predict(x_test)
correct_pred = 0
for i in range(len(Y_out)):
	if Y_out[i] == y_test[i+6080]:
		correct_pred+=1

print(float(correct_pred/3.8))

