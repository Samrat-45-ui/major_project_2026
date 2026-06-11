from flask import Flask, jsonify, request, send_from_directory
import sqlite3
import os

app = Flask(__name__)

DB_PATH = 'gym.db'
SQL_PATH = 'data.sql'

def init_db():
    if os.path.exists(DB_PATH):
        return

    conn = sqlite3.connect(DB_PATH)
    with open(SQL_PATH, 'r', encoding='utf-8') as sql_file:
        conn.executescript(sql_file.read())
    conn.commit()
    conn.close()


def connect_db():
    init_db()
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON;")
    return db

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/bookings')
def bookings_page():
    return send_from_directory('.', 'bookings.html')

@app.route('/contact')
def contact_page():
    return send_from_directory('.', 'contact.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

# API endpoint to return classes from the database
@app.route('/api/classes', methods=['GET'])
def list_classes():
    try:
        db = connect_db()
        class_rows = db.execute('SELECT * FROM classes').fetchall()
        db.close()
        
        class_list = []
        for class_row in class_rows:
            class_list.append({
                'id': class_row['class_id'],
                'name': class_row['class_name'],
                'instructor': class_row['instructor'],
                'time': class_row['time_slot'],
                'spots': class_row['spots_remaining']
            })
        return jsonify(class_list), 200
    except Exception as error:
        return jsonify({'error': str(error)}), 500

# API to process incoming form data and save to database
@app.route('/api/book', methods=['POST'])
def create_booking():
    data = request.get_json()
    if not data or 'username' not in data or 'class_id' not in data:
        return jsonify({'error': 'Missing data'}), 400
    
    username = str(data['username']).strip()
    class_id = int(data['class_id'])

    conn = connect_db()
    cursor = conn.cursor()

    try:
        # Get or create user wrapper record
        cursor.execute('SELECT user_id FROM users WHERE username = ?', (username,))
        user_row = cursor.fetchone()
        if user_row:
            user_id = user_row['user_id']
        else:
            cursor.execute('INSERT INTO users (username, email) VALUES (?, ?)', (username, f"{username}@gym.com"))
            user_id = cursor.lastrowid

        # Check seat parameters
        cursor.execute('SELECT spots_remaining FROM classes WHERE class_id = ?', (class_id,))
        class_row = cursor.fetchone()
        if not class_row:
            return jsonify({'error': 'Class not found'}), 404
        if class_row['spots_remaining'] <= 0:
            return jsonify({'error': 'Class is full'}), 409

        # Process transactional update
        cursor.execute('INSERT INTO bookings (user_id, class_id) VALUES (?, ?)', (user_id, class_id))
        cursor.execute('UPDATE classes SET spots_remaining = spots_remaining - 1 WHERE class_id = ?', (class_id,))
        conn.commit()
        return jsonify({'success': 'Spot secured!'}), 201

    except sqlite3.Error as e:
        conn.rollback()
        return jsonify({'error': 'Database transaction error', 'details': str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)