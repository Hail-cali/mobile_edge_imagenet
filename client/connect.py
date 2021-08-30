import asyncio
from random import random


async def run_client(host: str, port: int):
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter
    reader, writer = await asyncio.open_connection(host, port)

    print(f'{host} connected')

    while True:
        line = input(f'enter message: ')
        if not line:
            break

        payload = line.encode()

        writer.write(payload)

        await writer.drain()
        print(f'sent: {len(payload)} bytes\n')

        data = await reader.read(1024)
        print(f'received : {len(data)} bytes')

    print(f'closing connection')
    writer.close()

    await writer.wait_closed()
