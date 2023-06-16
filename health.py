import os
from time import time
from pathlib import Path
from flask import make_response
from config import HEALTH_CHECK_FAIL_THRESHOLD_SECONDS

health_file = "healthcheck.txt"

def health_update():
    Path(health_file).touch()
    #health_time = os.path.getmtime(health_file)
    #print(f'Health Update: {health_time}')


def health_check():
    timenow = time()
    health_time = os.path.getmtime(health_file)
    delta = abs(health_time - timenow)
    if( delta < HEALTH_CHECK_FAIL_THRESHOLD_SECONDS):
        return f'{delta}'
    else:
        return make_response(f"Last report: {health_time}, delta: {delta}", 500)

