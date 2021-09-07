import asyncio
import os
import sys
WORKING_DIR_AND_PYTHON_PATHS = os.path.join('/', *os.getcwd().split("/")[:-1])
# print(f'before {sys.path}')
sys.path.append(WORKING_DIR_AND_PYTHON_PATHS)
# print(f'after {sys.path}')

from server.connect import *
from client.connect import *


CLIENT_PORT = 8080
CLIENT_HOST = "127.0.0.1"


async def single():
    await asyncio.wait([
                        AsyncClient(name='client_3', host=CLIENT_HOST, port=CLIENT_PORT
                                    ).run_client(CLIENT_HOST, CLIENT_PORT),

                        ])


async def client():
    await asyncio.wait([
                        AsyncClient(name='client_1', host=CLIENT_HOST, port=CLIENT_PORT
                                    ).run_client(CLIENT_HOST, CLIENT_PORT),
                        AsyncClient(name='client_2', host=CLIENT_HOST, port=CLIENT_PORT
                                    ).run_client(CLIENT_HOST, CLIENT_PORT),
                        ])


if __name__ == '__main__':
    asyncio.run(single())
    # asyncio.run(client())
