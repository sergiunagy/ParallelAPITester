# Script for testing outside jupyter

from time import perf_counter
from datetime import datetime
import asyncio
import httpx

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

URL_CPU = "http://fastapianalytics:5000/test/sync-cpubound/50"
URL_IO = "http://fastapianalytics:5000/test/async-IObound/50"

n = 20

def fetch_all():
    async def innfetch():
        async with httpx.AsyncClient(limits=httpx.Limits(max_connections=None)) as client:
            resp  = await client.get(URL_IO, timeout= 300)
        
        return resp.json()

    return innfetch

async def fetch():
    async with httpx.AsyncClient(limits=httpx.Limits(max_connections=None)) as client:
        requests = [client.get(URL_IO, timeout= 300) for _ in range(n)]
        results = await asyncio.gather(*requests)
    
    print(*[r.json() for r in results], sep='\n')
    return [r.json() for r in results]

async def fetch_b():
    await asyncio.sleep(2)

async def fetch_with_thread_pool():
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=100) as executor:
        requests = [loop.run_in_executor(executor, lambda: httpx.get(URL_CPU, timeout= 300)) for _ in range(n)]
        responses = await asyncio.gather(*requests)

    print(*[r.json() for r in responses], sep='\n')
    return responses

async def fetch_with_process_pool():
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor(max_workers=4) as executor:
        requests = [loop.run_in_executor(executor, fetch_all) for _ in range(n)]
        responses = await asyncio.gather(*requests)

    # print(*[r.json() for r in responses], sep='\n')
    return responses

if __name__ == '__main__':
    start = perf_counter()
    # asyncio.run(fetch())
    asyncio.run(fetch_with_process_pool())
    end = perf_counter()

    print(end-start)


