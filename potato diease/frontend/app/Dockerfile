# Use Node.js as base image
FROM node:18

# Set working directory
WORKDIR /app

# Copy dependencies
COPY app/package.json app/package-lock.json ./
RUN npm install

# Copy the entire mobile app code
COPY . .

# Start Metro Bundler for React Native
CMD ["npx", "react-native", "start"]

# Expose the Metro Bundler port
EXPOSE 8081
