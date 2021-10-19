# server

import asyncio
from collections import defaultdict
from random import random
import sys
from models.set_model import *
from opt import parse_opts
from comunicate.request import *

import utils.debug

OPT = parse_opts()

# SERVER_PORT = 8080
# SERVER_HOST = '127.0.0.1'
SERVER_PORT = OPT.SERVER_PORT
SERVER_HOST = OPT.SERVER_HOST

class BaseServer:

    def __init__(self,
                 opt,
                 name: str,
                 host: str,
                 port: int):

        '''
        :param name:
        :param host:
        :param port:
        :argument data: Int
        '''

        self.name = name
        self.host = host
        self.port = port
        self.data = 1
        self.opt = opt

    async def __aenter__(self):
        await asyncio.sleep(1.0)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


    async def run(self):

        pass

    async def handler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):

        pass


class FedServer(BaseServer):

    def __init__(self,
                 opt,
                 name: str,
                 host: str,
                 port: int):

        '''
        :param name:
        :param host:
        :param port:
        :argument data: Int
        '''

        self.name = name
        self.host = host
        self.port = port
        self.data = 1
        self.opt = opt
        self.history = dict()

    @property
    def history(self, new):
        self.history.update(new)

    @history.getter
    def history(self):
        return self.history

    async def run(self):

        model = load_model(OPT)

        loaders, criterion, optimizer, self.history, model_params, device = set_model(
            model,
            OPT,
            dpath='../dataset/cifar-10-batches-py', file=3,
            train_size=0.8,
            batch_size=40,
            testmode=OPT.testmode)


        server = await asyncio.start_server(self.handler, host=SERVER_HOST, port=SERVER_PORT)

        addr = server.sockets[0].getsockname()

        print(f"{'=' * 15}PIPE SERVING ON {addr}{'=' * 15}")
        print(f"{'*' *5}")

        async with server:
            await server.serve_forever()


    async def handler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):

        hashqueue = defaultdict(asyncio.Queue)
        client = writer.get_extra_info('peername')
        print(f'[C: {client}] Conneted')
        if OPT.testmode:
            print(f'run test mode with dataset size ')

        while True:
            client = writer.get_extra_info('peername')

            await read_stream(reader, hashqueue[client])
            params: dict = await process_stream(hashqueue[client])
            self.history = params

            model.load_state_dict(copy.deepcopy(history['params']), strict=False)
            history['params'] = copy.deepcopy(model.state_dict())

            utils.debug.debug_history(history, 'server after read')

            await asyncio.sleep(random() * 2)
            packed = pack_params(history)
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
