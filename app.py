from flask import Flask, render_template, request, redirect, url_for, session, flash
import random
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import time
import sqlite3

app = Flask(__name__)
app.secret_key = "exam_stress_manager_secret_key"

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
    # 'home' is the root route which now shows the login choice
    allowed_routes = ['home', 'login_choice', 'login', 'admin_login', 'send_otp', 'verify_otp', 'static']
    if request.endpoint not in allowed_routes:
        if request.endpoint == 'admin_dashboard':
            if 'admin_logged_in' not in session:
                return redirect(url_for('home'))
        else:
            if 'user_email' not in session and 'admin_logged_in' not in session:
                return redirect(url_for('home'))

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
    return render_template('login_choice.html')

@app.route('/index')
def index():
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
    sender_email = "examstressmanagement@gmail.com"
    sender_password = "ybjoyhlqkvkybvli"

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
        return redirect(url_for('index'))
    return render_template('student_login.html')

@app.route('/send-otp', methods=['POST'])
def send_otp():
    if 'user_email' in session:
        return redirect(url_for('index'))

    email = request.form.get('email', '')
    if not email or not email.endswith('@kanchiuniv.ac.in'):
        flash("This system only accepts official college email IDs ending with @kanchiuniv.ac.in", "error")
        return redirect(url_for('login'))
        
    otp = str(random.randint(100000, 999999))
    
    # Store the OTP in Flask session variables when generating it
    session['otp'] = otp
    session['otp_email'] = email
    
    # OTP expiry should be stored using a timestamp (2 minutes validity)
    session['otp_expiry'] = time.time() + 120
    session.modified = True
    
    send_otp_email(email, otp)
    flash("OTP sent successfully. Please check your email.", "success")
    return redirect(url_for('verify_otp'))

@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if 'user_email' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        user_otp = request.form.get('otp')
        
        # Step 1: Check if 'otp' exists in session.
        if 'otp' not in session or 'otp_expiry' not in session:
            flash("Session expired. Please request a new OTP.", "error")
            return redirect(url_for('login'))
            
        # Step 2: Check if current time is greater than session['otp_expiry'].
        if time.time() > session['otp_expiry']:
            session.pop('otp', None)
            session.pop('otp_email', None)
            session.pop('otp_expiry', None)
            session.modified = True
            flash("OTP expired. Please request a new OTP.", "error")
            return redirect(url_for('login'))
            
        # Step 3: If not expired, compare entered OTP with session['otp'].
        if user_otp == session['otp']:
            # Log the student in
            session['user_email'] = session.get('otp_email')
            
            # Clear the OTP session
            session.pop('otp', None)
            session.pop('otp_email', None)
            session.pop('otp_expiry', None)
            session.modified = True
            
            # Redirect to the index page
            flash("Login successful!", "success")
            return redirect(url_for('index'))
        else:
            # If OTP is incorrect
            flash("Invalid OTP. Please try again.", "error")
            return redirect(url_for('verify_otp'))

    # Check for GET request to prevent random accesses without an OTP in play
    if 'otp' not in session:
        flash("Session expired. Please request a new OTP.", "error")
        return redirect(url_for('login'))

    return render_template('verify_otp.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
