# client
import asyncio
from random import random
import time
import sys

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
            print(f"[C {self.name}] sent: {len(payload)} bytes\n")

            data = await reader.read(1024)
            print(f"[C {self.name}] received : {len(data)} bytes")
            print(f"[C {self.name}] message : {data.decode()} ")

            if line[len(self.name)+2:] == 'exit':
                break

        print(f"[C {self.name}] closing connection")
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
