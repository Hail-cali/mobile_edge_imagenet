# server

import asyncio
from random import random
import sys
from functools import partial
from server.set_model import *




SERVER_PORT = 8080
SERVER_HOST = '127.0.0.1'

def handle_stdin(queue):
    data = sys.stdin.readline().strip()
    if data =='q':
        loop = asyncio.get_event_loop()
        loop.remove_reader(sys.stdin)
    asyncio.ensure_future(queue.put(data))

async def tick(queue):
    stop = False
    while not stop:

        data = await queue.get()
        print(f'Data received: {data}')

        if data == 'q':
            stop =True
        print('tick finished')


async def queue_handler_model(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    model, loaders, criterion, optimizer, history, model_params, device = set_model(
        dpath='../dataset/cifar-10-batches-py', file=3,
        train_size=0.8, batch_size=40)

    queue = asyncio.Queue()
    userqueue = ''

    while True:
        data: bytes = await reader.read(1024)

        peername = writer.get_extra_info('peername')

        print(f'[S] received {len(data)} bytes from {peername}')
        mes = data
        print(f'[S] message: {mes}')
        # res = mes.upper().split('@:')[-1]

        await asyncio.sleep(random() * 2)
        writer.write(mes)
        await writer.drain()

async def queue_handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):

    model, loaders, criterion, optimizer, history, model_params, device = set_model(
        dpath='../dataset/cifar-10-batches-py', file=3,
        train_size=0.8, batch_size=40)

    queue = asyncio.Queue()
    userqueue = ''

    while True:

        data: bytes = await reader.read(1024)

        peername = writer.get_extra_info('peername')

        print(f'[S] received {len(data)} bytes from {peername}')
        mes = data.decode()
        print(f'[S] message: {mes}')
        res = mes.upper().split('@:')[-1]

        await asyncio.sleep(random() * 2)
        writer.write(res.encode())
        await writer.drain()



async def handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    print(f'[S] server handler ')
    mes = 'start'
    while True:

        data: bytes = await reader.read(1024)

        peername = writer.get_extra_info('peername')

        print(f'[S] received {len(data)} bytes from {peername}')
        mes = data.decode()
        print(f'[S] message: {mes}')
        res = mes.upper()[::-1]

        await asyncio.sleep(random() * 2)
        writer.write(res.encode())
        await writer.drain()
        if mes == 'exit':
            pass



async def run_server():

    server = await asyncio.start_server(handler, host=SERVER_HOST, port=SERVER_PORT)
    addr = server.sockets[0].getsockname()
    print(f'SERVING ON {addr}')
    async with server:
        await server.serve_forever()
    # asyncio.get_event_loop().run_until_complete()

async def run_pipe():

    server = await asyncio.start_server(queue_handler_model, host=SERVER_HOST, port=SERVER_PORT)
    addr = server.sockets[0].getsockname()

    print(f'PIPE SERVING ON {addr}')
    async with server:
        await server.serve_forever()
