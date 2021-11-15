# __all__ = (
#     'StreamReader', 'StreamWriter', 'StreamReaderProtocol',
#     'open_connection', 'start_server')
#
# # it is based on asyncio stream code
# # add & modified steam & wrapper for edge communication
# _DEFAULT_LIMIT = 2 ** 16  # 64 KiB
# import socket
# import sys
# import warnings
# import weakref
# from asyncio import streams
#
# if hasattr(socket, 'AF_UNIX'):
#     __all__ += ('open_unix_connection', 'start_unix_server')
#
# class BaseStream:
#
#     _source_traceback = None
#
#     def __init__(self, limit=_DEFAULT_LIMIT, loop=None):
#
#
#         if limit <= 0:
#             raise ValueError('Limit cannot be <=0')
#         if loop is None:
#             self._loop = ''
#
# class FedStream(streams.StreamReader):
#
#     def __init__(self):
#         super().__init__()
import asyncio
TIMEOUT = 3000


class BaseStream:

    def __init__(self, timeout=TIMEOUT, reader=None, writer=None):
        self.writer = writer
        self.reader = reader
        self.timeout = timeout


class ComStream(BaseStream):

    '''
    IN_STREAM
    '''

    pass


class CopyStream(BaseStream):

    '''
    OUT_STREAM
    '''

    def __init__(self,  callback=None, loop=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if callback is None:
            self._callback = self.copy_callback
        else:
            self._callback = callback

        if loop is None:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        else:
            self.loop = loop



    async def _job(self):

        await self._callback()


    async def cancel(self):
        self._task.cancel()

    async def copy_callback(self):
        print('copy callback')
        await asyncio.sleep(self.timeout)

    async def setup(self):
        self._task = asyncio.ensure_future(self._job())


if __name__ == '__main__':

    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)

    stream = CopyStream(timeout=10, loop=None)
    # IN_stream = CopyStream(timeout=10, loop=None)
    try:
        stream.loop.run_until_complete(stream.setup())
        # loop.run_until_complete(stream.setup())
        print('hi')

    finally:

        stream.loop.run_until_complete(stream.loop.shutdown_asyncgens())
        stream.loop.close()

        # loop.run_until_complete(loop.shutdown_asyncgens())
        # loop.close()

