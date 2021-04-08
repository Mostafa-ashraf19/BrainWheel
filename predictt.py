import os
import glob
import cv2
import argparse
import PIL
import torch

import torch.nn as nn
import torch.nn.functional as F
import numpy as np

from util import io
from PIL import Image
from util.pallete import get_mask_pallete
from util.io import write_depth



from torchvision.transforms import Compose
from dpt.models import DPTSegmentationModel
from dpt.transforms import Resize, NormalizeImage, PrepareForNet

from dpt import models
from dpt.blocks import (
    FeatureFusionBlock,
    FeatureFusionBlock_custom,
    Interpolate,
    _make_encoder,
    forward_vit,
)
def _make_fusion_block(features, use_bn):
    return FeatureFusionBlock_custom(
        features,
        nn.ReLU(False),
        deconv=False,
        bn=use_bn,
        expand=False,
        align_corners=True,
    )









class segmentation_model(models.DPT):
    def __init__(self, num_classes=150, , path=None, **kwargs):
        self.num_classes=num_classes

        features = kwargs["features"] if "features" in kwargs else 256

        kwargs["use_bn"] = True
      

        head = nn.Sequential(
            nn.Conv2d(features, features, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(features),
            nn.ReLU(True),
            nn.Dropout(0.1, False),
            nn.Conv2d(features, num_classes, kernel_size=1),
            Interpolate(scale_factor=2, mode="bilinear", align_corners=True),
        )

        super().__init__(head, **kwargs)

        self.auxlayer = nn.Sequential(
            nn.Conv2d(features, features, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(features),
            nn.ReLU(True),
            nn.Dropout(0.1, False),
            nn.Conv2d(features, num_classes, kernel_size=1),
        )

        if path is not None:
            self.load(path)




    
    def predict(self,img_name,output_path,model_path, model_type="dpt_hybrid", optimize=True):
         device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
         print("device: %s" % device)

         net_w = net_h = 480
        # check with piere lw nshel condition w nsbt model w  brdoo cudaa #
        # load network
         if model_type == "dpt_large":
            model = DPTSegmentationModel(
                150,
                path=model_path,
                backbone="vitl16_384",
            )
         elif model_type == "dpt_hybrid":
            model = DPTSegmentationModel(
                150,
                path=model_path,
                backbone="vitb_rn50_384",
            )
         else:
            assert (
                False
            ), f"model_type '{model_type}' not implemented, use: --model_type [dpt_large|dpt_hybrid]"

         transform = Compose(
            [
                Resize(
                    net_w,
                    net_h,
                    resize_target=None,
                    keep_aspect_ratio=True,
                    ensure_multiple_of=32,
                    resize_method="minimal",
                    image_interpolation_method=cv2.INTER_CUBIC,
                ),
                NormalizeImage(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
                PrepareForNet(),
            ]
        )

         model.eval()

         if optimize == True and device == torch.device("cuda"):
            model = model.to(memory_format=torch.channels_last)
            model = model.half()

         model.to(device)
         img = io.read_image(img_name)
         img_input = transform({"image": img})["image"]
    
        
         
         with torch.no_grad():
            sample = torch.from_numpy(img_input).to(device).unsqueeze(0)
            if optimize == True and device == torch.device("cuda"):
                sample = sample.to(memory_format=torch.channels_last)
                sample = sample.half()

            out = model.forward(sample)
            
            prediction = torch.nn.functional.interpolate(
                out, size=img.shape[:2], mode="bicubic", align_corners=False
            )
            prediction = torch.argmax(prediction, dim=1) + 1
            prediction = prediction.squeeze().cpu().numpy()
            print( prediction)
            #return(prediction)




            filename = os.path.join(output_path, os.path.splitext(os.path.basename(img_name))[0])
            io.write_segm_img(filename, img, prediction, alpha=0.5)
            
    
    
  # def show_on_image(self, img_name,output_path,model_path):

            
        #    filename = os.path.join(output_path, os.path.splitext(os.path.basename(img_name))[0])
        #    prediction=self.predict(img_name,model_path)
        #    img= io.read_image(img_name)
        #    io.write_segm_img(filename, img, prediction, alpha=0.5)


            ###change img_name dih l img bsssssssssssssssss####################
        

          

         
           
        

if __name__ == "__main__":
    
    s=segmentation_model()
    #s.run("E:\Graduation Project\SS model 1\DPT\input","E:\\Graduation Project\SS model 1\DPT\output_semseg","E:\Graduation Project\SS model 1\DPT\weights\dpt_hybrid-ade20k-53898607.pt",model_type="dpt_hybrid", optimize=True)
    #s.run("test.jpeg","E:\\Graduation Project\SS model 1\DPT\output_semseg","E:\Graduation Project\SS model 1\DPT\weights\dpt_hybrid-ade20k-53898607.pt",model_type="dpt_hybrid", optimize=True)
    
    s.predict("test1.jpeg","E:\Graduation Project\SS model 1\DPT\output_semseg","E:\Graduation Project\SS model 1\DPT\weights\dpt_hybrid-ade20k-53898607.pt",model_type="dpt_hybrid", optimize=True)
 #s.show_on_image("test.jpeg","E:\Graduation Project\SS model 1\DPT\output_semseg","E:\Graduation Project\SS model 1\DPT\weights\dpt_hybrid-ade20k-53898607.pt")

        


        

