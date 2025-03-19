from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__, template_folder='templates')  # Update this line to point to the correct folder

# MySQL connection
db_config = {
    'host': 'host.docker.internal',  
    'user': 'ahmad_qasem',
    'password': 'ahmad@red22',
    'database': 'ahmad2003'
}

@app.route('/', methods=['GET', 'POST'])
def data_entry():
    if request.method == 'POST':
        message = request.form.get('message')
        numeric_value = request.form.get('numeric_value')

        # Convert numeric_value to an integer (to avoid errors)
        try:
            numeric_value = int(numeric_value)
        except ValueError:
            return "Invalid number entered. Please enter a valid integer."

        # Connect to MySQL and insert data
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO requests (message, numeric_value) VALUES (%s, %s)", (message, numeric_value))
        conn.commit()
        cursor.close()
        conn.close()

        return "Data inserted successfully!"
    
    return render_template('data_entry_form.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)
