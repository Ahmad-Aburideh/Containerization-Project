from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Data Entry Web App Running"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)