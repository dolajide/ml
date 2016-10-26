# from sklearn.datasets import load_iris
# iris = load_iris()
# print(iris.feature_names)
# print(iris.target_names)
# print(iris.data[0])
# print(iris.target[0])

import numpy as np
from sklearn.datasets import load_iris
from sklearn import tree
import pydotplus
#viz code
from sklearn.externals.six import StringIO

iris = load_iris()
test_idx = [0, 50, 100]

#training data
training_label = np.delete(iris.target, test_idx)
train_data = np.delete(iris.data, test_idx, axis=0)

#test data
test_label = iris.target[test_idx]
test_data = iris.data[test_idx]

clf = tree.DecisionTreeClassifier()
clf.fit(train_data, training_label)
print(test_label)
print(clf.predict(test_data))

# import pydotplus
dot_data = StringIO()
tree.export_graphviz(clf, 
                        out_file=dot_data,
                        feature_names=iris.feature_names,
                        class_names=iris.target_names,
                        filled=True, rounded=True,
                        impurity=False)
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
graph.write_pdf("iris.pdf")
print(iris.feature_names, iris.data[0], iris.target_names[iris.target[0]])
