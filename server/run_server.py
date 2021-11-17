import asyncio
import os
import sys
WORKING_DIR_AND_PYTHON_PATHS = os.path.join('/', *os.getcwd().split("/")[:-1])
# print(f' before {sys.path}')
sys.path.append(WORKING_DIR_AND_PYTHON_PATHS)
# print(f' after {sys.path}')

from opt import parse_opts
from server.connect import *

OPT = parse_opts()


async def new():

    # if stream is None, baseline class generated inside class so do loop (Coroutine)
    server = MultiHeadServer(name='server', opt=OPT, com_stream=None, copy_stream=None)

    server.out_stream.set_main_stream(server)

    await asyncio.wait([server.run(), server.copy_call()])


async def fed_run():

    await asyncio.wait([
        FedServer(name='server', opt=OPT).run()
    ])


async def wrapper_for_single_run():

    await asyncio.wait([old_run()])




if __name__ == '__main__':

    # # old version for wrapper
    # asyncio.run(wrapper_for_single_run())
    # # old version for server
    # asyncio.run(fed_run())

    # # server & (copy stream, com stream)
    asyncio.run(new())