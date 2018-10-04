import pandas as pd
from sklearn.preprocessing import scale
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

data = pd.read_csv('final_dataset.csv')

#x and y split
X_all = data.drop(['FTR'],1)
y_all = data['FTR']

#sclaing
cols = [['HTGD','ATGD','HTP','ATP','DiffLP']]
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

X_train, X_test, y_train, y_test = train_test_split(X_all, y_all, test_size = 50,random_state = 2,stratify = y_all)

from sklearn.metrics import f1_score

SVC(random_state = 912, kernel='rbf').fit(X_train, y_train)

y_pred = clf.predict(X_train)
    
# Print the results of prediction for both training and testing
f1 = f1_score(y_train, y_pred, pos_label='H')
acc = sum(target == y_pred) / float(len(y_pred)
print f1, acc
print "F1 score and accuracy score for training set: {:.4f} , {:.4f}.".format(f1 , acc)

y_pred = clf.predict(X_test)
    
# Print the results of prediction for both training and testing
f1 = f1_score(y_test, y_pred, pos_label='H')
acc = sum(target == y_pred) / float(len(y_pred)
print f1, acc
print "F1 score and accuracy score for training set: {:.4f} , {:.4f}.".format(f1 , acc)
