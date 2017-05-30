import training_data
import testing_data
import numpy as np
from sklearn import svm
from sklearn import tree
from sklearn.kernel_ridge import KernelRidge
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier

np.set_printoptions(threshold='nan')

#clf = svm.SVC()
#clf = KernelRidge(alpha=1.0)
#clf = tree.DecisionTreeClassifier()
clf = AdaBoostClassifier(n_estimators=100)
#clf = RandomForestClassifier(n_estimators=10)
clf.fit(training_data.x_col, training_data.y_col)
print("Finished fitting data.")

prediction = clf.predict(testing_data.x_col)

print("Prediction information:")
count = 0
total = 0
for i in range(0, len(prediction)):
    total = total + 1
    if prediction[i] == testing_data.y_col[i]:
        count = count + 1
print("Ratio:"+str(float(count)/total))

print(prediction)
print(testing_data.y_col)

