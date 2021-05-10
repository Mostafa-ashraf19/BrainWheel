# Computer Vision Module for BrainWheel

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
 - Semantic Segmentation (SS) using [ICNet](...)
 - Object Detecttion (OD) using [Yolov3](https://github.com/Lornatang/YOLOv3-PyTorch)
 - Finding the Occupancy Grid (OG) using the RANSAC algorithm
 - Calculating the Distance to Collision (D2C) for every object detected with OD


## Usage

First you have to download the pytorch model files:
 - Object Detection files should be put directly in the od_model/weights folder ([Source Repo](https://github.com/Lornatang/YOLOv3-PyTorch))
   - [yolov3](https://pjreddie.com/media/files/yolov3.weights)
   - [yolov3-tiny](https://pjreddie.com/media/files/yolov3-tiny.weights)
   - [yolov3-spp](https://pjreddie.com/media/files/yolov3-spp.weights)
   - [backbone network](https://pjreddie.com/media/files/darknet53.conv.74)
 - Semantic Segmentation files should be put directly in the ss_model folder ([Source Repo](...))
  - ...

To use the Computer Vision module you simply import it as follows:

```python
from computer_vision.computer_vision import ComputerVision

CV = ComputerVision()
```


You can then use each part of the project independently as follows:

You can also use each part on your own data which can be irrelevant to 
the captured images.

```python
l_img, r_img = CV.capture(show=True)

# Depth Estimation
depth_map = CV.depth_map(show=True)
point_cloud = CV.point_cloud()

# Object Detection
od_bbox = CV.object_detection(l_img, show=True)

# Semantic Segmentation
ss_pred = CV.semantic_segmentation(l_img, show=True)

# Occupancy Grid
occ_grid = CV.occupancy_grid(point_cloud, ss_pred, show=True)

# Distance to Collision
min_dists = CV.distance_to_collision(od_bbox, point_cloud)
```


Or you can use all functionality inside a for loop for a continuous stream of inputs
as shown here:

```python
import cv2

for cache in CV.loop(l_img=True, r_img=True, depth_map_img=True,point_cloud=True):
    l_img, r_img, depth_map_img, point_cloud = cache

    double_img = np.hstack((l_img, r_img))
    cv.imshow('Camera Inputs', double_img)
    cv.imshow('Depth Map', depth_map_img)

    # Object Detection
    od_bbox = CV.object_detection(l_img, show=True, keep_showing=True)

    # Semantic Segmentation
    ss_pred = CV.semantic_segmentation(l_img, show=True, keep_showing=True)

    # Occupancy Grid
    occ_grid = CV.occupancy_grid(point_cloud, ss_pred, show=True, keep_showing=True)

    # Distance to Collision
    min_dists = CV.distance_to_collision(od_data, point_cloud)
    print(min_dists)

    # Press 'q' to stop ...
  #'''

  cv.destroyAllWindows()
```

### Method Parameters:

The entire class uses the same interface for ease of use.
Every Parameter's Description is shown here:

 - ```l_img```, ```r_img```:
   - They are images of shape (H, W, 3)
   - If a function requires one image, always use ```l_img```
 - ```return_image```
   - A Boolean Type (Defaults to ```False```)
   - if ```True```: the function returns an image of the selected operation.
   - if ```False```: the function returns the output of the operation in a processable form.
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
   - [x] Write ```loop()``` method for the ```for``` loop syntax
   
 - [x] Interface with Cameras:
   - [x] Buy cameras
   - [x] Write ```capture()``` method
   
 - [x] Depth Estimation (DE):
   - [x] Write ```depth_map()``` method
   
 - [ ] Semantic Segmentation (SS):
   - [ ] Find a good SS model (ICNet)
   - [ ] Write an ```SSModel``` Class to interface with the model
     - [ ] Write a ```predict()``` method
     - [ ] Write a ```show_on_image()``` method
   - [x] Write ```semantic segmentation()``` method
   
 - [x] Object Detection (OD):
   - [x] Find a good OD model (Yolov3)
   - [x] Write an ```ODModel``` Class to interface with the model
     - [x] Write a ```predict()``` method
     - [x] Write a ```show_on_image()``` method
   - [x] Write ```object_detection()``` method
   
 - [ ] Occupancy Grid Generation (OG):
   - [ ] Get x, y & z coordinates from depth map
   - [ ] Extract points on the ground using SS
   - [ ] Find the equation of the plane using the RANSAC Algorithm
   - [ ] draw the occupancy grid from the data from before in the 
   ```occupaney_grid()``` method
   
 - [x] Distance to Collision Calculation (D2C):
   - [x] Write ```distance_to_collision()``` method
   - [x] Write ```is_close_to_collision()``` method
   - [x] Write ```is_close_to_collision_simple()``` method
   
 - [x] Document all Functions in the ```computer_vision``` module
 
