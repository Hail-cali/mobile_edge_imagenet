from torch import nn
from models.lightmobile import LightMobileNet
from models.set_model import load_model


class FedDistill(nn.Module):

    def __init__(self, h=10, out=20, opt=None, data_path=None):
        self.h = h
        self.out = out

        self.model = self._struct_student(opt)
        self.data_path = data_path

    def _struct_student(self, opt):
        return load_model(opt)


