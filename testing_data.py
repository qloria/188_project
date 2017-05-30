import dicom
import pylab
import sys
import numpy as np
import random
import os.path

np.set_printoptions(threshold='nan')

patch_size = 17

#feature = dicom.read_file("LesionDataset/11/Features/IM-0001-0012-0001.dcm") #sys.argv[1]
#label = dicom.read_file("LesionDataset/11/Labels/IM-0001-0012-0001.dcm")
#pylab.imshow(ds.pixel_array, cmap=pylab.cm.bone)
#pylab.show()

x_col = []
y_col = []


# iterate through patients
for n in range(12, 13):
    file_name1 = "LesionDataset/"
    file_name2 = str(n)
    file_name31 = "/Features/"
    file_name32 = "/Labels/"

    #Calculate number of files for current patient
    path = file_name1 + file_name2 + file_name31
    num_files = len([f for f in os.listdir(path)
                if os.path.isfile(os.path.join(path, f))])
    num_files = 3

    # Iterate through each image
    for m in range(13, 14):
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

        for cur_r in range(0, height):
            for cur_c in range(0, width):

                #if labels_image[cur_r][cur_c] == 5000:
                 #   y_col.append(1)
                if labels_image[cur_r][cur_c] != 5000:
                    y_col.append(0)

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
                            #print("offset_r:"+str(offset_r))
                            #print("offset_c:"+str(offset_c))
                            #print(str(image[offset_r][offset_c]))
                            patch.append(image[offset_r][offset_c])
                    x_col.append(patch)
        #print(x_col)                
                #else:
                #    y_col.append(0)





