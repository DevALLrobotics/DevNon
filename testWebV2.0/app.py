from flask import Flask, render_template, request, redirect, url_for, flash, session
import pymysql
import os
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'secretkey123'

# Database configuration
DB_HOST = '206.189.81.76'
DB_USER = 'non'
DB_PASSWORD = '1234N'
DB_NAME = 'testdb'

# Database connection
def get_db_connection():
    conn = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn

# Login Required Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Home Route
@app.route('/')
@login_required
def home():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM bookings')
            bookings = cursor.fetchall()
        return render_template('home.html', bookings=bookings)
    except Exception as e:
        flash(f"Error: {str(e)}")
        return redirect(url_for('home'))

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
            with conn.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO users (name, password, email) VALUES (%s, %s, %s)', (name, hashed_password, email)
                )
            conn.commit()
            flash('Registration successful!')
            return redirect(url_for('login'))
        except pymysql.IntegrityError:
            flash('Email already exists!')
        except Exception as e:
            flash(f"Error: {str(e)}")

    return render_template('register.html')

# Booking Route
@app.route('/booking', methods=['GET', 'POST'])
@login_required
def book_field():
    if request.method == 'POST':
        field_type = request.form.get('field-type')
        booking_time = request.form.get('booking-time')

        if not field_type or not booking_time:
            flash("All fields are required.")
            return redirect(url_for('home'))

        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO bookings (user_id, field_name, date, time) VALUES (%s, %s, %s, %s)",
                    (session['user_id'], field_type, booking_time.split('T')[0], booking_time.split('T')[1])
                )
            conn.commit()
            flash("Booking successful!")
        except Exception as e:
            flash(f"Error booking the field: {e}")
        finally:
            conn.close()

    return render_template('booking.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
                user = cursor.fetchone()

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

# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
