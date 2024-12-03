from flask import Flask, render_template, request, redirect, url_for
import time

app = Flask(__name__)

# Hardcoded credentials
correct_username = "adithyan112"
correct_password = "123456"

# Variable to track failed attempts
failed_attempts = []

# Function to detect anomalous login attempts
def detect_anomaly():
    global failed_attempts
    current_time = time.time()
    # Remove failed attempts older than 1 minute
    failed_attempts = [t for t in failed_attempts if current_time - t < 60]
    if len(failed_attempts) > 3:  # 3 failed attempts in the last 60 seconds
        return True
    return False

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    global failed_attempts

    username = request.form['username']
    password = request.form['password']

    # Check credentials
    if username == correct_username and password == correct_password:
        failed_attempts.clear()  # Clear the failed attempts list on successful login
        return render_template('welcome.html')
    else:
        failed_attempts.append(time.time())
        if detect_anomaly():
            return "Anomalous activity detected. Too many failed attempts."
        return "Incorrect username or password. Please try again."

if __name__ == '__main__':
    app.run(debug=True)
