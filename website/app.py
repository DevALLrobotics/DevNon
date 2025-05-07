from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secretkey123'

# Path to the database
DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'database.db')

# Database connection
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Home Route
@app.route('/')
def home():
    try:
        conn = get_db_connection()
        bookings = conn.execute('SELECT * FROM bookings').fetchall()
        conn.close()
        return render_template('home.html', bookings=bookings)
    except Exception as e:
        return f"Error: {str(e)}"

# View Database Route
@app.route('/view_db')
def view_db():
    try:
        conn = get_db_connection()
        users = conn.execute('SELECT * FROM users').fetchall()
        conn.close()
        users_list = [dict(user) for user in users]
        return {'users': users_list}
    except Exception as e:
        return {'error': str(e)}

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not email or not password:
            flash('Email and Password are required!')
            return redirect(url_for('login'))

        try:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
            conn.close()

            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['username'] = user['name']
                flash('Login successful!')
                return redirect(url_for('home'))
            else:
                flash('Invalid email or password!')
        except Exception as e:
            flash(f"Error: {str(e)}")

    return render_template('login.html')

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']

        if not name or not email or not password:
            flash('All fields are required!')
            return redirect(url_for('register'))

        try:
            hashed_password = generate_password_hash(password)

            conn = get_db_connection()
            conn.execute('INSERT INTO users (name, password, email) VALUES (?, ?, ?)', 
                         (name, hashed_password, email))
            conn.commit()
            conn.close()
            flash('Registration successful!')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email already exists!')
        except Exception as e:
            flash(f"Error: {str(e)}")

    return render_template('register.html')

# Booking Route
@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if 'user_id' not in session:
        flash('Please log in to book a field.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        user_id = session['user_id']
        field_name = request.form['field_name']
        date = request.form['date']
        time = request.form['time']

        try:
            conn = get_db_connection()
            conn.execute('INSERT INTO bookings (user_id, field_name, date, time) VALUES (?, ?, ?, ?)', 
                         (user_id, field_name, date, time))
            conn.commit()
            conn.close()

            flash('Booking successful!')
            return redirect(url_for('home'))

        except Exception as e:
            flash(f"Error: {str(e)}")

    return render_template('booking.html')

# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
