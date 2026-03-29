from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Connect DB
def get_db():
    conn = sqlite3.connect("contacts.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create table
def create_table():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            email TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db()
    contacts = conn.execute("SELECT * FROM contacts").fetchall()
    conn.close()
    return render_template('index.html', contacts=contacts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']

        conn = get_db()
        conn.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)",
                     (name, phone, email))
        conn.commit()
        conn.close()

        return redirect('/')
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db()
    contact = conn.execute("SELECT * FROM contacts WHERE id=?", (id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']

        conn.execute("UPDATE contacts SET name=?, phone=?, email=? WHERE id=?",
                     (name, phone, email, id))
        conn.commit()
        conn.close()
        return redirect('/')

    return render_template('edit.html', contact=contact)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM contacts WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    create_table()
    app.run(debug=True)