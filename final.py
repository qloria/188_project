import dicom
import pylab
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import random
import os.path
from sklearn import svm
from sklearn import tree
from sklearn.kernel_ridge import KernelRidge
from sklearn import linear_model
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier

np.set_printoptions(threshold='nan')

num_patients = 12
num_samples = 500 # actual sample size may vary
patch_size = 9

#feature = dicom.read_file("LesionDataset/1/Features/IM-0001-0014-0001.dcm") #sys.argv[1]
#label = dicom.read_file("LesionDataset/1/Labels/IM-0001-0014-0001.dcm")
#pylab.imshow(feature.pixel_array, cmap=pylab.cm.bone)
#pylab.show()

avg_overall = 0
avg_zero = 0
avg_one = 0
print(patch_size)
for t in range(1, num_patients+1): # use as testing patient
    # x_col holds patches and y_col holds the corresponding label value (0,1)
    x_col = []
    y_col = []

    t = 9 #select a specific patient to test on, comment out to loop through all patients

    # iterate through patients to create training table
    for n in range(1, num_patients+1):
        if n == t: # skip the testing patient
            continue
        file_name1 = "LesionDataset/"
        file_name2 = str(n)
        file_name31 = "/Features/"
        file_name32 = "/Labels/"

        # Calculate number of files for current patient
        path = file_name1 + file_name2 + file_name31
        num_files = len([f for f in os.listdir(path)
                    if os.path.isfile(os.path.join(path, f))])

        # Iterate through each image (image 10-23 are the only ones to have a marked lesion area)
        for m in range(10, 24):
            # Create file path and read in the image
            file_name4 = "IM-0001-00"
            if len(str(m)) == 1:
            	file_name5 = "0" + str(m)
            else:
            	file_name5 = str(m)
            file_name6 = "-0001.dcm"

            fname_feature = file_name1 + file_name2 + file_name31 + file_name4 + file_name5 + file_name6
            fname_label = file_name1 + file_name2 + file_name32 + file_name4 + file_name5 + file_name6
            feature = dicom.read_file(fname_feature)
            label = dicom.read_file(fname_label)
            image = feature.pixel_array
            labels_image = label.pixel_array

            # Calculate dimensions of image
            width = len(feature.pixel_array[0])
            height = len(feature.pixel_array)

            for i in range(0, num_samples):
                # Generate random numbers for x and y coordinates to be the center of our patches
                cur_r = random.randint(0, height-1)
                cur_c = random.randint(0, width-1)

                # Create y column of training table
                # (to balance training set, we control the number of 0's to 1's)
                if labels_image[cur_r][cur_c] == 5000:
                    y_col.append(1)

                    # Create patch and push into x column (1)
                    patch = []
                    offset = (patch_size-1)/2
                    for r in range(-offset, offset+1):
                        for c in range(-offset, offset+1):
                            offset_r = cur_r+r
                            offset_c = cur_c+c

                            # Check if pixel out of bounds
                            if offset_r < 0 or offset_r > height-1:
                                offset_r = cur_r;
                            if offset_c < 0 or offset_c > width-1:
                                offset_c = cur_c;

                            patch.append(image[offset_r][offset_c])
                    x_col.append(patch)

                    zero_count = 0 #control ratio of non lesion points to lesion
                    for j in range(i, num_samples):
                        cur_r = random.randint(0, height-1)
                        cur_c = random.randint(0, width-1)

                        if labels_image[cur_r][cur_c] != 5000:
                            y_col.append(0)
                            zero_count += 1

                            patch = []
                            offset = (patch_size-1)/2
                            for r in range(-offset, offset+1):
                                for c in range(-offset, offset+1):
                                    offset_r = cur_r+r
                                    offset_c = cur_c+c

                                    # Check if pixel out of bounds
                                    if offset_r < 0 or offset_r > height-1:
                                        offset_r = cur_r;
                                    if offset_c < 0 or offset_c > width-1:
                                        offset_c = cur_c;

                                    patch.append(image[offset_r][offset_c])
                            x_col.append(patch)
                            if (zero_count == 1):
                                break      
    print("Num samples: "+str(len(y_col)))
    print("Finished creating training data.")

    # Create testing set
    testing_x_col = []
    testing_y_col = []

    image_num = "13"
    file_name = "LesionDataset/"+str(t)+"/Features/IM-0001-00"+image_num+"-0001.dcm"
    file_name1 = "LesionDataset/"+str(t)+"/Labels/IM-0001-00"+image_num+"-0001.dcm"
    feature = dicom.read_file(file_name)
    label = dicom.read_file(file_name1)
    image = feature.pixel_array
    labels_image = label.pixel_array

    width = len(label.pixel_array[0])
    height = len(label.pixel_array)

    for cur_r in range(0, height):
        for cur_c in range(0, width):

            if labels_image[cur_r][cur_c] == 5000:
                testing_y_col.append(1)
            if labels_image[cur_r][cur_c] != 5000:
                testing_y_col.append(0)

            patch = []
            offset = (patch_size-1)/2
            for r in range(-offset, offset+1):
                for c in range(-offset, offset+1):
                    offset_r = cur_r+r
                    offset_c = cur_c+c

                    # Check if pixel out of bounds
                    if offset_r < 0 or offset_r > height-1:
                        offset_r = cur_r;
                    if offset_c < 0 or offset_c > width-1:
                        offset_c = cur_c;
                    patch.append(image[offset_r][offset_c])
            testing_x_col.append(patch)
    print("Finished compiling testing set on patient "+str(t))

    
    #clf = KernelRidge(alpha=1.0)
    #clf = linear_model.Ridge (alpha = .5)
    #clf = svm.SVC(gamma=0.000001) #0.000001
    #clf = tree.DecisionTreeClassifier()
    #clf = AdaBoostClassifier(n_estimators=100) #1:1 ratio
    clf = RandomForestClassifier(n_estimators=10)
    clf.fit(x_col, y_col)
    print("Finished fitting data.")

    prediction = clf.predict(testing_x_col)

    print("Prediction information:")
    count = 0
    total = 0
    count_ones = 0
    total_ones = 0
    count_zeroes = 0
    total_zeroes = 0

    '''
    # for linear methods, set threshold
    for i in range(0, len(prediction)):
        if prediction[i] > .1:
            prediction[i] = 1
        else:
            prediction[i] = 0
    '''

    for i in range(0, len(prediction)):
        total = total + 1
        if prediction[i] == testing_y_col[i]:
            count = count + 1

        # accuracy of lesion area prediction
        if testing_y_col[i] == 1:
            if prediction[i] == 1:
                count_ones += 1
            total_ones += 1

        # accuracy of non lesion area
        if testing_y_col[i] == 0:
            if prediction[i] == 0:
                count_zeroes += 1
            total_zeroes += 1

    avg_overall += float(count)/total
    avg_one += float(count_ones)/total_ones
    avg_zero += float(count_zeroes)/total_zeroes
    # save prediction image
    plt.imsave('test.png', np.array(prediction).reshape(height,width), cmap=cm.gray)
    

    #print("Prediction:")
    #print(prediction)
    #print("Expected outcome:")
    #print(testing_data.y_col)
    print("Accuracy overall: ")
    print(str(float(count)/total))
    print("Accuracy 1s: ")
    print(str(float(count_ones)/total_ones))
    print("Accuracy 0s: ")
    print(str(float(count_zeroes)/total_zeroes))
    print("-----------")

print("Avg overall: "+str(avg_overall/12))
print("Avg 1s: "+str(avg_one/12))
print("Avg 0s: "+str(avg_zero/12))






