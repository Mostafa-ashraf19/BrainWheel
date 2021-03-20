# Computer Vision for the BCSW

In this part we use numerous computer vision techniques to help
with the Brain-Controlled Smart Wheelchair (BCSW).


## Contents

 - [Part Description](#Part-Description)
 - [Usage](#Usage)
 - [Team Members](#Team-Members)
 - [Todo](#Todo)


## Part Description

The Computer Vision part of the project has many functions including
(but not limited to):

 - Using Stereo Camera Vision with an easy to use interface
 - Depth Estimation (DE) using a disparity map algorithm
 - Semantic Segmentation (SS) using [ICNet](https://openaccess.thecvf.com/content_ECCV_2018/papers/Hengshuang_Zhao_ICNet_for_Real-Time_ECCV_2018_paper.pdf)
 - Object Detecttion (OD) using [Yolov4](https://arxiv.org/pdf/2004.10934.pdf)
 - Finding the Occupancy Grid (OG) using the RANSAC algorithm
 - Calculating the Distance to Collision (D2C) for every object detected with OD


## Usage

To use the Computer Vision module you simply import it as follows:

```python
from computer_vision.computer_vision import ComputerVision

CV = ComputerVision()
```


You can then use each part of the project independently as follows:

You can also use each part on your own data which can be irrelevant to 
the captured images.

```python
from computer_vision.computer_vision import ComputerVision

CV = ComputerVision()

l_img, r_img = CV.capture(show=True)

# Depth Estimation
depth_map = CV.compute_depth_map(l_img, r_img, show=True)

# Object Detection
od_data, od_img = CV.object_detection(l_img, show=True)

# Semantic Segmentation
seg_data, seg_img = CV.semantic_segmentation(l_img, show=True)

# Occupancy Grid
occ_grid = CV.occupancy_grid(depth_map, seg_data, show=True)

# Distance to Collision
min_dists = CV.distance_to_collision(od_data, depth_map)
```


Or you can use all functionality inside a for loop for a continuous stream of inputs
as shown here:

```python
from computer_vision.computer_vision import ComputerVision
import cv2

CV = ComputerVision()

for l_img, r_img in CV:    
    # Depth Estimation and Disparity Map
    depth_map = CV.compute_depth_map(l_img, r_img, show=True, show_disp=True, keep_showing=True)
    
    # Object Detection
    od_data, od_img = CV.object_detection(l_img, show=True, keep_showing=True)
    
    # Semantic Segmentation
    seg_data, seg_img = CV.semantic_segmentation(l_img, show=True, keep_showing=True)
    
    # Occupancy Grid
    occ_grid = CV.occupancy_grid(depth_map, seg_data, show=True, keep_showing=True)
    
    # Distance to Collision
    min_dists = CV.distance_to_collision(od_data, depth_map)
    
    # press 'q' to stop

cv2.destroyAllWindows()
```

### Method Parameters:

The entire class uses the same interface for ease of use.
Every Parameter's Description is shown here:

 - ```l_img```, ```r_img```:
   - They are images of shape (H, W, 3)
   - If a function requires one image, always use ```l_img```
 - ```show```
   - A Boolean Type (Defaults to ```False```)
   - If ```True```: the method shows a window with the output img
 - ```keep_showing```
   - A Boolean Type (Defaults to ```False```)
   - If ```False```: the shown window (if shown by ```show=True```) will stay open with a 
   static image and the code will halt until the user presses any key.
   - If ```True```: the shown window (if shown by ```show=True```) will stay open but the 
   code will keep running. Use this if you want to show a continuous stream of 
   outputs.


## Team Members

 - [Pierre Nabil](https://github.com/PierreNabil)
 - [Panse Yasser](https://github.com/Panse98)
 
 
## Todo
 - [x] Create the ```ComputerVision``` Class
   - [x] Write ```__iter__()``` and  ```__next__()``` methods for 
   the ```for``` loop syntax
   
 - [ ] Interface with Cameras:
   - [ ] Buy cameras
   - [x] Write code for camera calibration
   - [ ] Calibrate the cameras and return the projection matrices
   - [x] Write ```capture()``` method]
   
 - [ ] Depth Estimation (DE):
   - [x] Write code for disparity map generation
   - [x] Write code for depth map generation from disparity map
   - [ ] Modify the parameters for depth map estimation
   - [x] Write ```compute_deapth_map()``` method
   
 - [x] Semantic Segmentation (SS):
   - [x] Find a good SS model (ICNet)
   - [x] Write an ```SSModel``` Class to interface with the model
     - [x] Write a ```predict()``` method
     - [x] Write a ```show()``` method
   - [x] Write ```semantic segmentation()``` method
   
 - [x] Object Detection (OD):
   - [x] Find a good SS model (Yolov4 & Yolov4-Tiny)
   - [x] Write an ```ODModel``` Class to interface with the model
     - [x] Write a ```predict()``` method
     - [x] Write a ```show()``` method
   - [x] Write ```object_detection()``` method
   
 - [x] Occupancy Grid Generation (OG):
   - [x] Get x, y & z coordinates from depth map
   - [x] Extract points on the ground using SS
   - [x] Find the equation of the plane using the RANSAC Algorithm
   - [x] draw the occupancy grid from the data from before in the 
   ```occupaney_grid()``` method
   
 - [x] Distance to Collision Calculation (D2C):
   - [x] Write ```distance_to_collision()``` method
   
 - [x] Document all Functions in the ```computer_vision``` module
 

