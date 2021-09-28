import json
import torch
import collections

MAX_MSG_SIZE = 8000

async def send_signal(writer, who, packed):
    print(f'is in signal first?')

    msg = {f'{who}': {f'size': len(packed)}}
    # msg_size = f'{client}@size@:{len(send)}'.encode()
    writer.write(json.dumps(msg).encode())
    await writer.drain()


async def send_stream(writer, who, params):
    print(f'is in stream next?')
    writer.write(params)
    await writer.drain()


async def read_stream(reader, msg_size):

    recv_msg: bytes = b''

    while len(recv_msg) < msg_size:
        recv_msg += await reader.read(MAX_MSG_SIZE)

    return recv_msg


class TorchEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, torch.Tensor):
            return obj.cpu().tolist()
        return json.JSONEncoder.default(self, obj)

def pack_params(history):
    return json.dumps(history, cls=TorchEncoder).encode()

def unpack_params(send):
    return json.loads(send.decode())

def msg_recv(mes):
    return json.loads(mes.decode())

def msg_req(mes):
    return json.dumps(mes).encode()




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


