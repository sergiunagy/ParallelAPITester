# ParallelAPITester
Proof of concept for APIs providing parallel operations

## Overview

The project contains one Tester service and multiple Target Services.  
The initial scope contains:  
- TesterService: Jupyter Notebook implementation of different api functional and performance tests
- FastAPI Analytics: Analytics (CPU bound tasks) service served over FastAPI and Uvicorn
- Flask Analytics: Analytics (CPU bound tasks) service served over Flask and Gunicorn
