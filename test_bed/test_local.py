import requests
from map import *
import time

def check_finished(task):

    if len(task) == 0:
        return True

    else:
        return False



def asyncio_test(base_engine=requests, base_session=BaseSession , verbose=False, test=False):

    result = []

    a_start = time.time()

    stream = FedStream(reader=BaseReader(base=base_engine, session=base_session))


    for l in range(5):

        stream.scheduler()

    tasks = stream.executor()

    loop = asyncio.get_event_loop()

    finished, unfinished = loop.run_until_complete(
        asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED))

    for task in finished:
        result.append(task.result())

        if verbose:
            print(task.result())

    print("unfinished:", len(unfinished))

    # if not check_finished(unfinished):
    #
    #     finished2, unfinished2 = loop.run_until_complete(
    #         asyncio.wait(unfinished, timeout=2))
    #
    #     for task in finished2:
    #         result.append(task.result())

    loop.close()

    a_end = time.time()

    print(f'asyncio {a_end - a_start:.5f}times')
    print(f'asyncio scrap done')
    print(f"{'+' * 20}")



    return result





if __name__ == '__main__':
    # api for web scraper
    asyncio_test(urls=None, base_engine=requests,
                    base_session=CustomSession,
                    verbose=False, test=False)