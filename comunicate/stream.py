__all__ = (
    'StreamReader', 'StreamWriter', 'StreamReaderProtocol',
    'open_connection', 'start_server')

# it is based on asyncio stream code
# add & modified steam & wrapper for edge communication
_DEFAULT_LIMIT = 2 ** 16  # 64 KiB
import socket
import sys
import warnings
import weakref

if hasattr(socket, 'AF_UNIX'):
    __all__ += ('open_unix_connection', 'start_unix_server')

class BaseStream:

    _source_traceback = None

    def __init__(self, limit=_DEFAULT_LIMIT, loop=None):


        if limit <= 0:
            raise  ValueError('Limit cannot be <=0')
        if loop is None:
            self._loop = ''
