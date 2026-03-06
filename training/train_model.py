import os

# Fix multiprocessing C-extension threading conflicts on Windows
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

import pandas as pd
import numpy as np
import joblib
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

print("Loading dataset...")
df = pd.read_csv("d:/Hackathon/Dataset/customer_activity_dataset.csv")

# Encode categorical variables exactly as app.py does
encoders = {
    'product_category': {'Clothing': 0.0, 'Books': 1.0, 'Sports': 2.0, 'Electronics': 3.0, 'Home': 4.0, 'Beauty': 5.0},
    'device_type': {'Tablet': 0.0, 'Mobile': 1.0, 'Desktop': 2.0},
    'traffic_source': {'Email': 0.0, 'Social Media': 1.0, 'Organic': 2.0, 'Ads': 3.0, 'Referral': 4.0}
}
df.replace(encoders, inplace=True)

# Ensure feature order matches:
features = [
    "pages_viewed", "time_spent", "cart_additions", "previous_purchases",
    "total_sessions", "session_duration", "product_category", "device_type", "traffic_source"
]

X = df[features]
y = df["purchase"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000, class_weight="balanced"))
])

print("Training pipeline...")
pipeline.fit(X_train, y_train)

# Model Validation
print("\n--- MODEL VALIDATION ---")
# Features: pages_viewed, time_spent, cart_additions, previous_purchases, total_sessions, session_duration, product_category, device_type, traffic_source
low_engagement = np.array([[1, 1, 0, 0, 1, 10, 1, 1, 1]])
medium_engagement = np.array([[5, 15, 2, 1, 8, 12, 3, 1, 4]])
high_engagement = np.array([[10, 200, 5, 3, 10, 300, 2, 1, 3]])

prob_low = pipeline.predict_proba(low_engagement)[0][1]
prob_med = pipeline.predict_proba(medium_engagement)[0][1]
prob_high = pipeline.predict_proba(high_engagement)[0][1]

print(f"Low engagement prediction: {prob_low*100:.2f}%")
print(f"Medium engagement prediction: {prob_med*100:.2f}%")
print(f"High engagement prediction: {prob_high*100:.2f}%")
print("------------------------\n")

# Save the Entire Pipeline
os.makedirs("model", exist_ok=True)
joblib.dump(pipeline, "model/purchase_pipeline.pkl")

print("Pipeline saved successfully")
