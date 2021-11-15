import torch
import numpy as np
from torch import nn
from models import lightmobile
from collections import defaultdict


def wrapper_activate(*args, **kwargs):

    result = defaultdict()
    size = len(kwargs)

    for c, kv in kwargs.items():

            for k, v in kv.items():
                if k == 'params' or k == 'epoch':
                    try:
                        result[k] += v

                    except:
                        result[k] = v

                elif k in ['train_los', 'val_los', 'train_acc', 'val_acc']:
                    try:
                        result[k] = [pre+post for pre, post in zip(result[k], v)]
                    except:
                        result[k] = v

    for k, v in result.items():
        if torch.is_tensor(v):
            result[k] = torch.div(v, size)

        elif isinstance(v, np.ndarray):
            result[k] = np.divide(v, size)

        elif isinstance(v, list):
            result[k] = [val/size for val in result[k]]

        elif isinstance(v, int):
            result[k] = v / size

    return result



class BaseModel(nn.Module):

    def activate(self, *args, **kwargs):

        raise NotImplementedError('for edge learning framework, need to set this method')


class FedAvg2(BaseModel):


    pass




class FedAvg(BaseModel):

    def __init__(self, h=10, out=20, opt=None, data_path=None, **kwargs):
        super().__init__(**kwargs)
        self.h = h
        self.out = out
        self.s = lightmobile.LightMobileNet(pretrained=opt.pretrained).load()
        self.data_path = data_path

    def __call__(self, *args, **kwargs):
        return self.s(*args, **kwargs)

    def activate(self, *args, **kwargs):

        '''
        it it base method for frame work training
        '''

        result = defaultdict()
        size = len(kwargs)

        for c, kv in kwargs.items():

            for k, v in kv.items():
                if k == 'params' or k == 'epoch':
                    try:
                        result[k] += v

                    except:
                        result[k] = v

        for k, v in result.items():
            if torch.is_tensor(v):
                result[k] = torch.div(v, size)

            elif isinstance(v, np.ndarray):
                result[k] = np.divide(v, size)

            elif isinstance(v, int):
                result[k] = v / size

        return result

    def end_page(self):


        pass

if __name__ == '__main__':
    import opt
    from collections import defaultdict
    OPT = opt.parse_opts()
    model = FedAvg(opt=OPT)

    sample_dict1 = {'a':10, 'b':20, 'c':30}
    sample_dict2 = {'a':40, 'b':10, 'c':10}

    total_dict = defaultdict()
    total_dict['1'] = sample_dict1
    total_dict['2'] = sample_dict2
    print(f'outside: {total_dict}')
    result = model.activate(**total_dict)
    print(result)


    temp_ = [1,2,3]
    temp__ = [5,6,7]
    print(temp__ + temp_)
    print(list(map(lambda x, y: x + y, temp__, temp_ )))
