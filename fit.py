import pdb
from sklearn.externals import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
import pandas as pd
from sklearn import svm, grid_search
from sklearn import naive_bayes as nb
from sklearn.preprocessing import Imputer
from sklearn.model_selection import ShuffleSplit
from sklearn import ensemble as ens
from sklearn.utils import shuffle
from sklearn.feature_selection import RFE
from sklearn.metrics import accuracy_score,classification_report
#order of events
#1. Load the Datai
devices = [ "HTC One M8", "Nexus 6P", "Pixel" ]
apps = ["Facebook", "Messenger", "Snapchat", "Spotify", "Twitter",
        "Uber", "Venmo", "Waze", "WhatsApp", "Yelp"]

tables = []
testTb = []
labels = []
count = 1
labelMap = {}
test = "Test2"
for dev in devices:
    for week in range( 1, 3 ):
        for app in apps:
            path = "./Data/"+ test+ "/Clean/"+ dev + "/" +app +"/"+app+"_"+str( week )+ "_final.csv"
            tab = pd.read_csv(path)
            labelMap[count] = app 
            print(len(tab.index))
            for i in range(len(tab.index)):
                labels.append(count)

            count+= 1
            pdb.set_trace()
            tables.append(tab)
            testTb.append( tab.tail(10) )


combine = pd.concat(tables)
matrixCombine = combine.as_matrix()
# Shuffle data
matrixCombine, labels = shuffle(matrixCombine,labels)
print(len(matrixCombine[0]))
#2. Adjust formatting for scikitlearn to read
#	a. change training to arrays (data)
#	b. change labels to numbers (target)
feat = (matrixCombine, labels)

#3. Cross Validate
#	a. Split the data into training and test
#	b. call cross_val_score

X_train, X_test, Y_train, Y_test = train_test_split(feat[0],feat[1], test_size=0.2, random_state=0)

imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
#imp.fit(X_train)
#X_train_imp = imp.fit_transform(X_train,Y_train)

imp.fit(feat[0])
X_train_imp = imp.fit_transform(X_train,Y_train)
#clf = svm.SVC(kernel='linear', C=1).fit(X_train_imp, Y_train)
#print(clf.score(X_test, Y_test))

#clf = svm.SVC(kernel='linear', C=1)
param_grid = [
  {'C': [1, 10, 100, 1000], 'kernel': ['linear']},
  {'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.0001], 'kernel': ['rbf']},
 ]
#clf = grid_search.GridSearchCV(clf,param_grid=param_grid)
#clf = svm.LinearSVC()
clf = ens.RandomForestClassifier()
#clf = nb.GaussianNB()
#cv = ShuffleSplit(n_splits=3, test_size=0.3, random_state=0)
#reduce number of features
scores = cross_val_score(clf,X_train_imp, Y_train,cv=5)
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
#4. Save the training data as a file
joblib.dump(clf,'trained.pkl')

clf.fit(X_train_imp,Y_train)

#5 Predict using the test data
X_test_imp = imp.fit_transform(X_test)
prediction = clf.predict(X_test_imp)
print(len(prediction))
print(len(Y_test))

acc = accuracy_score(prediction, Y_test) 
print(acc)

for i in range(len(prediction)):
    if prediction[i] != Y_test[i] :
        print("%s NOT %s"% (labelMap[prediction[i]],labelMap[ Y_test[i]]))



print(classification_report(Y_test, prediction, target_names=apps))
