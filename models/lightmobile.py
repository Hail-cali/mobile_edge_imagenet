import torch
from functools import partial
from torch import nn, Tensor
from torchvision.models.mobilenet import mobilenet_v3_small, mobilenet_v2




class LightMobileNet(nn.Module):

    def __init__(self, pretrained=True, input_size=32, num_class=100):
        super(LightMobileNet, self).__init__()
        self.pretrained = pretrained
        self.input_size = input_size
        self.num_class = num_class

    def load(self):
        if self.pretrained:
            # return mobilenet_v2(pretrained=True)
            return mobilenet_v3_small(pretrained=True)




