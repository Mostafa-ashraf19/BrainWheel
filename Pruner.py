from nni.algorithms.compression.pytorch.quantization import QAT_Quantizer
from models import DPTSegmentationModel
model = DPTSegmentationModel

config_list = [{
    'quant_types': ['parameters'],
    'quant_bits': {
        'parameter': 8,
    }, # you can just use `int` here because all `quan_types` share same bits length, see config for `ReLu6` below.
    'op_types':['Conv2d', 'Linear']
}, {
    'quant_types': ['output'],
    'quant_bits': 8,
    'quant_start_step': 7000,
    'op_types':['ReLU6']
}]
quantizer = QAT_Quantizer(model, config_list)
quantizer.compress()