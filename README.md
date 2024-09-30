# CS4311_INFILTR8_Team1_DecafCats_Fall2024

## Node and Svelte Setup

### Windows Install
- First install Node.js from this link -> https://nodejs.org/en/download/prebuilt-installer

- Once installed cd into the INFILTR8 folder inside the repo

- Inside of the INFILTR8 folder run the command -> npm install

- Then run this command to start website -> npm run dev

### Mac Install
- You are on your own

## New Database Setup
- Go to the website below and click the start for free button. You will need to create an account to do this.
> https://neo4j.com/product/auradb/
- Once an account has been created, you should see a dashboard interface and different plans listed. Select the AuraDB Free plan and create a instance on that plan
- This will take some time to build but once it has complete a file should be saved to your machine with the username and password information. It is important to take note of these and keep the file in a safe place.
- Looking at the instance the "Open" button can be pressed to take you to the web interface of the database.
- The connection URL will need to be copied, since this is what used by svelte to connect to the database. Svelte will also need the username and password information from the file that was downloaded onto your machine.
- Now with the database set up and working locate the .env inside of the INFILTR8 folder and then copy and paste your connection url, username, and password for your database instance.
- That should be everything you need to do to get the cloud based database set up and working. 