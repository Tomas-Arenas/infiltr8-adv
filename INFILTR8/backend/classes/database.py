from neo4j import GraphDatabase
from dotenv import dotenv_values

config = dotenv_values("../../.env")

URI = config['NEO4J_URI']
AUTH = (config['NEO4J_USERNAME'], config['NEO4J_PASSWORD'])

driver = GraphDatabase.driver(URI, auth=AUTH)

records, summary, keys = driver.execute_query(
    "MATCH (n:Person) RETURN n LIMIT 25",
    database_="neo4j",
)

for record in records:
    # print(record)
    # print(type(record))
    print(record[0]['name'])