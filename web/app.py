import os
from flask import Flask, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def check_db_connection():
    try:
        conn = mysql.connector.connect(
            host='db-svc',
            user='dbuser',
            password='dbpass',
            database='sampledb',
            connection_timeout=5
        )
        if conn.is_connected():
            conn.close()
            return True
    except Error as e:
        print("Connection error:", e)
    return False

@app.route('/status')
def status():
    connected = check_db_connection()
    status_msg = "Connected to DB" if connected else "DB Disconnected !"
    return jsonify({"status": status_msg})

@app.route('/')
def home():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>DB Connection Status</title>
        <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color: #f0f0f0;
            }
            .container {
                text-align: center;
                font-size: 2em;
                padding: 20px;
                border: 2px solid #ccc;
                border-radius: 10px;
                background-color: #fff;
            }
        </style>
    </head>
    <body>
        <div class="container" id="status">Checking DB Connection...</div>
        <script>
            async function fetchStatus() {
                try {
                    const response = await fetch('/status');
                    const data = await response.json();
                    const statusDiv = document.getElementById('status');
                    statusDiv.innerText = data.status;
                    if (data.status === "Connected to DB") {
                        statusDiv.style.color = "green";
                    } else {
                        statusDiv.style.color = "red";
                    }
                } catch (error) {
                    const statusDiv = document.getElementById('status');
                    statusDiv.innerText = 'Error fetching status';
                    statusDiv.style.color = "red";
                }
            }
            fetchStatus();
            setInterval(fetchStatus, 5000); // Poll every 5 seconds
        </script>
    </body>
    </html>
    """
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
