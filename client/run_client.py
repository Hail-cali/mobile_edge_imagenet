#run_client

import os
import sys
WORKING_DIR_AND_PYTHON_PATHS = os.path.join('/', *os.getcwd().split("/")[:-1])
# print(f'before {sys.path}')
sys.path.append(WORKING_DIR_AND_PYTHON_PATHS)

from opt import parse_opts
from client import *
from utils.data_loader import CustomDataset

OPT = parse_opts()


async def multi_fed(model):
    await asyncio.wait([
        FedClient(name='client_5', host=OPT.CLIENT_HOST, port=OPT.CLIENT_PORT, data=2
                  ).run_client_model(OPT.CLIENT_HOST, OPT.CLIENT_PORT, OPT, model),
        FedClient(name='client_6', host=OPT.CLIENT_HOST, port=OPT.CLIENT_PORT, data=3
                  ).run_client_model(OPT.CLIENT_HOST, OPT.CLIENT_PORT, OPT, model),

    ])


async def learning(model, dataset):
    await asyncio.wait([
        CustomClient(name='client_10', host=OPT.CLIENT_HOST, port=OPT.CLIENT_PORT
                     ).run_client_model(OPT.CLIENT_HOST, OPT.CLIENT_PORT, OPT, model, dataset),


    ])


if __name__ == '__main__':

    data_path = '/home/edge/data/00100.csv'

    model = load_model(OPT)
    dataset = CustomDataset(data_path)

    asyncio.run(learning(model, dataset))




