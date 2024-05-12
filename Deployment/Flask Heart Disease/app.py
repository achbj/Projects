import os
from flask import Flask, render_template, request, redirect, url_for, flash, request
import requests
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from pymongo import MongoClient
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import json


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Connect to MongoDB
client = MongoClient(os.getenv('MONGO_URI'))
db = client['flask_auth_db']

# Set REMEMBER_COOKIE_DURATION to keep user logged in for 7 days
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)

# User Model
class User(UserMixin):
    def __init__(self, name, username, email, password, role="patient"):
      self.name = name
      self.username = username
      self.email = email
      self.password = password
      # Enforce role to be one of "patient", "doctor", or "admin"
      if role not in ["patient", "doctor", "admin"]:
          raise ValueError("Invalid role. Role must be 'patient', 'doctor', or 'admin'.")
      self.role = role

    def get_id(self):
        return self.username

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(username):
    user_data = db.users.find_one({"username": username})
    if user_data:
        return User(user_data['name'], user_data['username'], user_data['email'], user_data['password'], user_data['role'] )
    return None

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('layout.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if db.users.find_one({"username": username}):
            flash('Username already exists. Please choose a different username.', 'error')
        else:
            hashed_password = generate_password_hash(password)
            db.users.insert_one({"name":name, "username": username, "email":email, "password": hashed_password, "role": "patient"})
            flash('Account created successfully. Please log in.', 'success')
            return redirect(url_for('login'))
    else:
        # Flash an error message if the username does not exist
        flash('Invalid username. Please try again.', 'error')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # First, check if the username exists in the database
        user_data = db.users.find_one({"username": username})
        if user_data:
            # If the username exists, then verify the password
            if check_password_hash(user_data['password'], password):
                # If the password is correct, create a User object
                user = User(user_data['name'], username, user_data['email'], user_data['password'], user_data['role'])
                login_user(user)
                return redirect(url_for('dashboard'))
        # If username or password is incorrect, show an error message
        flash('Invalid username or password', 'error')
    return render_template('login.html')


@app.route('/protected')
@login_required
def protected():
    return render_template('protected.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/heartdiseasedetection', methods=['GET', 'POST'])
@login_required
def hdd_predict():
    if request.method == 'POST':
        # Get form data

        form_data = request.form.to_dict()
        # Convert values to numeric types
        for key in form_data:
          form_data[key] = float(form_data[key])

       # Convert form data to JSON
        json_data = json.dumps(form_data)

        # Send POST request to models API
        response = requests.post('http://127.0.0.1:8000/predict', data=json_data)

        # Get prediction results
        prediction_label = response.json()['prediction_label']
        prediction_percentage = response.json()['prediction_percentage']
        left_percentage = response.json()['left_percentage']
        patients_data = response.json()['patients_data']

        if prediction_label == 1:
            prediction_label = "Yes"
            yes_probability = prediction_percentage
            no_probability = left_percentage
        if prediction_label == 0:
            prediction_label = "No"
            no_probability = prediction_percentage
            yes_probability = left_percentage
            
        return render_template('hdd.html', prediction_label=prediction_label, yes_probability = yes_probability, no_probability=no_probability, patients_data=patients_data)
    
    return render_template('hdd.html')


if __name__ == '__main__':
    app.run(debug=True)
