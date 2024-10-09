from flask import Flask, make_response, jsonify
from flask_cors import CORS
from neo4j import GraphDatabase
from dotenv import dotenv_values

config = dotenv_values(".env")

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