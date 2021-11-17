#run_client

import os
import sys
WORKING_DIR_AND_PYTHON_PATHS = os.path.join('/', *os.getcwd().split("/")[:-1])
# print(f'before {sys.path}')
sys.path.append(WORKING_DIR_AND_PYTHON_PATHS)

import asyncio
from opt import parse_opts
from client import *

OPT = parse_opts()

OPT.CLIENT_PORT = 10022
# CLIENT_HOST = "127.0.0.1"

async def single(model):

    await asyncio.wait([
                        AsyncClient(name='client_3', host=OPT.CLIENT_HOST, port=OPT.CLIENT_PORT, data=3
                                    ).run_client_model(OPT.CLIENT_HOST, OPT.CLIENT_PORT, OPT, model),

                        ])


async def multi_client(model):
    await asyncio.wait([
        AsyncClient(name='client_1', host=OPT.CLIENT_HOST, port=OPT.CLIENT_PORT, data=2
                    ).run_client_model(OPT.CLIENT_HOST, OPT.CLIENT_PORT, OPT, model),

        AsyncClient(name='client_2', host=OPT.CLIENT_HOST, port=OPT.CLIENT_PORT, data=2
                    ).run_client_model(OPT.CLIENT_HOST, OPT.CLIENT_PORT, OPT, model)
                        ])

async def new(model):

    await asyncio.wait([
                        FedClient(name='client_3', host=OPT.CLIENT_HOST, port=OPT.CLIENT_PORT, data=3
                                    ).run_client_model(OPT.CLIENT_HOST, OPT.CLIENT_PORT, OPT, model),

                        ])

if __name__ == '__main__':

    model = load_model(OPT)

    # asyncio.run(single(model))
    # asyncio.run(multi_client(model))

    asyncio.run(new(model))
