import json
import pickle
import matplotlib.pyplot as plt
import torch
import collections

class TorchEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, torch.Tensor):
            return obj.cpu().tolist()
        return json.JSONEncoder.default(self, obj)
def params_request(history):
    return json.dumps(history, cls=TorchEncoder)

def params_response(send):
    return json.loads(send)

def params_request_sub(history, model_params):

    if isinstance(history['params'], collections.OrderedDict):
        temp = {k: v.cpu().tolist() for k, v in history.pop('params').items()}
    else:
        temp = history

    temp.update(history)
    send = json.dumps(temp)
    return send


if __name__ == '__main__':


    pass


