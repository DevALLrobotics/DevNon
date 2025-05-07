from flask import Flask, render_template, request, redirect, url_for, flash, session
import pymysql
import os
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'secretkey123'

# Database configuration
DB_HOST = '143.198.203.134'
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

# Booking Route
@app.route('/booking', methods=['GET', 'POST'])
@login_required
def book_field():
    if request.method == 'POST':
        field_name = request.form.get('field-name')
        date = request.form.get('date')
        time = request.form.get('time')

        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute('INSERT INTO bookings (user_id, field_name, date, time) VALUES (%s, %s, %s, %s)', (session['user_id'], field_name, date, time))
            conn.commit()
            flash('Booking successful for ' + field_name + ' on ' + date + ' at ' + time)
        except Exception as e:
            flash(f"Error: {str(e)}")

        return redirect(url_for('home'))

    return render_template('booking.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
