import urllib.request
import json

base_url = "http://127.0.0.1:5001/predict"

tests = [
    {
        "name": "Low Engagement",
        "payload": {"pages_viewed": 1, "time_spent": 1, "cart_additions": 0, "previous_purchases": 0, "total_sessions": 1, "session_duration": 10, "product_category": "Books", "device_type": "Mobile", "traffic_source": "Social Media"}
    },
    {
        "name": "Medium Engagement",
        "payload": {"pages_viewed": 5, "time_spent": 15, "cart_additions": 2, "previous_purchases": 1, "total_sessions": 8, "session_duration": 12, "product_category": "Electronics", "device_type": "Mobile", "traffic_source": "Referral"}
    },
    {
        "name": "High Engagement",
        "payload": {"pages_viewed": 10, "time_spent": 200, "cart_additions": 5, "previous_purchases": 3, "total_sessions": 10, "session_duration": 300, "product_category": "Sports", "device_type": "Mobile", "traffic_source": "Ads"}
    }
]

for test in tests:
    print(f"Testing {test['name']}...")
    req = urllib.request.Request(base_url, data=json.dumps(test['payload']).encode(), headers={'Content-Type': 'application/json'})
    try:
        response = urllib.request.urlopen(req)
        print(response.read().decode())
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 50)
