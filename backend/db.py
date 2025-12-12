# db.py - Database operations for InsightLoop.AI

import sqlite3
import json
from datetime import datetime

DB_FILE = 'insightloop.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY,
        query TEXT,
        insights TEXT,
        links TEXT,
        extracted TEXT,
        comparison_table TEXT,
        timestamp TEXT
    )''')
    conn.commit()
    conn.close()

def save_report(query, insights, links, extracted, comparison_table, rating=0):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''INSERT INTO reports (query, insights, links, extracted, comparison_table, timestamp)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (query, insights, json.dumps(links), json.dumps(extracted), comparison_table, datetime.now().isoformat()))
    report_id = c.lastrowid
    if rating > 0:
        c.execute('''UPDATE reports SET rating = ? WHERE id = ?''', (rating, report_id))
    conn.commit()
    conn.close()
    return report_id

def update_rating(report_id, rating):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''UPDATE reports SET rating = ? WHERE id = ?''', (rating, report_id))
    conn.commit()
    conn.close()

def get_recent_reports(limit=10, search=""):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    if search:
        c.execute('SELECT query FROM reports WHERE query LIKE ? ORDER BY timestamp DESC LIMIT ?', (f'%{search}%', limit))
    else:
        c.execute('SELECT query FROM reports ORDER BY timestamp DESC LIMIT ?', (limit,))
    rows = c.fetchall()
    conn.close()
    return [row[0] for row in rows]
def get_report_by_query(query):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT insights, links, extracted, comparison_table FROM reports WHERE query = ? ORDER BY timestamp DESC LIMIT 1', (query,))
    row = c.fetchone()
    conn.close()
    if row:
        return {
            'insights': row[0],
            'links': json.loads(row[1]),
            'extracted': json.loads(row[2]),
            'comparison_table': row[3]
        }
    return None

def clear_history():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('DELETE FROM reports')
    conn.commit()
    conn.close()