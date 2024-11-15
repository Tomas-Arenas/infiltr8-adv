from neo4j import GraphDatabase
import bcrypt


def create_user(tx, username, hashed_password, recovery_key):
    query = (
        """
        MERGE (a:Analyst {username: $username})
        ON CREATE SET a.password = $hashed_password, a.recovery_key = $recovery_key
        ON MATCH SET a.existing = true
        MERGE (u:User)
        MERGE (a)-[:IS_A]->(u)
        RETURN a.existing AS existing
        """
    )
    
    result = tx.run(query, username=username, hashed_password=hashed_password, recovery_key=recovery_key)
    record = result.single()
    return record["existing"] if record else False  # Returns True if the user exists, otherwise False

def find_user_by_username(tx, username):
    query = "MATCH (a:Analyst {username: $username}) RETURN a"
    result = tx.run(query, username=username)
    return result.single()

def login_user(driver, username, password):
    with driver.session() as session:
        user_record = session.read_transaction(find_user_by_username, username)
        if user_record:
            user = user_record["a"]
            hashed_password = user["password"]
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                return True
        return False