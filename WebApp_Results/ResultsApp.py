from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import mysql.connector
from pymongo import MongoClient
from urllib.parse import quote_plus

app = Flask(__name__, template_folder='templates')
app.secret_key = os.urandom(24)

#MySQL Connection Configuration**
def get_db_connection():
    try:
        return mysql.connector.connect(
            host='host.docker.internal',
            user='ahmad_qasem',
            password='ahmad@red22',
            database='ahmad2003'
        )
    except mysql.connector.Error as err:
        print(f"Database Connection Error: {err}")
        return None

#  MongoDB Configuration
password = quote_plus("ahmad@2003")  # Encode password safely
mongo_client = MongoClient(f"mongodb://ahmad_qasem:{password}@host.docker.internal:27017/")
mongo_db = mongo_client["analytics_db"]
statistics_collection = mongo_db["statistics"]

@app.route('/')
def home():
    return redirect(url_for('results_login'))  # Redirect to login page

#Use MySQL Authentication for WebApp_Results
@app.route('/results-login', methods=['GET', 'POST'])
def results_login():
    error = None  # Default: No error

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        print(f"🔹 Login Request: Username = {username}, Password = {password}")

        conn = get_db_connection()
        if not conn:
            return "Database connection failed."

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM AuthUsers WHERE username = %s", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and user['password'] == password:
            print("Authentication Successful!")
            session['user_id'] = user['id']  # Store user session
            return redirect(url_for('dashboard'))  # Redirect to dashboard
        else:
            print("Invalid credentials!")
            error = "Invalid credentials, please try again."  # Error message

    return render_template("results_login.html", error=error)  # Pass error to template



@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('results_login'))  # Ensure user is authenticated

    return render_template("stats_dashboard.html")  # Show the dashboard page

#/get-stats route to get Statistics
@app.route('/get-stats', methods=['GET'])
def get_stats():
    try:
        # Fetch the latest Statistics from MongoDB
        latest_stats = statistics_collection.find().sort("_id", -1).limit(1)
        stats_list = []
        for stat in latest_stats:
            stats_list.append({
                "_id": str(stat["_id"]),  # Convert ObjectId to string
                "max": stat.get("max"),
                "min": stat.get("min"),
                "average": stat.get("average")
            })

        if not stats_list:
            return jsonify({"error": "No statistics found"}), 404

        return jsonify({"statistics": stats_list})  # Return Statistics as JSON

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
