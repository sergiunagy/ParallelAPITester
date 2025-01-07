import time
from time import perf_counter
import subprocess

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

@app.route("/test/resmon", methods=["GET"], strict_slashes=False)
def resmon_api():
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
    return {
        "message": "Error executing reading server resources : {e}",
    }, 500

 
def _do_cpu_bound():

    np.square(testmatrix)

    return 'Something'
