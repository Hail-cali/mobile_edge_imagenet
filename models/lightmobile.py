import torch
from functools import partial
from torch import nn, Tensor
from torchvision.models.mobilenet import mobilenet_v3_small




class LightMobileNet(nn.Module):

    def __init__(self, pretrained=True):
        super(LightMobileNet, self).__init__()
        self.pretrained = pretrained


    def load(self):
        if self.pretrained:
            return mobilenet_v3_small(pretrained=True)




