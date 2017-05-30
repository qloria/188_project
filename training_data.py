import dicom
import pylab
import sys
import numpy as np
import random
import os.path

num_patients = 10
num_samples = 2000
patch_size = 17

#feature = dicom.read_file("LesionDataset/1/Features/IM-0001-0014-0001.dcm") #sys.argv[1]
#label = dicom.read_file("LesionDataset/1/Labels/IM-0001-0014-0001.dcm")
#pylab.imshow(feature.pixel_array, cmap=pylab.cm.bone)
#pylab.show()

x_col = []
y_col = []

# iterate through patients
for n in range(1, num_patients+1):
    file_name1 = "LesionDataset/"
    file_name2 = str(n)
    file_name31 = "/Features/"
    file_name32 = "/Labels/"

    #Calculate number of files for current patient
    path = file_name1 + file_name2 + file_name31
    num_files = len([f for f in os.listdir(path)
                if os.path.isfile(os.path.join(path, f))])

    # Iterate through each image
    for m in range(1, num_files+1):
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

        # To hold our randomly generated coordinates
        r_coords = []
        c_coords = []
        for i in range(0, num_samples):
            # Generate random numbers for x and y coordinates to be the center of our patches
            r_coords.append(random.randint(0, height-1))
            c_coords.append(random.randint(0, width-1))

            cur_r = r_coords[i]
            cur_c = c_coords[i]

            # Create y column of training table
            if labels_image[cur_r][cur_c] == 5000:
                y_col.append(1)

                # Create patch and push into x column
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

                zero_count = 0
                for j in range(i, num_samples):
                    r_coords.append(random.randint(0, height-1))
                    c_coords.append(random.randint(0, width-1))
                    cur_r = r_coords[j]
                    cur_c = c_coords[j]
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
                        if (zero_count == 5):
                            break



           # else:
             #   y_col.append(0)
            
            

         

#print(x_col)
#print(y_col)
print("Finished creating training data.")







