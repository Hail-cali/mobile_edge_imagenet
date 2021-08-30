import asyncio
from random import random


_port = 58441

async def handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    while True:

        data: bytes = await reader.read(1024)

        peername = writer.get_extra_info('peername')
        print(f'[S] received {len(data)} bytes from {peername}')
        mes = data.decode()
        print(f'[S] message: {mes}')
        res = mes.upper()[::-1]

        await asyncio.sleep(random() * 2)
        writer.write(res.encode())



async def run_server():

    server = await asyncio.start_server(handler, host='127.0.0.1', port=_port)

    async with server:
        await server.serve_forever()

