import time
import requests

BASE_URL = "YOUR_IP_HERE:PORT/5000"

session = requests.Session()

def request_endpoint(path, method="get", data=None):
    url = f"{BASE_URL}{path}"
    start = time.time()
    response = session.request(method=method, url=url, data=data)
    end = time.time()
    print(f"Request to {url:<50} | Status: {response.status_code:<3}  | start: {start:<20.6f} | end: {end:<20.6f}")
    return {"endpoint": path, "response": response.status_code, "start": start, "end": end,
            "delta": end - start}