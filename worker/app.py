import os

from celery.app import Celery
from datetime import datetime
import pandas as pd
import json





redis_url = "redis://:123456@localhost:6379"

celery_app = Celery(__name__, broker=redis_url, backend=redis_url)


@celery_app.task()
def add(a, b):
    for i in range(a,b):
        print(i)
    return {"number":a+b}


@celery_app.task()
def process_ask(prompt, template, json_str, times, length):
    print(f"get ask")
    print(template)
    data = json.loads(json_str)
    df = pd.DataFrame(data)
    return {"ask": json_str}


