#!/bin/bash

echo "🚀 TDL Expiry Remover Deployment Script"
echo "======================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Build and start containers
echo "🔨 Building and starting containers..."
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    echo "✅ Application deployed successfully!"
    echo ""
    echo "🌐 Your TDL Expiry Remover is now running at:"
    echo "   http://localhost"
    echo "   or"
    echo "   http://localhost:5000"
    echo ""
    echo "📋 Available commands:"
    echo "   docker-compose logs -f    # View logs"
    echo "   docker-compose down       # Stop application"
    echo "   docker-compose up -d      # Start application"
else
    echo "❌ Deployment failed. Check logs with: docker-compose logs"
    exit 1
fi