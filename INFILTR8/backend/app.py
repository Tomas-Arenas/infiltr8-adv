from flask import Flask, make_response, request, jsonify
from flask_cors import CORS
from neo4j import GraphDatabase
from dotenv import dotenv_values
from user_service import createUserNode
import bcrypt

config = dotenv_values("../.env")

app = Flask(__name__)
CORS(app)
# CORS(app, resources={r"/api/*": {"origins": "*"}})  # Apply CORS to all routes under '/api'
@app.route("/flask-api/test")
def test():
    URI = config['URI']
    AUTH = (config['USERNAME'], config['PASSWORD'])

    driver = GraphDatabase.driver(URI, auth=AUTH)

    records, summary, keys = driver.execute_query(
        "MATCH (n:Person) RETURN n LIMIT 25",
        database_="neo4j",
    )
    names = []
    for record in records:
        names.append(record[0]['name'])
    return jsonify({'info': names})

@app.route("/flask-api/test2")
def test2():
    return jsonify({'test':'test2 to see if the proxy stuff works'})

# Handles the uploading of the file
@app.route("/flask-api/nessus-upload")
def nessusFileUpload():
    return jsonify({'test': 'hold'})

# Sends the entry points
@app.route("/flask-api/entry-points")
def rankedEntryPoints():
    return

# creates user in the db
@app.route('flask-api/create_user', methods=['POST'])
def create_user_route():
    data = request.get_json()
    first_name = data['first_name']
    last_name = data['last_name']
    username = data['username']
    password = data['password']

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    with driver.session() as session:
        session.write_transaction(create_user, first_name, last_name, username, hashed_password.decode('utf-8'))
    
    return jsonify({"status": "User created successfully"})