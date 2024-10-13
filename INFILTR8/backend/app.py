import os
from flask import Flask, make_response, jsonify, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from flask_cors import CORS
from dotenv import dotenv_values
from classes import database
from classes import user_service
import bcrypt
from flask_session import Session


# Gets all the env variables
config = dotenv_values(".env")
URI = config['URI']
AUTH = (config['USERNAME'], config['PASSWORD'])

# Used to know where to save the files ones uploaded
UPLOAD_FOLDER = "./nessus-drop"
ALLOWED_EXTENSIONS = {'nessus'} # not used but might be

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.urandom(12).hex() # Needed to sign session cookies and what not
CORS(app) # have to have or nothing works

# Flask-Session configuration
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './flask_session'  # Ensure the directory exists and is writable
app.config['SESSION_PERMANENT'] = False  # Disable permanent sessions
app.config['SESSION_USE_SIGNER'] = True  # To add an extra layer of security
Session(app)

# Makes the database object can be used anywhere
neo4j = database.DataBase(URI, AUTH)
driver = neo4j.driver_make()

@app.route("/flask-api/test")
def test():
    return jsonify({'info': 'Test to makes sure everything is working'})

@app.route("/flask-api/test2")
def test2():
    records = neo4j.run_query("MATCH (n:Person) RETURN n LIMIT 25")
    names = []
    for record in records:
        names.append(record[0]['name'])
    return jsonify({'test':names})

# Handles the uploading of the file
@app.route("/flask-api/nessus-upload", methods=['POST'])
def nessusFileUpload():
    # Makes sure the POST is tagged that is a file and nothing else
    if 'file' not in request.files:
        return jsonify({'info':'Need to be told it is file upload'})
    
    file = request.files['file']
    # Checks that a file was upload (could be removed becase frontend handles this)
    if file.filename == '':
        print('No selected file')
        return jsonify({'info':'no file'})
    if file:
        # security stuff
        filename = secure_filename(file.filename)
        # Saves it based on the give file path and uses the upload file name
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'status':'file was sent and has been saved on server'})

# Sends the entry points
@app.route("/flask-api/entry-points")
def rankedEntryPoints():
    return

# creates user in the db
@app.route('/flask-api/create_user', methods=['POST'])
def create_user_route():
    data = request.get_json()
    first_name = data['first_name']
    last_name = data['last_name']
    username = data['username']
    password = data['password']

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    with driver.session() as session:
        session.write_transaction(user_service.create_user, username, first_name, last_name, hashed_password.decode('utf-8'))
    
    return jsonify({"status": "User created successfully"})

# checks login information 
@app.route('/flask-api/login', methods=['POST'])
def login_route():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if user_service.login_user(driver, username, password):
        session['username'] = username  # Store username in session
        return jsonify({"status": "Login successful"})
    else:
        return jsonify({"status": "Invalid username or password"}), 401

@app.route('/flask-api/logout', methods=['POST'])
def logout_route():
    session.pop('username', None)
    session.clear()
    return jsonify({"status": "Logged out successfully"})

@app.route('/flask-api/check_session', methods=['GET'])
def check_session_route():
    if 'username' in session:
        return jsonify({"status": "Logged in", "logged_in": True, "username": session['username']})
    else:
        return jsonify({"status": "Not Logged in", "logged_in": False, "username": ''})