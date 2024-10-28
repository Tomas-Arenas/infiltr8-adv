def countProjects(driver, username):
    query = "MATCH (p:Project)-[r:HAS_PROJECT]->(u:Analyst {username: $username}) RETURN count(p) as total"

    with driver.session() as session:
        numProject = session.run(query, username=username)
        return numProject.single()['total']

def projectParser(project):
    print("Project record:", project)
    return {'projectId': project['projectId'], 'projectname': project['projectname'], 'ips': project['ips'], 'exploits': project['exploits']}

def allProjectInfo(driver, username):
    query = "MATCH (p:Project)-[:HAS_PROJECT]->(a:Analyst {username: $username}) RETURN p.projectId AS projectId, p.projectName AS projectname, p.ips AS ips, p.exploits AS exploits"
    with driver.session() as session:
        result = session.run(query, username=username)
        all_projects = [projectParser(record) for record in result]
        print("All projects:", all_projects) 
        return all_projects


def getProjectInfomation(driver, username, projectId):
    query = "MATCH (p:Project {projectId: $projectId})-[r:HAS_PROJECT]->(u:Analyst {username: $username}) RETURN p as project"

    with driver.session() as session:
        result = session.run(query, projectId=projectId, username=username)
        project = result.single()["project"]
        return projectParser(project)

def createProject(driver,username, projectName, ips, exploits):

    query = (
        """
        MATCH (u:Analyst {username: $username})
        CREATE (p:Project {projectId: $projectId, projectName: $projectName, ips: $ips, exploits: $exploits})-[:HAS_PROJECT]->(u)
        return p.projectId AS projectId
        """
        )

    projectId = countProjects(driver, username) + 1
    with driver.session() as session:
        result = session.run(query, projectId=projectId, username=username, projectName=projectName, ips=ips, exploits=exploits)
        projectId = result.single()["projectId"]
        return projectId


def getAllProjectIds(driver, username):
    query = "MATCH (p:Project)-[:HAS_PROJECT]->(a:Analyst{username: $username}) RETURN p.projectId AS projectIds"
    with driver.session() as session:
        result = session.run(query, username=username)
        allIds = []
        for id in result:
            allIds.append(id["projectIds"])
        print(allIds)
        return allIds
