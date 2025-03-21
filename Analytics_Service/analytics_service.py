from flask import Flask, jsonify, render_template
import mysql.connector
from pymongo import MongoClient
from urllib.parse import quote_plus
import json
from bson import ObjectId  # To handle MongoDB ObjectId serialization

app = Flask(__name__)

# MySQL 
mysql_config = {
    'host': 'host.docker.internal',
    'user': 'ahmad_qasem',
    'password': 'ahmad@red22',
    'database': 'ahmad2003'
}

# MongoDB Configuration
password = quote_plus("ahmad@2003")  # Encode the password
mongo_client = MongoClient(f"mongodb://ahmad_qasem:{password}@host.docker.internal:27017/")
mongo_db = mongo_client["analytics_db"]
statistics_collection = mongo_db["statistics"]

# Ensure ObjectId is serializable
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)  # Convert ObjectId to string
        return super().default(obj)

app.json_encoder = JSONEncoder

@app.route('/')
def home():
    return render_template('compute_stats.html')

@app.route('/compute-stats', methods=['GET'])
def compute_stats():
    try:
        # Connect to MySQL
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)

        # Fetch numeric values from requests table
        cursor.execute("SELECT numeric_value FROM requests WHERE numeric_value IS NOT NULL")
        values = [row["numeric_value"] for row in cursor.fetchall()]
        
        if not values:
            return jsonify({"error": "No numeric data found"}), 400

        max_value = max(values)
        min_value = min(values)
        avg_value = sum(values) / len(values)

        # Store statistics in MongoDB
        stats = {
            "max": max_value,
            "min": min_value,
            "average": avg_value
        }
        inserted_stat = statistics_collection.insert_one(stats)

        # Convert `_id` (ObjectId) to string before returning response
        stats["_id"] = str(inserted_stat.inserted_id)

        return jsonify({"message": "Statistics computed and stored!", "data": stats})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-stats', methods=['GET'])
def get_stats():
    try:
        latest_stats = statistics_collection.find().sort("_id", -1).limit(1)
        stats_list = [{**doc, "_id": str(doc["_id"])} for doc in latest_stats]

        return jsonify({"statistics": stats_list})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stats-dashboard')
def stats_dashboard():
    return render_template('stats_dashboard.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
