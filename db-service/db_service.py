from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DB_FILE = "logs.db"

def init_db():
    """Initialize the database."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

@app.route('/log', methods=['POST'])
def add_log():
    data = request.json
    action = data.get('action')
    timestamp = data.get('timestamp')

    with sqlite3.connect('logs.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO logs (action, timestamp) VALUES (?, ?)', (action, timestamp))
        conn.commit()

    return jsonify({"message": "Log added successfully"}), 201

@app.route('/logs', methods=['POST'])
def log_action():
    data = request.get_json()
    action = data.get("action", "UNKNOWN")
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO logs (action) VALUES (?)', (action,))
        conn.commit()
    return jsonify({"status": "success"}), 201

@app.route('/logs', methods=['GET'])
def get_logs():
    with sqlite3.connect('logs.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT action, timestamp FROM logs ORDER BY id DESC')
        logs = [{"action": row[0], "timestamp": row[1]} for row in cursor.fetchall()]

    return jsonify(logs)

@app.route('/reset', methods=['POST'])
def reset_logs():
    with sqlite3.connect('logs.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM logs')
        conn.commit()
    return jsonify({"status": "success", "message": "Logs have been reset."}), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5001)