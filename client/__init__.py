import os
import sys
WORKING_DIR_AND_PYTHON_PATHS = os.path.join('/', *os.getcwd().split("/")[:-1])
# print(f'before {sys.path}')
sys.path.append(WORKING_DIR_AND_PYTHON_PATHS)
# print(f'after {sys.path}')


from utils.make_plot import history_plot
from client.connect import *

# check
print(f'here client init file passsed')
