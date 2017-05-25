import dicom
import pylab
import sys
import numpy as np
import random
import os.path

num_samples = 100

x_col = []
y_col = []

# iterate through patients, then each image
for n in range(11, 13):
    file_name1 = "LesionDataset/"
    file_name2 = str(n)
    file_name31 = "/Features/"
    file_name32 = "/Labels/"

    path = file_name1 + file_name2 + file_name31
    num_files = len([f for f in os.listdir(path)
                if os.path.isfile(os.path.join(path, f))])

    for m in range(1, num_files+1): #26 or 24 photos
        
        file_name4 = "IM-0001-00"
        if len(str(m)) == 1:
        	file_name5 = "0" + str(m)
        else:
        	file_name5 = str(m)
        file_name6 = "-0001.dcm"

        fname_feature = file_name1 + file_name2 + file_name31 + file_name4 + file_name5 + file_name6
        fname_label = file_name1 + file_name2 + file_name32 + file_name4 + file_name5 + file_name6

        print(fname_feature)
        
        feature = dicom.read_file(fname_feature)
        label = dicom.read_file(fname_label)

        image = feature.pixel_array
        labels_image = label.pixel_array

        x_coords = random.sample(range(1, 254), num_samples)
        y_coords = random.sample(range(1, 222), num_samples)
        for w in range(1, 254):
            for z in range(1, 222):
                if labels_image[w][z] == 5000:
                    patch = []
                    for x in range(-1,2):
                        for y in range(-1,2):
                            patch.append(image[w+x][z+y])
                    x_col.append(patch)                
                    y_col.append(1)


        for i in range(0, num_samples):
            #x_col.append(image[x_coords[i]][y_coords[i]])
            cur_x = x_coords[i];
            cur_y = y_coords[i];
            patch = []

            for x in range(-1,2):
                for y in range(-1,2):
                    patch.append(image[cur_x+x][cur_y+y])
            x_col.append(patch)

            # Create y column of training table
            if labels_image[cur_x][cur_y] == 5000:
                y_col.append(1)
            else:
                y_col.append(0)

#print(x_col)
#print(y_col)







