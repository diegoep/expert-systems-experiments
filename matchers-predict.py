from numpy.linalg import inv, det
from sklearn import tree, svm
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.naive_bayes import GaussianNB

dados = pd.read_csv("trainingset/training-precision.csv", header = 0, sep=",")
X = dados.iloc[:, :3].values
y = dados.iloc[:, 3].values

print(X)
print(y)

skf = StratifiedKFold(n_splits=10, random_state=None, shuffle=True)
for train_index, test_index in skf.split(X, y):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

    nbg = GaussianNB()
    nbg.fit(X_train, y_train)


# for j in range(30):  # repetir 30x
#     skf = StratifiedKFold(n_splits=10, random_state=None, shuffle=True)  # 10 rodadas
#     contador = 1
#
#     for train_index, test_index in skf.split(X, y):
#         X_train, X_test = X[train_index], X[test_index]
#         y_train, y_test = y[train_index], y[test_index]
#         complete_view_train = X_train
#         complete_view_test = X_test
#
#         nbg = GaussianNB()
#         nbg.fit(X_train, y_train)
#
#         result = nbg.predict(X_test)
#         print("predict result = " + result)
#         print("Y test = "+ y_test)

# y = df.matcher
# X = df.drop('matcher', axis=1)
## O label é o matcher

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
#
# print("\nX_train:\n")
# print(X_train.head())
# print(X_train.shape)
#
# print("\nX_test:\n")
# print(X_test.head())
# print(X_test.shape)
#
# classifier = svm.SVC(kernel='linear', probability=True,
#                      random_state=random_state)


#clf = tree.DecisionTreeClassifier()

#clf = clf.fit(data)
