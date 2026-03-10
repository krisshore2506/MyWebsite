from flask import Flask, render_template, request, redirect, url_for, session, flash
import random
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import time

# Flask setup
app = Flask(__name__)   # ✅ remove static_folder line
app.secret_key = 'super_secret_key_for_otp_login'  # Required for sessions


# Home Page
@app.route('/')
def home():
    return render_template('index.html')


# Stress Tips Page
@app.route('/stress')
def stress():
    return render_template('stress.html')


# Study Techniques Page
@app.route('/study')
def study():
    return render_template('study.html')


# Timer Page
@app.route('/timer')
def timer():
    return render_template('timer.html')


# Contact Page
@app.route('/contact')
def contact():
    return render_template('contact.html')


# Contact Form Submission
@app.route('/submit', methods=['POST'])
def submit():

    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    print("New Feedback Received")
    print("Name:", name)
    print("Email:", email)
    print("Message:", message)

    return redirect(url_for('contact'))


# --- OTP LOGIN SYSTEM ---

def send_otp_email(receiver_email, otp):
    """
    Sends the OTP via email.
    Note: For a real application, you need to provide a valid SMTP server,
    sender email, and password (or app password).
    """
    sender_email = "your_email@gmail.com"
    sender_password = "your_app_password"  # Use an App Password if using Gmail

    msg = MIMEText(f"Your OTP for login is: {otp}. It is valid for 2 minutes.")
    msg['Subject'] = "Your Login OTP"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Print OTP to terminal for easy testing without valid email configuration!
    print(f"\n[{datetime.now()}] DEVELOPMENT OTP for {receiver_email}: {otp}\n")

    try:
        # Uncomment and configure with real credentials to enable actual email sending
        # server = smtplib.SMTP('smtp.gmail.com', 587)
        # server.starttls()
        # server.login(sender_email, sender_password)
        # server.send_message(msg)
        # server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
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
        
    # Generate 6-digit OTP
    otp = str(random.randint(100000, 999999))
    
    # Store in session
    session['otp'] = otp
    session['otp_email'] = email
    session['otp_time'] = time.time()  # Store current timestamp
    session['otp_attempts'] = 0
    
    # Try to send email (prints to console by default)
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
        
        # Check expiration (2 minutes)
        current_time = time.time()
        otp_time = session.get('otp_time', 0)
        if current_time - otp_time > 120:
            session.pop('otp', None)
            flash("OTP has expired. Please request a new one.", "error")
            return redirect(url_for('login'))
            
        # Check attempts
        attempts = session.get('otp_attempts', 0)
        if attempts >= 3:
            session.pop('otp', None)
            flash("Too many failed attempts. Please request a new OTP.", "error")
            return redirect(url_for('login'))

        # Verify OTP
        if user_otp == session['otp']:
            # Success! Log the user in
            session['user_email'] = session['otp_email']
            
            # Clear sensitive session data
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
    return redirect(url_for('login'))


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
