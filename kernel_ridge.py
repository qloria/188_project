import training_data
import testing_data
from sklearn.kernel_ridge import KernelRidge
import numpy as np
from sklearn import svm

np.set_printoptions(threshold='nan')

clf = svm.SVC()
clf.fit(training_data.x_col, training_data.y_col)

prediction = clf.predict(testing_data.x_col)
print(prediction)
print(testing_data.y_col)

