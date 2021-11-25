import asyncio
TIMEOUT = 3000
CLOCK = 5

class BaseStream:

    def __init__(self, timeout=TIMEOUT):

        self.timeout = timeout
        # ref main_server
        self.main_stream = None

        if timeout is None:
            self.timeout = TIMEOUT
        else:
            self.timeout = timeout



    def set_main_stream(self, main_stream):
        if main_stream is not None:
            self.main_stream = main_stream

class ComStream(BaseStream):

    '''

    IN_STREAM:: for wrapper class stream for communicate network
    it is dependent to server's writer & reader
    '''

    def __init__(self, reader=None, writer=None, queue=None, *args, **kwargs):
        super(ComStream, self).__init__()


        if reader is None:
            self.reader: asyncio.StreamReader
        else:
            self.reader = reader

        if writer is None:
            self.writer: asyncio.StreamWriter
        else:
            self.writer = writer

        self.queue = queue

        print(f'reader {self.reader}')
        print(f'writer {self.writer}')
        print(f'timeout {self.timeout}')

    async def cancel(self):
        self._task.cancel()

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


        if clock is None:
            self.clock = CLOCK
        else:
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

            if self.main_stream is not None:
                self.main_stream.update_train()

        else:
            print('wait for signal')

    async def copy(self, check):

        await self.copy_callback(check)
        print(f'{self.clock}')
        await asyncio.sleep(self.clock)

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


