import joblib
import numpy as np

MODEL_PATH = "model/purchase_pipeline.pkl"
pipeline = joblib.load(MODEL_PATH)

features = np.array([[1.0, 1.0, 0.0, 0.0, 1.0, 10.0, 1.0, 1.0, 1.0]])
probability_ratio = float(pipeline.predict_proba(features)[0][1])
print(f"Test probability: {probability_ratio}")
