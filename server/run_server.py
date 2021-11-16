import asyncio
import os
import sys
WORKING_DIR_AND_PYTHON_PATHS = os.path.join('/', *os.getcwd().split("/")[:-1])
# print(f'before {sys.path}')
sys.path.append(WORKING_DIR_AND_PYTHON_PATHS)
# print(f'after {sys.path}')

from opt import parse_opts
from server.connect import *

OPT = parse_opts()



async def fedrun():

    await asyncio.wait([
        FedServer(name='server', opt=OPT).run()
    ])

async def multi_setting():

    await asyncio.wait([
        FedServer(name='server', opt=OPT).run()
    ])

async def wrapper_for_run():

    await asyncio.wait([run_pipe()])

async def new():
    server = MultiHeadServer(name='server', opt=OPT)
    # copy_server = ''
    await asyncio.wait([server.run(), server.copy_call()])


if __name__ == '__main__':

    # asyncio.run(wrapper_for_run())
    # asyncio.run(fedrun())
    # asyncio.run(multi_setting())
    asyncio.run(new())