import os
# Fix PyInstaller / multiprocessing C-extension threading conflicts on Windows
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

import sqlite3
import joblib
import numpy as np
from flask import Flask, render_template, request, jsonify, g
from datetime import datetime

app = Flask(__name__)
app.config['DATABASE'] = 'database.db'
app.config['UPLOAD_FOLDER'] = 'uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

MODEL_PATH = "model/purchase_pipeline (1).pkl"
print("Loading ML pipeline...")

if os.path.exists(MODEL_PATH):
    pipeline = joblib.load(MODEL_PATH)
    print("Pipeline loaded successfully")
else:
    pipeline = None
    print("ERROR: Pipeline file not found")

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pages_viewed REAL,
                time_spent REAL,
                cart_additions REAL,
                previous_purchases REAL,
                probability REAL,
                recommendation TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS datasets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dataset_name TEXT,
                upload_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                file_path TEXT
            )
        ''')
        db.commit()

# Ensure database is initialized during startup
init_db()

def get_recommendation(prob):
    if prob > 0.8:
        return "Show product immediately"
    elif prob >= 0.5:
        return "Offer discount"
    else:
        return "Recommend similar products"

@app.route("/")
def index():
    return render_template("index.html")

from threading import Lock
predict_lock = Lock()

@app.route("/predict", methods=["POST"])
def predict():
    if pipeline is None:
        return jsonify({"error": "ML model not loaded"}), 500

    try:
        data = request.json
        if not data:
            data = request.form
            
        try:
            pages_viewed = float(data.get("pages_viewed", 0))
            items_viewed = float(data.get("items_viewed", 0))
            time_spent = float(data.get("time_spent", 0))
            cart_additions = float(data.get("cart_additions", 0))
            previous_purchases = float(data.get("previous_purchases", 0))
            session_duration = float(data.get("session_duration", 0))
        except ValueError:
            return jsonify({"error": "Invalid inputs. Must provide numbers.", "success": False}), 400
        
        # Categorical String Handling Using Dictionaries Match to Scikit Config
        encoders = {
            'product_category': {'Clothing': 0.0, 'Books': 1.0, 'Sports': 2.0, 'Electronics': 3.0, 'Home': 4.0, 'Beauty': 5.0},
            'device_type': {'Tablet': 0.0, 'Mobile': 1.0, 'Desktop': 2.0},
            'traffic_source': {'Email': 0.0, 'Social Media': 1.0, 'Organic': 2.0, 'Ads': 3.0, 'Referral': 4.0}
        }
        
        product_category_raw = data.get("product_category", "Clothing")
        device_type_raw = data.get("device_type", "Desktop")
        traffic_source_raw = data.get("traffic_source", "Organic")

        product_category = encoders['product_category'].get(product_category_raw, 0.0)
        device_type = encoders['device_type'].get(device_type_raw, 0.0)
        traffic_source = encoders['traffic_source'].get(traffic_source_raw, 0.0)

        # Raw shape matching all 9 variables properly
        features = np.array([[
            pages_viewed, items_viewed, time_spent, cart_additions, previous_purchases,
            session_duration, product_category, device_type, traffic_source
        ]])
        
        # Output prediction probability using the pipeline
        probability_ratio = float(pipeline.predict_proba(features)[0][1])
            
        recommendation = get_recommendation(probability_ratio)
        
        print("Input features:", features.tolist())
        print("Prediction probability:", probability_ratio)
        
        # Format the output percentage for the database AND JSON output
        probability = round(probability_ratio * 100.0, 2)
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO predictions (pages_viewed, time_spent, cart_additions, previous_purchases, probability, recommendation)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (pages_viewed, time_spent, cart_additions, previous_purchases, probability, recommendation))
        db.commit()
        
        return jsonify({
            "probability": probability,
            "recommendation": recommendation,
            "success": True
        })
    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 400

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/upload-dataset", methods=["GET", "POST"])
def upload_dataset():
    if request.method == "POST":
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        if file and file.filename.endswith('.csv'):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            
            db = get_db()
            cursor = db.cursor()
            cursor.execute('INSERT INTO datasets (dataset_name, file_path) VALUES (?, ?)', (file.filename, file_path))
            db.commit()
            return jsonify({"success": True, "message": "Dataset uploaded successfully!"})
        return jsonify({"error": "Invalid file type, CSV expected."}), 400
    
    return render_template("upload.html")

@app.route("/history")
def history():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM predictions ORDER BY timestamp DESC LIMIT 50')
    predictions = cursor.fetchall()
    return render_template("history.html", predictions=predictions)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, debug=False, threaded=False)
