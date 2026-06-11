import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DATABASE = 'notes.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute(
        '''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        '''
    )
    conn.commit()
    conn.close()


def initialize_database():
    init_db()
initialize_database()

@app.route('/', methods=['GET'])
def index():
    conn = get_db_connection()
    notes = conn.execute('SELECT * FROM notes ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('notes.html', notes=notes)

@app.route('/add', methods=['POST'])
def add_note():
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    if title and content:
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M')
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO notes (title, content, created_at) VALUES (?, ?, ?)',
            (title, content, created_at)
        )
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:note_id>', methods=['GET'])
def delete_note(note_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM notes WHERE id = ?', (note_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0",port=5000,debug=True)
