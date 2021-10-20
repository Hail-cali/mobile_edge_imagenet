# server

import asyncio
from random import random
from models.set_model import *
from comunicate.request import *

import utils.debug

# this is for Version compatibility (func wrapper for server side)
# if need to use wrapper, change mode to True

mode = False
if mode:
    from opt import parse_opts
    OPT = parse_opts()
    SERVER_PORT = OPT.SERVER_PORT
    SERVER_HOST = OPT.SERVER_HOST


class BaseServer:

    def __init__(self,
                 opt,
                 name: str,
                 ):

        self.opt = opt
        self.name = name
        self.host = self.opt.SERVER_HOST
        self.port = self.opt.SERVER_PORT

        self.user = defaultdict(int)

        self._info: dict = {'state': None, 'terminate': False}
        self.end = f'if '
        self.data = 1

        self.model = None
        self.history = None

    async def __aenter__(self):
        await asyncio.sleep(1.0)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


    async def run(self):

        pass

    async def handler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):

        pass


class FedServer(BaseServer):

    def __init__(self, emp=None, **kwargs):
        super().__init__(**kwargs)
        self.emp = emp


    def register(self, client):
        # value is count
        if client:
            self.user[client] += 1

    def update_train(self, params):
        if isinstance(params, dict):
            # self.history = params
            self.history.update(params)
            self.model.load_state_dict(copy.deepcopy(self.history['params']), strict=False)

        else:
            print(f'Type Error: check parmas')
            self._info['state'] = 'cracked'



    async def run(self):

        self.model = load_model(self.opt)

        loaders, criterion, optimizer, self.history, model_params, device = set_model(
            self.model,
            self.opt,
            dpath='../dataset/cifar-10-batches-py', file=3,
            train_size=0.8,
            batch_size=40,
            testmode=self.opt.testmode)


        server = await asyncio.start_server(self.handler, host=self.opt.SERVER_HOST, port=self.opt.SERVER_PORT)

        addr = server.sockets[0].getsockname()

        print(f"\n{'=' * 15}PIPE SERVING ON {addr}{'=' * 15}\n")


        async with server:
            await server.serve_forever()


    async def handler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):

        hashqueue = defaultdict(asyncio.Queue)
        client = writer.get_extra_info('peername')

        self.register(client)
        print(f'[C: {client}] Conneted')

        if self.opt.testmode:
            print(f'run test mode with dataset size ')

        while True:
            client = writer.get_extra_info('peername')

            await read_stream(reader, hashqueue[client])
            params: dict = await process_stream(hashqueue[client])

            self.update_train(params)

            utils.debug.debug_history(self.history, 'server after read')

            await asyncio.sleep(random() * 2)
            packed = pack_params(self.history)
            await send_stream(writer, '[S]', packed)










# func
async def run_pipe():

    model = load_model(OPT)

    loaders, criterion, optimizer, history, model_params, device = set_model(
        model,
        OPT,
        dpath='../dataset/cifar-10-batches-py', file=3,
        train_size=0.8,
        batch_size=40,
        testmode=OPT.testmode)

    async def stream_handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):

        hashqueue = defaultdict(asyncio.Queue)
        client = writer.get_extra_info('peername')
        print(f'[C: {client}] Conneted')
        if OPT.testmode:
            print(f'run test mode with dataset size ')

        while True:

            client = writer.get_extra_info('peername')

            await read_stream(reader, hashqueue[client])
            params: dict = await process_stream(hashqueue[client])
            history = params

            model.load_state_dict(copy.deepcopy(history['params']), strict=False)
            history['params'] = copy.deepcopy(model.state_dict())

            utils.debug.debug_history(history, 'server after read')

            await asyncio.sleep(random() * 2)
            packed = pack_params(history)
            await send_stream(writer, '[S]', packed)


    # server = await asyncio.start_server(queue_handler_model, host=SERVER_HOST, port=SERVER_PORT)
    server = await asyncio.start_server(stream_handler, host=SERVER_HOST, port=SERVER_PORT)

    addr = server.sockets[0].getsockname()

    print(f"{'=' * 15}")
    print(f'PIPE SERVING ON {addr}')
    print(f"{'=' * 15}")

    async with server:
        await server.serve_forever()
