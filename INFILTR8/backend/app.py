from flask import Flask, make_response, jsonify
from flask_cors import CORS
from neo4j import GraphDatabase
from dotenv import dotenv_values

config = dotenv_values(".env")

app = Flask(__name__)
CORS(app)
# CORS(app, resources={r"/api/*": {"origins": "*"}})  # Apply CORS to all routes under '/api'
@app.route("/test")
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
        # print(record)
        # print(type(record))
        names.append(record[0]['name'])
    return jsonify({'info': names})