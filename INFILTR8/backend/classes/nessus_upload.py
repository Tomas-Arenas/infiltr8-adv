import csv

def processAndUpload(driver, username, projectId, filepath):
    ranked = fileRead('/home/erik/utep-fall-24/CS4311_INFILTR8_1DecafCats_Fall2024/INFILTR8/backend/output/ranked_entry_points.csv')
    mostInfo = fileRead('/home/erik/utep-fall-24/CS4311_INFILTR8_1DecafCats_Fall2024/INFILTR8/backend/output/entrypoint_most_info.csv')
    
    query = """
    MATCH (p:Project {projectId: $projectId})-[r:HAS_PROJECT]->(u:Analyst {username: $username}) 
    WITH p
    CREATE (r:Report {name: $reportName, contents: $upload})
    CREATE (r)-[:HAS_FILE]->(p)
    RETURN count(r) as total
    """
    
    with driver.session() as session:
        numProject = session.run(query, username=username, projectId=projectId, reportName='rankedList',upload=ranked)
        numProject = session.run(query, username=username, projectId=projectId, reportName='mostInfo',upload=mostInfo)
        return numProject.single()['total']

def fileRead(filepath):
    wholeCsv = []
    with open(filepath, mode = 'r') as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            stringLine = ''
            for part in lines:
                stringLine = part + ' '
            wholeCsv.append(stringLine)
        return wholeCsv