# resultName is the name that is given to the node that will contain the info
def getResult(driver, resultName, currentProject, username, fileId):
    query = """
        MATCH (r:Report {name: $name})-[:HAS_FILE]->(f:File {fileId: $fileId})-[r1:NESSUS_FILE]->(p:Project {projectId: $projectId})-[:HAS_PROJECT]->(a:Analyst {username: $username}) 
        RETURN r.contents AS content
    """
    with driver.session() as sessionData:
        result = sessionData.run(query, name=resultName, fileId=fileId, projectId=currentProject, username=username)
        record = result.single()
        
    output = []
    for line in record['content']:
        output.append(line.split())
        
    return output