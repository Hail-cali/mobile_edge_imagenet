# client connect

import asyncio

from worker.set import *
from communicate.request import *
from communicate.stream import ComStream
from utils.make_plot import history_plot, suffix_name, prefix_name, logger

from worker.set import CustomSetter

MAX_MSG_SIZE = 8000

from fed.rule import ReadyPhase, TrainPhase, CommunicatePhase


class CustomClient:
    def __init__(self,
                 name: str,
                 host: str,
                 port: int,
                 ):
        '''
        :param name:
        :param host:
        :param port:
        :argument data: Int
        '''

        self.name = name
        self.host = host
        self.port = port

        print(f'with hugging phase client class ')

    async def run_client_model(self, host: str, port: int, opt, model_input, dataset):
        reader: asyncio.StreamReader #-> In_stream: asyncio.StreamReaderProtocol
        writer: asyncio.StreamWriter
        queue: asyncio.Queue

        history: dict
        model = model_input

        worker = ReadyPhase(worker=CustomSetter())


        model, loaders, criterion, optimizer, history, model_params, opt, device = worker(
            model, dataset, opt)



        com_stream = ComStream(*await asyncio.open_connection(host, port), queue=asyncio.Queue())

        cs = CommunicatePhase(streamer=com_stream, transport=None)

        # reader, writer = await asyncio.open_connection(host, port)
        # queue = asyncio.Queue()


        print(f"{'=' * 30}")
        print(f"{'|' * 1} [C {self.name}] connected to {self.host}:{self.port} {'|' * 1}")
        print(f"{'=' * 30}")

        epoch = opt.start_epoch
        start = opt.start_epoch

        while epoch <= opt.n_epochs:

            if epoch == start:
                # utils.debug.debug_history(history, f'client {epoch}_start')
                model.load_state_dict(copy.deepcopy(history['params']), strict=False)

            else:
                model.load_state_dict(copy.deepcopy(history['params']), strict=False)

            tr = TrainPhase()
            history = tr(model, loaders, criterion, optimizer,
                                                    history, model_params, opt, device)
            model_params = tr.best

            # communication step
            rep_his = await cs(dict((k, v) for k, v in history.items() if k in ['params']), self.name)

            history = self.update_history(history, rep_his)

            # utils.debug.debug_history(history, 'client after read')

            history, epoch = self.update_epoch(history)


            if epoch % opt.log_interval == 0:
                logger(history, prefix_name(term='short')+suffix_name(opt))

        # # end-page

        # await send_stream(writer, history, recipient='S', giver=self.name)

        print(f"[C {self.name}] closing connection")

        # save history
        history_plot(history, prefix_name(term='short')+suffix_name(opt))
        logger(history, prefix_name(term='short')+suffix_name(opt))

        cs.close()
        # await writer.wait_closed()

    @staticmethod
    def update_history(his, params):
        history = his

        for k, v in params.items():
            if k == 'params':
                history[k].update(v)

        return history

    @staticmethod
    def update_epoch(history):

        out = history

        if 'epoch' in out.keys():
            out['epoch'] += 1

        return out, out['epoch']




