# client
import asyncio
from random import random
import time
import sys
from server.set_model import *
from comunicate.request import *

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

    async def run_client(self, host: str, port: int):
        reader: asyncio.StreamReader
        writer: asyncio.StreamWriter

        model, loaders, criterion, optimizer, history, model_params, device = set_model(
            dpath='../dataset/cifar-10-batches-py', file=1,
            train_size=0.8, batch_size=40)
        opt = parse_opts()

        reader, writer = await asyncio.open_connection(host, port)

        print(f"{'=' * 5}")
        print(f"[C {self.name}] connected {'=' * 10}")
        print(f"{'=' * 5}")



        while True:
            # line = sys.stdin.readline().strip()
            line = f"{self.name}@:"+input(f"[C {self.name}] enter message: ")
            if not line:
                break

            payload = line.encode()
            writer.write(payload)
            await writer.drain()
            # print(f"[C {self.name}] sent: {len(payload)} bytes\n")

            data = await reader.read(1024)
            print(f"[C {self.name}] received : {len(data)} bytes")
            print(f"[C {self.name}] message : {data.decode()} ")

            if line[len(self.name)+2:] == 'exit':
                break

        print(f"[C {self.name}] closing connection")
        writer.close()
        await writer.wait_closed()


    async def run_client_model(self, host: str, port: int, opt, model):
        reader: asyncio.StreamReader
        writer: asyncio.StreamWriter

        loaders, criterion, optimizer, history, model_params, device = set_model(
            model,
            dpath='../dataset/cifar-10-batches-py',
            file=1,
            train_size=0.8,
            batch_size=40,
            testmode=True)


        reader, writer = await asyncio.open_connection(host, port)

        print(f"{'=' * 5}")
        print(f"[C {self.name}] connected {'=' * 10}")
        print(f"{'=' * 5}")

        opt.start_epoch = epoch = 1
        opt.n_epochs = 2

        while epoch <= opt.n_epochs:
            # line = sys.stdin.readline().strip()
            model.load_state_dict(copy.deepcopy(history['params']))
            history, model_params = one_epoch_train(model, loaders, criterion, optimizer, history, model_params, device)

            send = params_request(history)
            writer.write(send)
            await writer.drain()

            recv_msg = ''
            msg_len = len(send) + 10
            while len(recv_msg) < msg_len:
                recv_msg += await reader.read(MAX_MSG_SIZE)

            # recv_msg = await reader.read(1024)

            history = params_response(recv_msg)

            epoch = history['epoch']
            print(f"[C {self.name}] received : {len(recv_msg)} bytes")

        print(f"[C {self.name}] closing connection")

        history_plot(history, 'test')
        writer.close()
        await writer.wait_closed()





async def run_client(name: str , host: str, port: int):
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter
    reader, writer = await asyncio.open_connection(host, port)
    print(f"{'='*5}")
    print(f"[C {name}] connected {'='*10}")
    print(f"{'=' * 5}")

    while True:
        line = sys.stdin.readline().strip()
        # line = input(f"[C {name}] enter message: ")
        if not line:
            break

        payload = line.encode()
        writer.write(payload)
        await writer.drain()
        print(f"[C {name}] sent: {len(payload)} bytes\n")


        data = await reader.read(1024)
        print(f"[C {name}] received : {len(data)} bytes")
        print(f"[C {name}] message : {data.decode()} ")

    print(f"[C {name}] closing connection")
    writer.close()
    await writer.wait_closed()
