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
        FedServer(name='server', opt=OPT, user_num=1).run()
    ])

async def wrapper_for_run():

    await asyncio.wait([run_pipe()])

if __name__ == '__main__':

    # asyncio.run(wrapper_for_run())
    asyncio.run(fedrun())
