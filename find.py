import joblib

model = joblib.load("model/purchase_pipeline.pkl")

print(model)