class FedClient:
    def __init__(self,
                 name: str,
                 host: str,
                 port: int,
                 data: int):
        '''
        :param name:
        :param host:
        :param port:
        :argument data: Int
        '''

        self.name = name
        self.host = host
        self.port = port
        self.data = data
        print(f'with hugging phase client class ')

    async def run_client_model(self, host: str, port: int, opt, model_input):
        reader: asyncio.StreamReader #-> In_stream: asyncio.StreamReaderProtocol
        writer: asyncio.StreamWriter
        queue: asyncio.Queue

        history: dict
        model = model_input

        worker = ReadyPhase(worker=None)


        model, loaders, criterion, optimizer, history, model_params, opt, device = worker(
            model, opt, file=self.data, testmode=opt.testmode)

        # model, loaders, criterion, optimizer, history, model_params, opt, device = worker(
        #     model, dataset, opt)



        com_stream = ComStream(*await asyncio.open_connection(host, port), queue=asyncio.Queue())

        cs = CommunicatePhase(streamer=com_stream, transport=None)

        # reader, writer = await asyncio.open_connection(host, port)
        # queue = asyncio.Queue()


        print(f"{'=' * 30}")
        print(f"{'|' * 1} [C {self.name}] connected to {self.host}:{self.port} {'|' * 1}")
        print(f"{'=' * 30}")

        epoch = opt.start_epoch
        start = opt.start_epoch

        while epoch <= opt.n_epochs:

            if epoch == start:
                # utils.debug.debug_history(history, f'client {epoch}_start')
                model.load_state_dict(copy.deepcopy(history['params']), strict=False)

            else:
                model.load_state_dict(copy.deepcopy(history['params']), strict=False)

            tr = TrainPhase()
            history = tr(model, loaders, criterion, optimizer,
                                                    history, model_params, opt, device)
            model_params = tr.best

            # communication step
            rep_his = await cs(dict((k, v) for k, v in history.items() if k in ['params']), self.name)

            history = self.update_history(history, rep_his)

            # utils.debug.debug_history(history, 'client after read')

            history, epoch = self.update_epoch(history)


            if epoch % opt.log_interval == 0:
                logger(history, prefix_name(term='short')+suffix_name(opt))

        # # end-page

        # await send_stream(writer, history, recipient='S', giver=self.name)

        print(f"[C {self.name}] closing connection")

        # save history
        history_plot(history, prefix_name(term='short')+suffix_name(opt))
        logger(history, prefix_name(term='short')+suffix_name(opt))

        cs.close()
        # await writer.wait_closed()

    @staticmethod
    def update_history(his, params):
        history = his

        for k, v in params.items():
            if k == 'params':
                history[k].update(v)

        return history

    @staticmethod
    def update_epoch(history):

        out = history

        if 'epoch' in out.keys():
            out['epoch'] += 1

        return out, out['epoch']




class AsyncClient:

    def __init__(self,
                 name: str,
                 host: str,
                 port: int,
                 data: int):

        '''
        :param name:
        :param host:
        :param port:
        :argument data: Int
        '''

        self.name = name
        self.host = host
        self.port = port
        self.data = data
        print(f'old version client used')

    async def __aenter__(self):
        pass

    async def __aexit__(self, exc_type, exc_val, exc_tb):

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

        print(f"{'=' * 30}")
        print(f"{'|' * 1} [C {self.name}] connected to {self.host}:{self.port} {'|' * 1}")
        print(f"{'=' * 30}")

        # opt.start_epoch = epoch = start = 1
        epoch = opt.start_epoch
        start = opt.start_epoch
        # opt.n_epochs = 3

        while epoch <= opt.n_epochs:

            if epoch == start:
                # utils.debug.debug_history(history, f'client {epoch}_start')
                model.load_state_dict(copy.deepcopy(history['params']), strict=False)

            else:
                model.load_state_dict(copy.deepcopy(history['params']), strict=False)

            print(f'EPOCH: [{epoch}/{opt.n_epochs}]')
            # train step
            history, model_params = one_epoch_train(model, loaders, criterion, optimizer,
                                                    history, model_params, opt, device)


            # communication step

            await send_stream(writer, history, recipient='S', giver=self.name)

            await read_stream(reader, queue, recipient=self.name, giver='S')

            rep_his = await process_stream(queue, tasks=self.name, given='S')
            history = self.update_history(history, rep_his)

            # utils.debug.debug_history(history, 'client after read')

            epoch = history['epoch']

            if epoch % opt.log_interval == 0:
                logger(history, prefix_name(term='short')+suffix_name(opt))

        # end-page
        await send_stream(writer, history, recipient='S', giver=self.name)

        print(f"[C {self.name}] closing connection")

        # save history
        history_plot(history, prefix_name(term='short')+suffix_name(opt))
        logger(history, prefix_name(term='short')+suffix_name(opt))

        writer.close()
        await writer.wait_closed()

    @staticmethod
    def update_history(his, params):
        history = his

        for k, v in params.items():
            if k == 'params':
                history[k].update(v)
            elif k == 'epoch':
                history[k] = v + 1

        return history

