import dicom
import pylab
import sys
import numpy as np
import random

#read in the data
num_patients = 10;

feature = dicom.read_file("LesionDataset/1/Features/IM-0001-0014-0001.dcm") #sys.argv[1]
label = dicom.read_file("LesionDataset/1/Labels/IM-0001-0014-0001.dcm")
#pylab.imshow(ds.pixel_array, cmap=pylab.cm.bone)
#pylab.show()
image = feature.pixel_array
labels_image = label.pixel_array

num_samples = 100

x_coords = random.sample(range(1, 254), num_samples)
y_coords = random.sample(range(1, 222), num_samples)

x_col = []
y_col = []

for i in range(0, num_samples):
    #x_col.append(image[x_coords[i]][y_coords[i]])
    cur_x = x_coords[i];
    cur_y = y_coords[i];

    patch = []

    for x in range(-1,2):
        for y in range(-1,2):
            patch.append(image[cur_x+x][cur_y+y])

    # Create y column of training table
    if labels_image[cur_x][cur_y] == 5000:
        y_col.append(1)
    else:
        y_col.append(0)

    print(patch)









