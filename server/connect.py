# server

import asyncio
from collections import defaultdict
from random import random
import sys
from models.set_model import *
from opt import parse_opts
from comunicate.request import *



OPT = parse_opts()

# SERVER_PORT = 8080
# SERVER_HOST = '127.0.0.1'
SERVER_PORT = OPT.SERVER_PORT
SERVER_HOST = OPT.SERVER_HOST



async def run_pipe():

    model = load_model(OPT)

    loaders, criterion, optimizer, history, model_params, device = set_model(
        model,
        OPT,
        dpath='../dataset/cifar-10-batches-py', file=3,
        train_size=0.8,
        batch_size=40,
        testmode=True)

    async def queue_handler_model(reader: asyncio.StreamReader, writer: asyncio.StreamWriter, ):



        # hashqueue = defaultdict(asyncio.Queue)

        while True:

            data: bytes = await reader.read(10000)

            peername = writer.get_extra_info('peername')
            print(f'[S] received {len(data)} bytes from {peername}')
            # hashqueue[peername].put_nowait(data)

            recv = msg_recv(data)

            try:
                if recv[list(recv.keys())[0]]['size']:
                    msg_size = recv[list(recv.keys())[0]]['size']
                    print(f'server recv msg size {msg_size}')
                    # await asyncio.sleep(random() * 2)
                    params: bytes = await read_stream(reader, msg_size)
                    print(f'parmas byte size : {len(params)}')

                    temp = unpack_params(params)
                    print(f'temp type {temp.keys()}')

            except:
                pass

            req = msg_req(recv)

            await asyncio.sleep(random() * 2)
            writer.write(req)
            await writer.drain()
    async def stream_handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):

        hashqueue = defaultdict(asyncio.Queue)
        client = writer.get_extra_info('peername')
        print(f'[C: {client}] Conneted')

        while True:

            client = writer.get_extra_info('peername')

            await read_stream(reader, hashqueue[client])
            params: dict = await process_stream(hashqueue[client])
            print(params.keys())

            await asyncio.sleep(random() * 2)
            packed = pack_params(params)
            await send_stream(writer, '[S]', packed)


    # server = await asyncio.start_server(queue_handler_model, host=SERVER_HOST, port=SERVER_PORT)
    server = await asyncio.start_server(stream_handler, host=SERVER_HOST, port=SERVER_PORT)

    addr = server.sockets[0].getsockname()

    print(f"{'=' * 15}")
    print(f'PIPE SERVING ON {addr}')
    print(f"{'=' * 15}")

    async with server:
        await server.serve_forever()
