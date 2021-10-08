import asyncio
import os
import sys
WORKING_DIR_AND_PYTHON_PATHS = os.path.join('/', *os.getcwd().split("/")[:-1])
# print(f'before {sys.path}')
sys.path.append(WORKING_DIR_AND_PYTHON_PATHS)
# print(f'after {sys.path}')

from server.connect import *




async def pipe():
    await asyncio.wait([run_pipe()])

if __name__ == '__main__':

    asyncio.run(pipe())
