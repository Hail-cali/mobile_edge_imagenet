# server

import asyncio
import async_timeout
from random import random
from worker.set import *
from comunicate.request import *
import utils.debug

# this is for Version compatibility (func wrapper for server side)
# if need to use wrapper, change mode to True

TIMEOUT = 300


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
        print('server end')
        pass


    async def run(self):

        raise NotImplementedError(f'should set run method for fed learning')

    async def handler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):

        pass


class MultiHeadServer(BaseServer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stored_client = defaultdict()
        self.sampling = 1
        self.login = defaultdict()
        self._tolerance: int = 1
        self.timeout = self.opt.TIMEOUT
        self.epoch: int = 0

    @property
    def stored_status(self):
        return len(self.stored_client.keys())

    def register(self, client):
        if client is None:
            self.login[client] += 1
            print(f'[{client}] Connected')

    def logout(self, client):
        if client is None:
            self.login.pop(client)

    def flush(self):
        pass

    @property
    def transport_lock(self):



        return



class FedServer(BaseServer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client_params = defaultdict()
        self._tolerance: int = 1
        if not self.opt.TIMEOUT:
            self._timeout: int = TIMEOUT
        else:
            self._timeout = self.opt.TIMEOUT

        self.epoch: int = 0

    @property
    def user_size(self):
        return len(self.user.keys())

    @property
    def status(self):
        return len(self.client_params.keys())

    def register(self, client):
        # value is count
        if client:
            self.user[client] += 1
            print(f'[{client}] Connected')
        # debug
        # print(f"registered: {self.user.keys()}")

    def logout(self, client):
        if client is None:
            self.user.pop(client)


    def update_train(self):
        # must model have method named activate for fed learning
        print(f"{'-'*10}\nstart update w: fed learning", end=' ')
        if self.client_params:
            from models.distill import wrapper_activate

            params = wrapper_activate(**self.client_params)

            self.history.update(params)
            self.model.load_state_dict(copy.deepcopy(self.history['params']), strict=False)
            self.epoch += 1

        else:
            print(f'error: update step')

        print(f"->done")

    def flush(self):
        # reset stored params
        pass

    async def run(self):

        # set step
        self.model = load_model(self.opt)

        loaders, criterion, optimizer, self.history, model_params, device = set_model(
            self.model,
            self.opt,
            dpath='../dataset/cifar-10-batches-py', file=5,
            train_size=0.8,
            batch_size=40,
            testmode=self.opt.testmode)

        # start server
        server = await asyncio.start_server(self.handler, host=self.opt.SERVER_HOST, port=self.opt.SERVER_PORT)
        addr = server.sockets[0].getsockname()
        print(f"\n{'=' * 15}PIPE SERVING ON {addr}{'=' * 15}\n")

        # create loop
        async with server:
            await server.serve_forever()

    async def handler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):

        hashqueue = defaultdict(asyncio.Queue)
        client = str(writer.get_extra_info('peername')[1])

        self.register(client)

        if self.opt.testmode:
            print(f"\n{'-'*20}run test mode with small dataset size{'-'*20}\n")

        while self.epoch <= self.opt.n_epochs:
            client = str(writer.get_extra_info('peername')[1])
            print('read_stream start')
            await read_stream(reader, hashqueue[client], recipient='S', giver=client)
            params: dict = await process_stream(hashqueue[client], tasks='S', given=client)
            self.client_params[client] = params

            await self.transport(writer, client)
            # utils.debug.debug_history(self.history, 'server fed avg done')

    async def transport(self, writer, client):
        print('is transport?')
        async with async_timeout.timeout(self._timeout):
            print('here transport')
            if False:
                print('transport done ')
                self.update_train()
                await send_stream(writer, self.history, recipient=client, giver='S')








    pass



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

            await read_stream(reader, '[S]', hashqueue[client])
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
