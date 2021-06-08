
import torch
import torch.nn.functional as F




from torchvision.transforms import Compose
from dpt.models import DPTSegmentationModel
from dpt.transforms import Resize, NormalizeImage, PrepareForNet

import dpt.models
from dpt.blocks import (
        FeatureFusionBlock,
        FeatureFusionBlock_custom,
        Interpolate,
        _make_encoder,
        forward_vit,
    )
from dpt.models import DPTSegmentationModel
from nni.algorithms.compression.pytorch.quantization import QAT_Quantizer






model = DPTSegmentationModel(150)

config_list = [{
    'quant_types': ['weights'],
    'quant_bits': {
        'weights': 8,
    }, # you can just use `int` here because all `quan_types` share same bits length, see config for `ReLu6` below.
    'op_types':['Conv2d', 'linear']
}, {
    'quant_types': ['output'],
    'quant_bits': 8,
    'quant_start_step': 7000,
    'op_types':['ReLU']
}]
quantizer = QAT_Quantizer(model, config_list)
quantizer.compress()