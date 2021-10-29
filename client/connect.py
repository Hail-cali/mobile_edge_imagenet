# client connect

import asyncio

from models.set_model import *
from comunicate.request import *
from utils.make_plot import history_plot

import utils.debug

MAX_MSG_SIZE = 8000

class AsyncClient:
    def __init__(self,
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

    async def __aenter__(self):
        await asyncio.sleep(1.0)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print(f'client end')
        pass

    async def run_client_model(self, host: str, port: int, opt, model_input):
        reader: asyncio.StreamReader #-> In_stream: asyncio.StreamReaderProtocol
        writer: asyncio.StreamWriter
        queue: asyncio.Queue

        history: dict
        model = model_input

        loaders, criterion, optimizer, history, model_params, device = set_model(
            model,
            opt,
            dpath='../dataset/cifar-10-batches-py',
            file=self.data,
            train_size=0.8,
            batch_size=40,
            testmode=opt.testmode)

        reader, writer = await asyncio.open_connection(host, port)
        queue = asyncio.Queue()

        print(f"{'=' * 15}")
        print(f"[C {self.name}] connected ")
        print(f"{'=' * 15}")

        opt.start_epoch = epoch = start =0
        opt.n_epochs = -1

        while epoch <= opt.n_epochs:

            if epoch == start:
                utils.debug.debug_history(history, f'client {epoch}_start')
                model.load_state_dict(copy.deepcopy(history['params']), strict=False)

            else:
                model.load_state_dict(copy.deepcopy(history['params']), strict=False)
                # model.state_dict().update(history['params'])

            # train step
            history, model_params = one_epoch_train(model, loaders, criterion, optimizer,
                                                    history, model_params, opt, device)

            #com step
            packed = pack_params(history)

            await send_stream(writer, self.name, packed)

            await read_stream(reader, queue)
            # params: dict = await process_stream(queue)
            # history = params
            history = await process_stream(queue)

            utils.debug.debug_history(history, 'client after read')

            epoch = history['epoch']


        print(f"[C {self.name}] closing connection")

        history_plot(history, 'test')

        writer.close()
        await writer.wait_closed()
