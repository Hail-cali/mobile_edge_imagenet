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

        self.name = name
        self.host = host
        self.port = port

    async def __aenter__(self):
        await asyncio.sleep(1.0)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def run_client_model(self, host: str, port: int, opt, model):
        reader: asyncio.StreamReader #-> In_stream: asyncio.StreamReaderProtocol
        writer: asyncio.StreamWriter
        queue: asyncio.Queue

        history: dict


        loaders, criterion, optimizer, history, model_params, device = set_model(
            model,
            opt,
            dpath='../dataset/cifar-10-batches-py',
            file=1,
            train_size=0.8,
            batch_size=40,
            testmode=True)

        reader, writer = await asyncio.open_connection(host, port)
        queue = asyncio.Queue()

        print(f"{'=' * 15}")
        print(f"[C {self.name}] connected ")
        print(f"{'=' * 15}")

        opt.start_epoch = epoch = 1
        opt.n_epochs = 2

        while epoch <= opt.n_epochs:

            utils.debug.debug_history(history, 'client start')

            model.load_state_dict(copy.deepcopy(history['params']), strict=False)

            history, model_params = one_epoch_train(model, loaders, criterion, optimizer,
                                                    history, model_params, opt, device)


            packed = pack_params(history)

            await send_stream(writer, self.name, packed)

            await read_stream(reader, queue)
            params: dict = await process_stream(queue)

            history = params

            utils.debug.debug_history(history, 'client after read')

            epoch = history['epoch']


        print(f"[C {self.name}] closing connection")

        history_plot(history, 'test')

        writer.close()
        await writer.wait_closed()
