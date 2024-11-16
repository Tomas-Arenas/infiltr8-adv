from neo4j import GraphDatabase
import bcrypt


def create_user(tx, username, hashed_password, recovery_key):
    query = (
        """
        MERGE (a:Analyst {username: $username})
        ON CREATE SET a.password = $hashed_password, a.recovery_key = $recovery_key
        RETURN EXISTS((a)-[:IS_A]->(:User)) AS existing
        """
    )
    result = tx.run(query, username=username, hashed_password=hashed_password, recovery_key=recovery_key)
    record = result.single()
    return not record["existing"] if record else False  # True if user was newly created


def find_user_by_username(tx, username):
    query = "MATCH (a:Analyst {username: $username}) RETURN a"
    result = tx.run(query, username=username)
    if result.peek():  # Check if any records exist
        return result.single()

    # Check if the user is an admin
    query = "MATCH (a:admin {username: $username}) RETURN a"
    result = tx.run(query, username=username)
    return result.single() if result.peek() else None

def login_user(driver, username, password):
    with driver.session() as session:
        user_record = session.read_transaction(find_user_by_username, username)
        if user_record:
            user = user_record["a"]
            user_labels = user.labels

            # Check if the user is an Admin
            if "admin" in user_labels:
                stored_password = user.get("password")
                print(f"Admin stored password: {stored_password}")
                if stored_password is None:
                    return {"error": "Admin password not set"}
                if password == stored_password:
                    return {"status": "Admin", "username": username}
                else:
                    return {"error": "Invalid password for Admin"}

            # Check if the user is an Analyst
            elif "Analyst" in user_labels:
                hashed_password = user.get("password")
                if hashed_password is None:
                    return {"error": "Analyst password not set"}
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                    return {"status": "User", "username": username}
                else:
                    return {"error": "Invalid password for Analyst"}

        return {"error": "User not found"}  # User does not exist