from flask import Flask, request, render_template, redirect, url_for, session
import mysql.connector
import os

app = Flask(__name__, template_folder='AuthTemplates')  # AuthTemplates for login.html
app.secret_key = os.urandom(24)

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

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None  # Initialize error message as None

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_db_connection()
        if not conn:
            error = "Database connection failed."
            return render_template("login.html", error=error)

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM AuthUsers WHERE username = %s", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and user['password'] == password:
            session['user_id'] = user['id']
            return redirect("http://192.168.100.9:5002")  # Successful Login
        else:
            error = "Invalid credentials! Please try again."  #Set error message

    return render_template("login.html", error=error)  # Pass error message to HTML


@app.route('/dashboard')  #Correct route name
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Ensure user is authenticated
    
    return redirect("http://127.0.0.1:5002/")  # Redirect to DataEntry web app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)