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
CLOCK = 3000

class BaseStream:

    def __init__(self, timeout=TIMEOUT, reader=None, writer=None):

        if reader is None:
            self.writer: asyncio.StreamWriter
        if writer is None:
            self.reader: asyncio.StreamReader
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

    def __init__(self,  callback=None, loop=None, clock=CLOCK, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if callback is None:
            self._callback = self.copy_callback
        else:
            self._callback = callback

        self.clock = clock

        if loop is None:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        else:
            self.loop = loop

    async def _job(self, check):

        await self._callback(check)

    async def cancel(self):
        self._task.cancel()

    async def copy_callback(self, check):

        print(f'call back check'
              f' status: {check}')

        if check:
            print('copy callback')


        else:
            print('wait for signal')

    async def copy(self, check):

        await asyncio.sleep(self.clock)
        await self.copy_callback(check)

    async def copy_root(self):
        while True:
            await asyncio.sleep(self.clock)
            self._task = asyncio.ensure_future(self._job(True))



if __name__ == '__main__':

    in_stream = CopyStream(timeout=10, loop=None, clock=5)
    out_stream = CopyStream(timeout=10, loop=None)


    try:
        in_stream.loop.run_until_complete(in_stream.copy())

        print('hi')

    finally:

        in_stream.loop.run_until_complete(in_stream.loop.shutdown_asyncgens())
        in_stream.loop.close()


