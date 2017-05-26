import training_data
import testing_data
import numpy as np
from sklearn import svm
from sklearn import tree
from sklearn.kernel_ridge import KernelRidge

np.set_printoptions(threshold='nan')

#clf = svm.SVC()
#clf = KernelRidge(alpha=1.0)
clf = tree.DecisionTreeClassifier()
clf.fit(training_data.x_col, training_data.y_col)
print("Finished fitting data.")

prediction = clf.predict(testing_data.x_col)

count = 0
total = 0
for i in range(0, len(prediction)):
    total = total + 1
    if prediction[i] == 1:
        count = count + 1
print("Ratio:"+str(float(count)/total))

print(prediction)
print(testing_data.y_col)

