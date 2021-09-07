import asyncio
import os
import sys
WORKING_DIR_AND_PYTHON_PATHS = os.path.join('/', *os.getcwd().split("/")[:-1])
# print(f'before {sys.path}')
sys.path.append(WORKING_DIR_AND_PYTHON_PATHS)
# print(f'after {sys.path}')

from server.connect import *
from client.connect import *

#
# """
# used docker container
#
# """

CLIENT_PORT = 80
CLIENT_HOST = "127.0.0.1"


async def test():
    await asyncio.wait([run_server(), run_client('client_1', CLIENT_HOST, CLIENT_PORT)])

async def test2():
    await asyncio.wait([run_server(),
                        run_client('client_1', CLIENT_HOST, CLIENT_PORT),
                        run_client('client_2', CLIENT_HOST, CLIENT_PORT)])

async def test3():
    await asyncio.wait([run_server(),
                        AsyncClient(name='client_1', host=CLIENT_HOST, port=CLIENT_PORT).run_client(CLIENT_HOST, CLIENT_PORT),
                        ])

async def test4():
    await asyncio.wait([run_server()])

async def test5():
    await asyncio.wait([
                        AsyncClient(name='client_1', host=CLIENT_HOST, port=CLIENT_PORT).run_client(CLIENT_HOST, CLIENT_PORT)
                        ])




if __name__ == '__main__':
    # asyncio.run(test())
    asyncio.run(test4())
