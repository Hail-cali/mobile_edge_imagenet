from torch import nn



class BasePredictor(nn.Module):

    def __init__(self, h=200, out=10):

        self.h = h
        self.out = out
        self.a = 0.01
        self.b = 0.001







