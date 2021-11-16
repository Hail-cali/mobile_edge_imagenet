import json
import torch
import collections
import queue
import utils.debug

# max msg size is differ from server's spec & communication
# it is recommended to set
MAX_MSG_SIZE = 5000
VERBOSE_SIZE = 1000


class Transport:

    def __init__(self, tasks=None):
        self.task = tasks

    async def phase(self, writer, reader, history, queue, name):

        await send_stream(writer, history, recipient='S', giver=name)

        await read_stream(reader, queue, recipient=name, giver='S')

        rep_his = await process_stream(queue, tasks=name, given='S')
        his = self.update_history(history, rep_his)

        return his

    @staticmethod
    def update_history(his, params):
        history = his

        for k, v in params.items():
            if k == 'params':
                history[k].update(v)
            elif k == 'epoch':
                history[k] = v

        return history


async def read_stream(reader, user_queue, recipient=None, giver=None):
    # read data from stream(reader)
    # write data to pipeline(queue)
    # print(user_queue.qsize() == 0)
    print(f'[{recipient}] read stream from {giver}', end=': ')
    data: bytes
    i = 0

    # need to fix, while mec -> set flag
    while True:
        if i % VERBOSE_SIZE == 0:
            utils.debug.process()
        packet = await reader.read(MAX_MSG_SIZE)
        user_queue.put_nowait(packet)
        if packet.endswith(b'\n'):
            # print(packet[-10:])
            break
        i += 1
    print(f'-> done : queue size({user_queue.qsize()})')

async def process_stream(user_queue, tasks=None, given=None):
    # without using send_signal -> msg_size
    print(f'[{tasks}] process_stream from {given}', end=': ')
    params: bytes = b''
    i = 0
    while not user_queue.empty():
        params += user_queue.get_nowait()

        if i % VERBOSE_SIZE == 0:
            utils.debug.process()
        i += 1

    decoded = unpack_params(params)
    result = to_torch_params(decoded)

    print(f'-> done')
    return result

async def send_stream(writer, params, recipient=None, giver=None):
    print(f'[{giver}] send stream to {recipient}: ', end=' ')

    packed = pack_params(params)
    writer.write(packed)
    await writer.drain()
    print(f'-> done')

async def stream_decoder(user_queue, tasks=None, given=None):

    print(f'[{tasks}] stream decoder from {given}', end=': ')
    params: bytes = b''
    i = 0
    while not user_queue.empty():
        params += user_queue.get_nowait()
        if i % VERBOSE_SIZE == 0:
            utils.debug.process()
        i += 1

    result = unpack_params_torch(params)

    print(f'-> done')
    return result




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
                    defalut[k] = torch.tensor(v)

                obj['params'] = defalut

        return obj

def pack_params(history):
    # utils.debug.debug_comm(history, 'pack_phrase')
    return (json.dumps(history, cls=TorchEncoder)+'\n').encode()

def unpack_params_torch(params):
    return json.loads(params[:-1].decode(), cls=TorchDecoder)

def unpack_params(send):
    # utils.debug.debug_comm(send, 'unpack_phrase')
    return json.loads(send[:-1].decode())

def _to_torch(his):
    # utils.debug.debug_comm(his, 'to_torch_phrase')
    # params = collections.OrderedDict()
    params = dict()
    for k, v in his['params'].items():

        params[k] = torch.tensor(v)

    return params

def to_torch_params(his):
    history = his
    history['params'] = _to_torch(his)
    return history




