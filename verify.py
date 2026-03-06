import json
from app import app

tests = [
    {
        "name": "Low Engagement",
        "payload": {
            "pages_viewed": 1, "time_spent": 1, "cart_additions": 0, 
            "previous_purchases": 0, "total_sessions": 1, "session_duration": 10, 
            "product_category": "Books", "device_type": "Mobile", "traffic_source": "Social Media"
        }
    },
    {
        "name": "Medium Engagement",
        "payload": {
            "pages_viewed": 5, "time_spent": 15, "cart_additions": 2, 
            "previous_purchases": 1, "total_sessions": 8, "session_duration": 12, 
            "product_category": "Electronics", "device_type": "Mobile", "traffic_source": "Referral"
        }
    },
    {
        "name": "High Engagement",
        "payload": {
            "pages_viewed": 10, "time_spent": 200, "cart_additions": 5, 
            "previous_purchases": 3, "total_sessions": 10, "session_duration": 300, 
            "product_category": "Sports", "device_type": "Mobile", "traffic_source": "Ads"
        }
    }
]

client = app.test_client()

for test in tests:
    print(f"Testing {test['name']}...")
    response = client.post(
        '/predict',
        data=json.dumps(test['payload']),
        content_type='application/json'
    )
    print("Status:", response.status_code)
    print("Response:", response.get_json())
    print("-" * 50)
