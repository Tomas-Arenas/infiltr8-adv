# CS4311_INFILTR8_Team1_DecafCats_Fall2024

## Node and Svelte Setup

### Windows Install
- First install Node.js from this link -> https://nodejs.org/en/download/prebuilt-installer

- Once installed cd into the INFILTR8 folder inside the repo

- Inside of the INFILTR8 folder run the command -> npm install

- Then run this command to start website -> npm run dev

### Mac Install
- You are on your own

## Database and Docker Setup
- Install Docker by following the steps here (will need WSL for windows)
	> https://docs.docker.com/desktop/install/windows-install/
	> https://docs.docker.com/desktop/install/mac-install/
- Once installed open a docker desktop and make sure it is working. Also open WSL and type "docker" to make sure it was installed globally. 
- Enter the following command into WSL
	> docker pull el68/neo4j:latest
- Then enter the following command
	> docker run --name neo4j-test-data --publish=7474:7474 --publish=7687:7687 --env NEO4J_AUTH=none el68/neo4j:latest
- If everything worked you should be able to access the database at this url.
	> http://localhost:7474/browser/
- You'll be asked for a password but this is not needed just hit connect. Click on the star icon on the left side of the screen and run Team Make Script. This will put information about our team in the database and is used to make sure everything is working.
- With the website running click and report and then click the test database. If everything works a alert should popup and have some information.
- I will be making the process better and setting some kind of persistence storage up.