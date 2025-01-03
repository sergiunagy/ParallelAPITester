import time
from time import perf_counter

from flask import Flask, request, jsonify
# CORS library
from flask_cors import CORS

import numpy as np

app = Flask(__name__)
CORS(app)

# generate a test matrix. Random but with seed so we can reproduce results
np.random.seed(42)
testmatrix = np.random.rand(5000,5000)

# ################# PUBLIC ROUTINES  #########################
@app.route('/test/calibrate', methods=["GET"], strict_slashes=False)
def calibration_api():

    start = perf_counter()
    res = _do_cpu_bound()
    end = perf_counter()

    return {
        "message": "Duration of one iteration",
        "result": end - start,
    }


@app.route('/test/sync-cpubound/<iterations>', methods=["GET"], strict_slashes=False)
def syncronous_api(iterations:str):

    print('Received: ', iterations)
    start = perf_counter()
    for _ in range(int(iterations)):
        _do_cpu_bound()
    end = perf_counter()

    return {
        "message": f"Duration of {iterations} iterations",
        "result": end - start,
    }

 
def _do_cpu_bound():

    np.square(testmatrix)

    return 'Something'
