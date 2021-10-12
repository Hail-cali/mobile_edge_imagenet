import json
import torch
import collections
import queue
import utils.debug

MAX_MSG_SIZE = 8000

async def read_stream(reader, user_queue):
    # read data from stream(reader)
    # write data to pipeline(queue)
    print(f'check is queue empty {user_queue.qsize()==0}', end=' ')
    data: bytes

    while True:
        packet = await reader.read(MAX_MSG_SIZE)
        user_queue.put_nowait(packet)
        if packet.endswith(b'\n'):
            # print(packet[-10:])
            break

    print(f'-> write pipeline: {user_queue.qsize()}')

async def process_stream(user_queue):
    # without using send_signal -> msg_size
    print('proces_stream')
    params: bytes = b''
    while not user_queue.empty():
        params += user_queue.get_nowait()

    decoded = unpack_params(params)
    result = to_torch_params(decoded)

    print(f'-> read & process stream')
    return result


async def send_stream(writer, who, params):
    writer.write(params)
    await writer.drain()
    print(f'-> {who} send stream')


class TorchEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, torch.Tensor):
            return obj.cpu().tolist()
        return json.JSONEncoder.default(self, obj)

class TorchDecoder(json.JSONDecoder):

    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.to_torch)

    def to_torch(self, obj):
        defalut = collections.OrderedDict()

        if ('params' in obj.keys()):

            if isinstance(list(obj['params'].values())[0], list):
                for k, v in obj['params'].items():
                    defalut[k] = torch.Tensor(v)

                obj['params'] = defalut

        return obj

def pack_params(history):
    utils.debug.debug_comm(history, 'pack_phrase')
    return (json.dumps(history, cls=TorchEncoder)+'\n').encode()

def unpack_params_torch(params):
    return json.loads(params[:-1].decode(), cls=TorchDecoder)

def unpack_params(send):
    utils.debug.debug_comm(send, 'unpack_phrase')
    return json.loads(send[:-1].decode())

def _to_torch(his):
    utils.debug.debug_comm(his, 'to_torch_phrase')
    params = collections.OrderedDict()
    for k, v in his['params'].items():
        params[k] = torch.Tensor(v)
    return params

def to_torch_params(his):
    his['params'] = _to_torch(his)
    return his











def conv_history(his):

    if not isinstance(his, dict):
        print(f'Not imple error')
        return None

    his.update({'train_los': _tolist(his['train_los'])})
    his.update({'val_los': _tolist(his['val_los'])})
    his.update({'train_acc': _tolist(his['train_acc'])})
    his.update({'val_acc': _tolist(his['val_acc'])})

    return his


def _tolist(obj):
    return obj.cpu().tolist()

# def msg_recv(mes):
#     return json.loads(mes.decode())
#
# def msg_req(mes):
#     return json.dumps(mes).encode()


# def params_request_sub(history, model_params):
#
#     if isinstance(history['params'], collections.OrderedDict):
#         temp = {k: v.cpu().tolist() for k, v in history.pop('params').items()}
#     else:
#         temp = history
#
#     temp.update(history)
#     send = json.dumps(temp)
#     return send

