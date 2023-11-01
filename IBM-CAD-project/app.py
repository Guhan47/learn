# Import necessary libraries and modules
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import functools

# Create a Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.secret_key = '65249356f7e2e89464144489a2b85e5d8c06ffa2c2c0eab4'
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Define the login-required decorator
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return wrapped_view
@app.route('/about')
def about():
    return render_template('about.html')
# Routes
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/info")
def info():
    return render_template("info.html")
@app.route("/memories")
def memories():
    return render_template("memories.html")
@app.route("/recent")
def recent():
    return render_template("recent.html")

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('travel'))
        else:
            error = "Invalid email or password"
    return render_template('login.html', error=error)

@app.route('/travel')
@login_required
def travel():
    return render_template('travel.html')



@app.route('/form_detail', methods=['GET', 'POST'])
def form_detail():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if password != confirm_password:
            return "Password and Confirm Password do not match. Please try again."
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "Email already exists. Please use a different email."
        new_user = User(fullname=fullname, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('success'))
    return render_template('form_detail.html')

@app.route('/success')
def success():
    return render_template('success.html')

# CLI command to view the database
@app.cli.command('view-db')
def view_db():
    users = User.query.all()
    for user in users:
        print(f"ID: {user.id}, Full Name: {user.fullname}, Email: {user.email}")

if __name__ == '__main__':
    app.run(debug=True)
