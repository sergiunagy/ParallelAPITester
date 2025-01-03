# ############################
# gunicorn_config.py
# ----------------
# Configuration file for the gunicorn App-Server
# - server config : command line arguments
# - server hooks : set up hooks for debugging and information extraction
# # ##################################################################

##################################################################
# ######### Server config - https://docs.gunicorn.org/en/stable/settings.html
import os
# watching for requests coming over this address:port
bind = os.getenv('GUNICORN_EXPOSED_ON', default='0.0.0.0:5000') #'0.0.0.0:5000'

# number of poor bastards doing work
workers= 5 # assume 2x Cores CPU

# Give workers no time to rest >:D - timeout threshold at 0s 
timeout = 0

# watchdog file maps by default to hdd so remap to RAM virtual folder
# gunicorn optimization for docker: https://pythonspeed.com/articles/gunicorn-in-docker/
worker_tmp_dir= "/dev/shm"

# configure log files location for the application server
accesslog='logs/gunicorn.access.log'
errorlog='logs/gunicorn.error.log'

# communication is the key
loglevel = 'info' # 'info', 'warning', 'error', 'critical'

# reload for code changes - disable on prod
reload = True

##################################################################
# ######### Server hooks https://docs.gunicorn.org/en/stable/settings.html?highlight=hooks#server-hooks


def on_starting(server):
    """
    Do something on server start
    """
    print(" Gunicorn: Startin' server with {} workers".format(workers) )


def on_reload(server):
    """
     Do something on reload
    """
    print("=========Server has reloaded")


def post_worker_init(worker):
    """
    Do something on worker initialization
    """
    print("============Worker has been initialized. Worker Process id –>", worker.pid)

def worker_exit(server, worker):
    
    print ('worker {} is tired of your shit. Going home..'.format(worker.pid))

def pre_request(worker, req):
    
    print('Worker {} received request:{} - {}'.format(worker.pid, req.method, req.path))