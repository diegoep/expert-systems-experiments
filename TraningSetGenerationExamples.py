from sklearn import tree
from sklearn.datasets import load_iris
import graphviz

iris = load_iris()

clf = tree.DecisionTreeClassifier()
clf = clf.fit(iris.data, iris.target)

print(clf.predict([[5.1, 3.5, 1.4, 0.2]])) # 0 = setosa
print(clf.predict([[4.9, 2.4, 3.3, 1.0]])) # 1 = versicolor

dot_data = tree.export_graphviz(clf, out_file=None,
                                feature_names=iris.feature_names,
                                class_names=iris.target_names,
                                filled=True, rounded=True,
                                special_characters=True)
graph = graphviz.Source(dot_data)
graph.render("iris")