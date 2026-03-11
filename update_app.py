import os

app_content = """from flask import Flask, render_template, request, redirect, url_for, session, flash
import random
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import time
import sqlite3

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_otp_login'

def init_db():
    conn = sqlite3.connect('exam_stress.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT,
            date_submitted TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize DB on start
init_db()

@app.before_request
def require_login():
    allowed_routes = ['login_choice', 'login', 'admin_login', 'send_otp', 'verify_otp', 'static']
    if request.endpoint not in allowed_routes:
        if request.endpoint == 'admin_dashboard':
            if 'admin_logged_in' not in session:
                return redirect(url_for('login_choice'))
        else:
            if 'user_email' not in session and 'admin_logged_in' not in session:
                return redirect(url_for('login_choice'))

@app.route('/login-choice')
def login_choice():
    session.clear()
    return render_template('login_choice.html')

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if 'admin_logged_in' in session:
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'admin' and password == 'admin123':
            session.clear()
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid credentials", "error")
            return redirect(url_for('admin_login'))

    return render_template('admin_login.html')

@app.route('/admin-dashboard')
def admin_dashboard():
    conn = sqlite3.connect('exam_stress.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts ORDER BY date_submitted DESC")
    contacts = cursor.fetchall()
    conn.close()
    return render_template('admin_dashboard.html', contacts=contacts)

@app.route('/')
def home():
    if 'admin_logged_in' in session:
        return redirect(url_for('admin_dashboard'))
    return render_template('index.html')

@app.route('/stress')
def stress():
    if 'admin_logged_in' in session:
        return redirect(url_for('admin_dashboard'))
    return render_template('stress.html')

@app.route('/study')
def study():
    if 'admin_logged_in' in session:
        return redirect(url_for('admin_dashboard'))
    return render_template('study.html')

@app.route('/timer')
def timer():
    if 'admin_logged_in' in session:
        return redirect(url_for('admin_dashboard'))
    return render_template('timer.html')

@app.route('/contact')
def contact():
    if 'admin_logged_in' in session:
        return redirect(url_for('admin_dashboard'))
    return render_template('contact.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    conn = sqlite3.connect('exam_stress.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO contacts (name, email, message)
        VALUES (?, ?, ?)
    ''', (name, email, message))
    conn.commit()
    conn.close()

    print("New Feedback Saved to DB")
    return redirect(url_for('contact'))

# --- OTP LOGIN SYSTEM ---
def send_otp_email(receiver_email, otp):
    sender_email = "kishorekktd123@gmail.com"
    sender_password = "vctgcmcrhiwbvnbr"

    msg = MIMEText(f"Your OTP for login is: {otp}. It is valid for 2 minutes.")
    msg['Subject'] = "Your Login OTP"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print("OTP Email Sent Successfully")
        return True
    except Exception as e:
        print("Error sending email:", e)
        return False

@app.route('/login')
def login():
    if 'user_email' in session:
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/send-otp', methods=['POST'])
def send_otp():
    if 'user_email' in session:
        return redirect(url_for('home'))

    email = request.form.get('email')
    if not email:
        flash("Email is required.", "error")
        return redirect(url_for('login'))
        
    otp = str(random.randint(100000, 999999))
    
    session.clear()
    session['otp'] = otp
    session['otp_email'] = email
    session['otp_time'] = time.time()
    session['otp_attempts'] = 0
    
    send_otp_email(email, otp)
    flash("OTP sent successfully. Please check your email.", "success")
    return redirect(url_for('verify_otp'))

@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if 'user_email' in session:
        return redirect(url_for('home'))
        
    if 'otp' not in session or 'otp_email' not in session:
        flash("Session expired. Please request a new OTP.", "error")
        return redirect(url_for('login'))

    if request.method == 'POST':
        user_otp = request.form.get('otp')
        
        current_time = time.time()
        otp_time = session.get('otp_time', 0)
        if current_time - otp_time > 120:
            session.pop('otp', None)
            flash("OTP has expired. Please request a new one.", "error")
            return redirect(url_for('login'))
            
        attempts = session.get('otp_attempts', 0)
        if attempts >= 3:
            session.pop('otp', None)
            flash("Too many failed attempts. Please request a new OTP.", "error")
            return redirect(url_for('login'))

        if user_otp == session['otp']:
            session['user_email'] = session['otp_email']
            session.pop('otp', None)
            session.pop('otp_time', None)
            session.pop('otp_attempts', None)
            return redirect(url_for('home'))
        else:
            session['otp_attempts'] = attempts + 1
            flash("Invalid OTP. Please try again.", "error")
            return redirect(url_for('verify_otp'))

    return render_template('verify.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('login_choice'))

if __name__ == '__main__':
    app.run(debug=True)
"""
with open(r'c:\Users\KRISSHORE S\OneDrive\Desktop\MyWebsite\app.py', 'w', encoding='utf-8') as f:
    f.write(app_content)

print('app.py has been completely rewritten with SQLite integration and Admin logic.')
