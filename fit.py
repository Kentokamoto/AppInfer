from sklearn.externals import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
import pandas as pd
from sklearn import svm
from sklearn import naive_bayes as nb
from sklearn.preprocessing import Imputer
from sklearn.model_selection import ShuffleSplit
from sklearn import ensemble as ens
#order of events
#1. Load the data
apps = ["Facebook", "Messenger", "Snapchat", "Spotify", "Twitter",
        "Uber", "Venmo", "Waze", "WhatsApp", "Yelp"]
tables = []
labels = []
count = 1
labelMap = {}
for app in apps:
    path = "./Data/Clean/"+app +"/"+app+"_final.csv"
    tab = pd.read_csv(path)
    labelMap[count] = app 
    print(len(tab.index))
    for i in range(len(tab.index)):
        labels.append(count)

    count+= 1
    tables.append(tab)

combine = pd.concat(tables)
matrixCombine = combine.as_matrix()
#2. Adjust formatting for scikitlearn to read
#	a. change training to arrays (data)
#	b. change labels to numbers (target)
feat = (matrixCombine, labels)

#3. Cross Validate
#	a. Split the data into training and test
#	b. call cross_val_score

#X_train, X_test, Y_train, Y_test = train_test_split(feat[0],feat[1], test_size=0.4, random_state=0)

imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
#imp.fit(X_train)
#X_train_imp = imp.fit_transform(X_train,Y_train)

imp.fit(feat[0])
X_train_imp = imp.fit_transform(feat[0],feat[1])
#clf = svm.SVC(kernel='linear', C=1).fit(X_train_imp, Y_train)
#print(clf.score(X_test, Y_test))

#clf = svm.SVC(kernel='linear', C=1)
#clf = svm.LinearSVC()
clf = ens.RandomForestClassifier()
#clf = nb.GaussianNB()
#cv = ShuffleSplit(n_splits=3, test_size=0.3, random_state=0)
scores = cross_val_score(clf,X_train_imp, feat[1],cv=5)
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
#4. Save the training data as a file

joblib.dump(clf,'trained.pkl')
