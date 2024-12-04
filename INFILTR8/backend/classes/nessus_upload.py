import csv
import os
from classes import project, parser

def fileRead(filepath):
    wholeCsv = []
    with open(filepath, mode = 'r') as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            stringLine = ''
            for part in lines:
                if " "  in part:
                    part = part.replace(" ", "-")
                stringLine = stringLine + ' ' + part
            wholeCsv.append(stringLine)
        return wholeCsv

def turnIntoCsv(contents):
    result = []
    for line in contents:
        result.append(line.split())
    return result

def getDataExploits(driver, username, projectId, fileId):
    query = """
    MATCH (f:Report {name: "dataExploits"})-[h:HAS_FILE]->(fi:File {fileId: $fileId})-[r1:NESSUS_FILE]->(p:Project {projectId: $projectId})-[r:HAS_PROJECT]->(u:Analyst {username: $username}) 
    RETURN f.contents as content
    """
    with driver.session() as session:
        resultCount = session.run(query, fileId=fileId, username=username, projectId=projectId)
        try:
            return turnIntoCsv(resultCount.single()['content'])
        except TypeError:
            return []

def countResults(driver, username, projectId, fileId):
    query = """
    MATCH (re:Report)-[h:HAS_FILE]->(f:File {fileId: $fileId})-[r1:NESSUS_FILE]->(p:Project {projectId: $projectId})-[r:HAS_PROJECT]->(u:Analyst {username: $username}) 
    RETURN count(re) as reportCount
    """
    with driver.session() as session:
        resultCount = session.run(query, fileId=fileId, username=username, projectId=projectId)
        return resultCount.single()['reportCount']
    
def countRankAndEntry(driver, username, projectId, fileId):
    query = """
    MATCH (re:Report)-[h:HAS_FILE]->(f:File {fileId: $fileId})-[r1:NESSUS_FILE]->(p:Project {projectId: $projectId})-[r:HAS_PROJECT]->(u:Analyst {username: $username}) 
    WHERE re.name = 'mostInfo' OR re.name = 'rankedEntry'
    RETURN count(re) as reportCount
    """
    with driver.session() as session:
        resultCount = session.run(query, fileId=fileId, username=username, projectId=projectId)
        return resultCount.single()['reportCount']
    
def deleteResults(driver, username, projectId, fileId):
    query = """
    MATCH (re:Report)-[h:HAS_FILE]->(f:File {fileId: $fileId})-[r1:NESSUS_FILE]->(p:Project {projectId: $projectId})-[r:HAS_PROJECT]->(u:Analyst {username: $username}) 
    DETACH DELETE re
    """
    with driver.session() as session:
        session.run(query, fileId=fileId, username=username, projectId=projectId)
        
def deleteRankAndEntry(driver, username, projectId, fileId):
    query = """
    MATCH (re:Report)-[h:HAS_FILE]->(f:File {fileId: $fileId})-[r1:NESSUS_FILE]->(p:Project {projectId: $projectId})-[r:HAS_PROJECT]->(u:Analyst {username: $username})
    WHERE re.name = 'mostInfo' OR re.name = 'rankedEntry'
    DETACH DELETE re
    """
    with driver.session() as session:
        session.run(query, fileId=fileId, username=username, projectId=projectId)

def uploadDataExAndPortZero(driver, username, projectId, fileId, fileName):
    output_base_dir = os.getcwd()+'/output/'
    file = project.getProjectInfomationManyTest(driver, username, projectId, fileId)
    query = """
    MATCH (f:File {fileId: $fileId})-[r1:NESSUS_FILE]->(p:Project {projectId: $projectId})-[r:HAS_PROJECT]->(u:Analyst {username: $username}) 
    WITH f
    CREATE (r:Report {name: $reportName, contents: $upload})
    CREATE (r)-[:HAS_FILE]->(f)
    """
    
    dataExploits = fileRead(output_base_dir+'data_with_exploits'+fileName+'.csv')
    portZero = fileRead(output_base_dir+'port_0_entries'+fileName+'.csv')
    
    with driver.session() as session:
        session.run(query, fileId=fileId, username=username, projectId=projectId, reportName='dataExploits',upload=dataExploits)
        session.run(query, fileId=fileId, username=username, projectId=projectId, reportName='portZero',upload=portZero)
    
    os.remove(output_base_dir+'data_with_exploits'+fileName+'.csv')
    os.remove(output_base_dir+'port_0_entries'+fileName+'.csv')
        
def processAndUpload(driver, username, projectId, fileId, success):
    output_base_dir = os.getcwd()+'/output/'
    file = project.getProjectInfomationManyTest(driver, username, projectId, fileId)
    query = """
    MATCH (f:File {fileId: $fileId})-[r1:NESSUS_FILE]->(p:Project {projectId: $projectId})-[r:HAS_PROJECT]->(u:Analyst {username: $username}) 
    WITH f
    CREATE (r:Report {name: $reportName, contents: $upload})
    CREATE (r)-[:HAS_FILE]->(f)
    """
    if not success:
        print('failed to do the analysis')
        return 
            
    ranked = fileRead(output_base_dir+'ranked_entry_points'+file["file"]+'.csv')
    mostInfo = fileRead(output_base_dir+'entrypoint_most_info'+file["file"]+'.csv')
    
    if countRankAndEntry(driver, username, projectId, fileId) != 0:
        deleteRankAndEntry(driver, username, projectId, fileId)    
    
    with driver.session() as session:
        session.run(query, fileId=fileId, username=username, projectId=projectId, reportName='rankedEntry',upload=ranked)
        session.run(query, fileId=fileId, username=username, projectId=projectId, reportName='mostInfo',upload=mostInfo)
        
    os.remove(output_base_dir+'ranked_entry_points'+file["file"]+'.csv')
    os.remove(output_base_dir+'entrypoint_most_info'+file["file"]+'.csv')