import re

# only change these variables
filename_input = "shot.####.exr"
filename_output = "shot_denoiced.####.exr"
arnold_bin_path = "C:/solidangle/mtoadeploy/2018/bin"
startframe = 101
endframe = 199
variance = 0.5
pixel_search_radius = 9
pixel_neighborhood_patch_radius = 3
temporal_range = 6
light_aov_names = ["frontlight", "backlight"] # if no light aov denoising needed, just leave list empty: []



filename_input_sequence_number = re.sub(r'#+',lambda m: r'{{:0{}d}}'.format(len(m.group(0))), filename_input)
filename_output_sequence_number = re.sub(r'#+',lambda m: r'{{:0{}d}}'.format(len(m.group(0))), filename_output)

for i in range (startframe, endframe + 1):
    temporal_range_string = ""
    light_aov_string = ""
    for j in range(-temporal_range/2, temporal_range/2):
        if (j==0) or (i+j < startframe) or (i+j > endframe):
            continue
        
        temporal_range_string += "-i " + filename_input_sequence_number.format(i+j) + " "

    for k in light_aov_names:
        light_aov_string += "-aov " + str(k) + " "
    
    print arnold_bin_path + "/noice.exe " \
            + "-patchradius " + str(pixel_neighborhood_patch_radius) + " " \
            + "-searchradius " + str(pixel_search_radius) + " " \
            + "-variance " + str(variance) + " " \
            + light_aov_string + " " \
            + "-i " + filename_input_sequence_number.format(i) + " " \
            + temporal_range_string + " " \
            + "-output " + filename_output_sequence_number.format(i),
            
    if i is not endframe:
      print " &&",