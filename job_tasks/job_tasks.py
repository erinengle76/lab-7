import os
from celery import Celery
import requests
import time

broker_url = os.environ.get("CELERY_BROKER_URL")
res_backend = os.environ.get("CELERY_RESULT_BACKEND")

celery_app = Celery(name='job_tasks', 
                    broker=broker_url, 
                    result_backend=res_backend)

@celery_app.task
def countInput(inputString):
    try:
        r = inputString
        # MAY NEED TO LOOK AT REMOVING PUNCTUATION
        input = r.strip()
        noWords = int(len(input.split()))
        time.sleep(noWords)
        # this is just a number? need to be a json?
        return noWords
    except Exception as e:
        print(e)
        return str(e)
