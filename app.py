from flask import Flask, render_template, request, redirect, url_for

# Flask setup
app = Flask(__name__)   # ✅ remove static_folder line


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


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
