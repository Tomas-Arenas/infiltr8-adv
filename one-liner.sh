#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Remove existing Node.js if present
if command_exists node; then
    echo "Removing existing Node.js installation..."
    sudo apt-get remove -y nodejs
fi

# Install Node.js and npm directly from NodeSource
NODE_VERSION="18.x"

echo "Installing Node.js $NODE_VERSION..."
curl -fsSL https://deb.nodesource.com/setup_$NODE_VERSION | sudo -E bash -
sudo apt-get install -y nodejs

# Verify Node.js and npm installation
echo "Node.js version: $(node -v)"
echo "npm version: $(npm -v)"

## Install Python and pip
if ! command_exists python3; then
    echo "Python3 is not installed. Installing Python3..."
    sudo apt-get install -y python3 python3-pip
else
    echo "Python3 is already installed."
fi


# Install Neo4j
if ! command_exists neo4j; then
    echo "Neo4j is not installed. Installing Neo4j..."
    wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/neotechnology.gpg
    echo 'deb [signed-by=/etc/apt/keyrings/neotechnology.gpg] https://debian.neo4j.com stable latest' | sudo tee -a /etc/apt/sources.list.d/neo4j.list
    sudo apt-get update
    sudo apt-get install neo4j=1:5.25.1
else
    echo "Neo4j is already installed."
fi

sudo systemctl enable neo4j

sudo sed -i '/^#dbms.security.auth_enabled=false/s/^#//;' /etc/neo4j/neo4j.conf
# cypher-shell "MERGE (a:admin {username: 'admin', password: 'admin', passwordHash: 'not set', token: '123456'}) RETURN a"


# Clone the GitHub repository
REPO_URL="https://github.com/Bonilla-Adrian/CS4311_INFILTR8_1DecafCats_Fall2024.git"
PROJECT_DIR="CS4311_INFILTR8_1DecafCats_Fall2024"

if [ ! -d "$PROJECT_DIR" ]; then
    echo "Cloning the repository..."
    git clone "$REPO_URL"
else
    echo "Repository already cloned."
fi

cd "$PROJECT_DIR"

# Install Node.js dependencies
if [ -f "package.json" ]; then
    echo "Installing Node.js dependencies..."
    cd INFILTR8
    npm install
else
    echo "package.json not found. Skipping Node.js dependencies installation."
fi

# Install Python dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    pip3 install -r requirements.txt
else
    echo "requirements.txt not found. Skipping Python dependencies installation."
fi

# Install flask_cors module
echo "Installing flask_cors module..."
pip3 install flask_cors category_encoders flask_session python-dotenv


# Create .env file with Neo4j connection information
echo "Creating .env file with Neo4j connection information..."

NEO4J_URI="bolt://localhost:7687"
NEO4J_USER="neo4j"
NEO4J_PASSWORD="neo4j"

cd backend

cat <<EOL > .env
URI=$NEO4J_URI
USERNAME=$NEO4J_USER
PASSWORD=$NEO4J_PASSWORD
EOL

echo ".env file created successfully."

# Additional setup tasks (e.g., configuring environment variables, database setup)
# Add any additional setup tasks here
#Run starter.py script

#remove java
#sudo apt-get purge openjdk*
#sudo apt-get autoremove

#install new java runtime
#sudo apt-get update
#sudo apt-get install openjdk-11-jre openjdk-11-jdk

# set java default
#sudo update-alternatives --config java

# Start Neo4j in the background
#sudo neo4j restart &

#sleep 30

#cypher-shell "MERGE (a:admin {username: 'admin', password: 'admin', passwordHash: 'not set', token: '123456'}) RETURN a"

#echo "Running starter.py script..."
cd ..
cd ..
cd ..
#python3 starter.py


# Create run.sh script
RUN_SCRIPT="INFILTR8.sh"
cat <<EOL > $RUN_SCRIPT
#!/bin/bash

PROJECT_DIR="CS4311_INFILTR8_1DecafCats_Fall2024"

# Start Neo4j in the background
echo "Starting Neo4j in the background..."
sudo neo4j restart &

# Wait for Neo4j to start up
sleep 30

cypher-shell "MERGE (a:admin {username: 'admin', password: 'admin', passwordHash: 'not set', token: '123456'}) RETURN a"

cd "$PROJECT_DIR"
# Run starter.py script
echo "Running starter.py script..."
python3 starter.py
EOL



chmod +x $RUN_SCRIPT

./$RUN_SCRIPT

echo "Installation and setup completed successfully."
echo "INFILTR8.sh script will start the app"
