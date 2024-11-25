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
            user_properties = user._properties  # Access properties of the node
            
            # Debug: Print all user properties
            print('User properties:', user_properties)

            # Check if the user is an Admin
            if "admin" in user_labels:
                stored_password = user_properties.get("password")
                print(f"Admin stored password: {stored_password}")
                if stored_password is None:
                    return {"error": "Admin password not set"}
                if password == stored_password:
                    return {"status": "Admin", "username": username}
                else:
                    return {"error": "Invalid password for Admin"}

            # Check if the user is an Analyst
            elif "Analyst" in user_labels:
                hashed_password = user_properties.get("password")
                print(f"Stored hashed password for Analyst: {hashed_password}")
                if hashed_password is None:
                    return {"error": "Analyst password not set"}

                # Debug: Check password comparison
                password_matches = bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
                print(f"Password match result: {password_matches}")
                
                if password_matches:
                    return {"status": "User", "username": username}
                else:
                    return {"error": "Invalid password for Analyst"}

        return {"error": "User not found"}  # If no matching user is found
