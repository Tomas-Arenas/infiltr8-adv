from neo4j import GraphDatabase

<<<<<<< HEAD
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
=======
class DataBase:
    
    def __init__(self,URI, AUTH):
        self.URI = URI
        self.AUTH = AUTH
    
    def driver_make(self):
        return GraphDatabase.driver(self.URI, auth=self.AUTH)
    
    def run_query(self, query):
        driver = self.driver_make()
        records, summary, keys = driver.execute_query(query, database_="neo4j")
        driver.close()
        return records
>>>>>>> f848c1191e31cd57cbf2c4f8703ffb5e8559ca0e
