# Use a Node image with alpine disabled to avoid musl errors
FROM node:20

# Set working directory
WORKDIR /app

# Copy only package.json first (layer caching optimization)
COPY package*.json ./

# Install dependencies inside container

RUN npm install

# Copy the rest of the frontend code
COPY . .

# Expose the port Vite uses
EXPOSE 5173

# Start dev server
CMD ["npm", "run", "dev" ,"--host"]
