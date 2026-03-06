import urllib.request
import urllib.error
import urllib.parse
import json

url = "http://127.0.0.1:5001/predict"
payload = {
    "pages_viewed": 10.0,
    "time_spent": 15.0,
    "cart_additions": 3.0,
    "previous_purchases": 5.0,
    "total_sessions": 25.0,
    "session_duration": 40.0,
    "product_category": 3.0,
    "device_type": 1.0,
    "traffic_source": 4.0
}
data = json.dumps(payload).encode('utf-8')

req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode())
        print("Status:", response.status)
        print("Response:", result)
except urllib.error.HTTPError as e:
    print("Error:", e.code)
    print("Reason:", e.read().decode())
