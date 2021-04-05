import os
import glob
import cv2
import argparse

import torch

import torch.nn as nn
import torch.nn.functional as F


from util import io

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

class BaseModel(torch.nn.Module):
    def load(self, path):
        """Load model from file.

        Args:
            path (str): file path
        """
        parameters = torch.load(path, map_location=torch.device("cpu"))

        if "optimizer" in parameters:
            parameters = parameters["model"]

        self.load_state_dict(parameters)

class DPT(BaseModel):
    def __init__(
        self,
        head,
        features=256,
        backbone="vitb_rn50_384",
        readout="project",
        channels_last=False,
        use_bn=False,
        enable_attention_hooks=False,
    ):

        super(DPT, self).__init__()

        self.channels_last = channels_last

        hooks = {
            "vitb_rn50_384": [0, 1, 8, 11],
            "vitb16_384": [2, 5, 8, 11],
            "vitl16_384": [5, 11, 17, 23],
        }

        # Instantiate backbone and reassemble blocks
        self.pretrained, self.scratch = _make_encoder(
            backbone,
            features,
            False,  # Set to true of you want to train from scratch, uses ImageNet weights
            groups=1,
            expand=False,
            exportable=False,
            hooks=hooks[backbone],
            use_readout=readout,
            enable_attention_hooks=enable_attention_hooks,
        )

        self.scratch.refinenet1 = _make_fusion_block(features, use_bn)
        self.scratch.refinenet2 = _make_fusion_block(features, use_bn)
        self.scratch.refinenet3 = _make_fusion_block(features, use_bn)
        self.scratch.refinenet4 = _make_fusion_block(features, use_bn)

        self.scratch.output_conv = head

    def forward(self, x):
        if self.channels_last == True:
            x.contiguous(memory_format=torch.channels_last)

        layer_1, layer_2, layer_3, layer_4 = forward_vit(self.pretrained, x)

        layer_1_rn = self.scratch.layer1_rn(layer_1)
        layer_2_rn = self.scratch.layer2_rn(layer_2)
        layer_3_rn = self.scratch.layer3_rn(layer_3)
        layer_4_rn = self.scratch.layer4_rn(layer_4)

        path_4 = self.scratch.refinenet4(layer_4_rn)
        path_3 = self.scratch.refinenet3(path_4, layer_3_rn)
        path_2 = self.scratch.refinenet2(path_3, layer_2_rn)
        path_1 = self.scratch.refinenet1(path_2, layer_1_rn)

        out = self.scratch.output_conv(path_1)

        return out


class DPTSegmentationModel(DPT):
    def __init__(self, num_classes, path=None, **kwargs):

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
    
    def run(input_path, output_path, model_path, model_type="dpt_hybrid", optimize=True):
    #Run segmentation network

    #Args:
    #    input_path (str): path to input folder
    #    output_path (str): path to output folder
    #    model_path (str): path to saved model
    
        print("initialize")

        # select device
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print("device: %s" % device)

        net_w = net_h = 480

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

        # get input
        img_names = glob.glob(os.path.join(input_path, "*"))
        num_images = len(img_names)

        # create output folder
        os.makedirs(output_path, exist_ok=True)

        print("start processing")

        for ind, img_name in enumerate(img_names):

            print("  processing {} ({}/{})".format(img_name, ind + 1, num_images))

            # input
            img = io.read_image(img_name)
            img_input = transform({"image": img})["image"]

            # compute
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

            # output
            filename = os.path.join(
                output_path, os.path.splitext(os.path.basename(img_name))[0]
            )
            io.write_segm_img(filename, img, prediction, alpha=0.5)

        print("finished")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i", "--input_path", default="input", help="folder with input images"
    )

    parser.add_argument(
        "-o", "--output_path", default="output_semseg", help="folder for output images"
    )

    parser.add_argument(
        "-m",
        "--model_weights",
        default=None,
        help="path to the trained weights of model",
    )

    # 'vit_large', 'vit_hybrid'
    parser.add_argument("-t", "--model_type", default="dpt_hybrid", help="model type")

    parser.add_argument("--optimize", dest="optimize", action="store_true")
    parser.add_argument("--no-optimize", dest="optimize", action="store_false")
    parser.set_defaults(optimize=True)

    args = parser.parse_args()

    default_models = {
        "dpt_large": "weights/dpt_large-ade20k-b12dca68.pt",
        "dpt_hybrid": "weights/dpt_hybrid-ade20k-53898607.pt",
    }

    if args.model_weights is None:
        args.model_weights = default_models[args.model_type]

    # set torch options
    torch.backends.cudnn.enabled = True
    torch.backends.cudnn.benchmark = True

    # compute segmentation maps
    DPTSegmentationModel.run(
        args.input_path,
        args.output_path,
        args.model_weights,
        args.model_type,
        args.optimize,
    )

