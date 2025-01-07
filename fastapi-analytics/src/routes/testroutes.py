import time
from time import perf_counter
import subprocess
from datetime import datetime
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
 
    ts = datetime.now().isoformat()

    start = perf_counter()
    res = _do_cpu_bound()
    end = perf_counter()

    return {
        "message": "f'--------\n Received at: {ts} -- Duration of one iteration",
        "result": end - start,
    }

@router.get(
    "/sync-cpubound/{iterations}",
    tags=["testpoint"],
    summary="get duration in s for one iteration",
    description="returns duration in seconds for n iterations on CPU bound task execution",
)
async def syncronous_api(iterations:int =1):

    ts = datetime.now().isoformat()

    print(f'--------\n Received at: {ts} -- iterations = {iterations} \n -------')
    start = perf_counter()
    for _ in range(iterations):
        _do_cpu_bound()
    end = perf_counter()

    return {
        "message": f"--------\n Received at: {ts} -- Duration of {iterations} iterations",
        "result": end - start,
    }

@router.get(
    "/badasync-cpubound/{iterations}",
    tags=["testpoint"],
    summary="async api hiding a sync call test",
    description="returns duration in seconds for n iterations on CPU bound task execution",
)
async def bad_async(iterations: int=1):

    ts = datetime.now().isoformat()
    print(f'--------\n Received at: {ts} -- iterations = {iterations} \n -------')
    concurrent_tasks = len(asyncio.all_tasks()) + 1 # we add the current task as well
    print('Running concurrently: ', concurrent_tasks)
    
    start = perf_counter()
    # schedule all iterations to run concurrently 
    result = await _bad_async_do_work(iterations)
    end = perf_counter()
    
    return {
        "message": f"At {ts} -- duration for {iterations} iterationss",
        "result": end - start,
        "concurrent_tasks": concurrent_tasks
    }

@router.get(
    "/async-IObound/{iterations}",
    tags=["testpoint"],
    summary="non-blocking task api",
    description="returns duration in seconds for n iterations on CPU bound task execution",
)
async def async_iobound(iterations: int=1):

    ts = datetime.now().isoformat()
    print(f'--------\n Received at: {ts} -- iterations = {iterations} \n -------')
    concurrent_tasks = len(asyncio.all_tasks()) + 1 # we add the current task as well
    print('Running concurrently: ', concurrent_tasks)
    
    start = perf_counter()
    # schedule all iterations to run concurrently 
    result = await _do_io_bound(2) # wait 2 seconds
    end = perf_counter()
    
    return {
        "message": f"At {ts} -- duration for {iterations} iterationss",
        "result": end - start,
        "concurrent_tasks": concurrent_tasks
    }


@router.get(
    "/resmon",
    tags=["monitoring", "resource"],
    summary="resource monitor output",
    description="returns snapshot of current used resources on server",
)
async def resmon_api():

  try:
    resmondata = subprocess.check_output(['top', # command
                                     '-b',   # run as batch, no display
                                     '-n1'   # run for one iteration only -> snapshot of current resources
                                     ], text=True)
    return {
        "message": "Duration of one iteration",
        "result": resmondata,
    }
  except subprocess.CalledProcessError as e:
    print(f"Error executing 'top' command: {e}")
    raise HTTPException(status_code=500, detail=f"Error executing reading server resources : {e}")





#################################

# @router.get(
#     "/trueasynctest/{data}",
#     tags=["testpoint"],
#     summary="async api test",
#     description="reflects back request",
# )
# async def async_test(wait: float):

#     # synchronous call
#     await _true_async_do_work(wait)
    
#     return {
#         "result": "async api test",
#         "message": "Alive",
#         "mirorred": wait,
#     }
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
            executor, _do_cpu_bound
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
def _do_cpu_bound():
    """
    Synchronous/blocking task.
    Here, a matrix multiplication is used to consume actual CPU.
    """
    # time.sleep(2)
    np.square(testmatrix)

    return 'Something'


async def _bad_async_do_work(iterations:int):
    """ Contains sync call and now actual async-await point"""
    # synchronous call in async function -> await 
    for _ in range(iterations):
        _do_cpu_bound()

async def _do_io_bound(wait: float):
    """ Uses non-blocking sleep """
    # synchronous call in async function -> await 
    await asyncio.sleep(wait)
