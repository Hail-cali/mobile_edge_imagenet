from torch import nn as nn
from torch import Tensor

def conv3x3(in_planes: int, out_planes: int, stride: int =1, groups: int =1, dilation: int= 1) -> nn.Conv2d:

    return nn.Conv2d(in_planes, out_planes, kernel_size=3, stride=stride,
                     padding=dilation, groups=groups, bias=False, dilation=dilation)

def conv1x1(in_planes: int, out_planes: int, stride: int =1) -> nn.Conv2d:

    return nn.Conv2d(in_planes, out_planes, kernel_size=1, stride=stride, bias=False)



class PinBlock(nn.Module):

    def __init__(self):
        super().__init__()
        self.conv2d = None


class PinEncoder(nn.Module):

    def __init__(self, input_shape=(16,128,128,3)):
        super().__init__()
        self.shape = input_shape





class PinNet(nn.Module):

    def __init__(self,h):
        super().__init__()
        self.h = h


