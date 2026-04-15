import psutil
import requests
import time

API_URL = "http://127.0.0.1:8000/metrics"

while True:
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent

    data = {
        "cpu": cpu,
        "memory": memory
    }

    try:
        response = requests.post(API_URL, json=data)
        print("Sent:", data)
    except Exception as e:
        print("Error:", e)

    time.sleep(5)