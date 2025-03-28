# Use official Node.js image
FROM node:18

# Set working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to install dependencies
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the entire frontend code
COPY . .

# Build the Vite app
RUN npm run build

# Install a lightweight static file server
RUN npm install -g serve

# Serve the built Vite app on port 3000
CMD ["serve", "-s", "dist", "-l", "3000"]

# Expose the React frontend port
EXPOSE 3000
