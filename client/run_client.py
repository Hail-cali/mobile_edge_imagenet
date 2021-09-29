#run_client

import asyncio
from opt import parse_opts
from client import *

OPT = parse_opts()

# CLIENT_PORT = 8080
# CLIENT_HOST = "127.0.0.1"

async def single(model):

    await asyncio.wait([
                        AsyncClient(name='client_3', host=OPT.CLIENT_HOST, port=OPT.CLIENT_PORT
                                    ).run_client_model(OPT.CLIENT_HOST, OPT.CLIENT_PORT, OPT, model),

                        ])


async def multi_client():
    await asyncio.wait([
        AsyncClient(name='client_1', host=OPT.CLIENT_HOST, port=OPT.CLIENT_PORT
                    ).run_client_model(OPT.CLIENT_HOST, OPT.CLIENT_PORT, OPT, model),
        AsyncClient(name='client_2', host=OPT.CLIENT_HOST, port=OPT.CLIENT_PORT
                    ).run_client_model(OPT.CLIENT_HOST, OPT.CLIENT_PORT, OPT, model)
                        ])


if __name__ == '__main__':

    model = load_model(OPT)

    asyncio.run(single(model))

