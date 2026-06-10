from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('gym.db')
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/bookings')
def bookings_page():
    return render_template('bookings.html')

@app.route('/contact')
def contact_page():
    return render_template('contact.html')

@app.route('/api/classes', methods=['get'])
def get_classes():
    try:
        conn = 
        except Exception as e:
    
          
     



