import time
from time import perf_counter

from fastapi import APIRouter
import asyncio
from concurrent.futures import ProcessPoolExecutor
import numpy as np

router = APIRouter(prefix='/test', tags=['testing APIs'])

# generate a test matrix. Random but with seed so we can reproduce results
np.random.seed(42)
testmatrix = np.random.rand(5000,5000)

# ------ APIs

@router.get(
    "/calibrate",
    tags=["testpoint"],
    summary="get duration in s for one iteration",
    description="returns duration in seconds for one iteration on CPU bound task execution",
)
async def calibration_api():

    start = perf_counter()
    res = _do_cpu_bound()
    end = perf_counter()

    return {
        "message": "Duration of one iteration",
        "result": end - start,
    }

def _do_cpu_bound():

    # time.sleep(2)
    np.square(testmatrix)

    return 'Something'

@router.get(
    "/sync-cpubound/{iterations}",
    tags=["testpoint"],
    summary="get duration in s for one iteration",
    description="returns duration in seconds for one iteration on CPU bound task execution",
)
async def syncronous_api(iterations:int =1):

    print('Received: ', iterations)
    start = perf_counter()
    for _ in range(iterations):
        _do_cpu_bound()
    end = perf_counter()

    return {
        "message": f"Duration of {iterations} iterations",
        "result": end - start,
    }


@router.get(
    "/control/{data}",
    tags=["testpoint"],
    summary="control api, mirrors data",
    description="reflects back request",
)
async def control_api(data:str):

   
    return {
        "result": "synchronous api test",
        "message": "Alive",
        "mirorred": data,
    }

@router.get(
    "/synctest/{wait}",
    tags=["testpoint"],
    summary="synchronous call api",
    description="reflects back request",
)
async def sync_api(wait: float):
    # synchronous call
    _sync_do_work(wait)
   
    return {
        "result": "synchronous api test",
        "message": "Alive",
        "mirorred": wait,
    }

@router.get(
    "/badasynctest/{data}",
    tags=["testpoint"],
    summary="async api hiding a sync call test",
    description="reflects back request",
)
async def bad_async(wait: float):

    # async call with CPU bound sub-function
    await _bad_async_do_work(wait)
    
    return {
        "result": " bad async test",
        "message": "Alive",
        "mirorred": wait,
    }

@router.get(
    "/trueasynctest/{data}",
    tags=["testpoint"],
    summary="async api test",
    description="reflects back request",
)
async def async_test(wait: float):

    # synchronous call
    await _true_async_do_work(wait)
    
    return {
        "result": "async api test",
        "message": "Alive",
        "mirorred": wait,
    }
@router.get(
    "/multiproctest/{data}",
    tags=["testpoint"],
    summary="async api test",
    description="reflects back request",
)
async def async_test(wait: float):

    # synchronous call
    with ProcessPoolExecutor() as executor:
        future = asyncio.get_running_loop().run_in_executor(
            executor, _sync_do_work, wait
        )
        await future
    await _true_async_do_work(wait)
    
    return {
        "result": "async api test",
        "message": "Alive",
        "mirorred": wait,
    }

# ---------------------------------
# Private functions
async def _local_fn(param: int):
    pass 

def _sync_do_work(wait: float):
    time.sleep(wait)

async def _bad_async_do_work(wait: float):
    """ Contains sync call and now actual async-await point"""
    # synchronous call in async function -> await 
    time.sleep(wait)

async def _true_async_do_work(wait: float):
    """ Uses non-blocking sleep """
    # synchronous call in async function -> await 
    await asyncio.sleep(wait)
