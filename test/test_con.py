import asyncio
from server.connect import *
from client.connect import *
_port = 58441

async def test():
    await asyncio.wait([run_server(), run_client("127.0.0.1", _port)])


if __name__ == '__main__':
    asyncio.run(test())