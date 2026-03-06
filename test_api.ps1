$headers = @{"Content-Type" = "application/json"}

$body1 = '{"pages_viewed": 1, "time_spent": 1, "cart_additions": 0, "previous_purchases": 0, "total_sessions": 1, "session_duration": 10, "product_category": "Books", "device_type": "Mobile", "traffic_source": "Social Media"}'
Write-Host "--- Low Engagement ---"
Invoke-RestMethod -Uri "http://127.0.0.1:5001/predict" -Method Post -Headers $headers -Body $body1 | ConvertTo-Json

$body2 = '{"pages_viewed": 5, "time_spent": 15, "cart_additions": 2, "previous_purchases": 1, "total_sessions": 8, "session_duration": 12, "product_category": "Electronics", "device_type": "Mobile", "traffic_source": "Referral"}'
Write-Host "--- Medium Engagement ---"
Invoke-RestMethod -Uri "http://127.0.0.1:5001/predict" -Method Post -Headers $headers -Body $body2 | ConvertTo-Json

$body3 = '{"pages_viewed": 10, "time_spent": 200, "cart_additions": 5, "previous_purchases": 3, "total_sessions": 10, "session_duration": 300, "product_category": "Sports", "device_type": "Mobile", "traffic_source": "Ads"}'
Write-Host "--- High Engagement ---"
Invoke-RestMethod -Uri "http://127.0.0.1:5001/predict" -Method Post -Headers $headers -Body $body3 | ConvertTo-Json
