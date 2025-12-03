#!/bin/bash

# BOB ATM Dashboard Quick Start Script
echo "🏦 Starting Bank of Baku ATM Strategy Dashboard..."
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker daemon is not running. Please start Docker."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "⚠️  docker-compose not found, using 'docker compose' instead..."
    COMPOSE_CMD="docker compose"
else
    COMPOSE_CMD="docker-compose"
fi

# Stop any existing containers
echo "📦 Stopping existing containers..."
$COMPOSE_CMD down 2>/dev/null

# Build and start
echo "🔨 Building Docker image..."
$COMPOSE_CMD build

echo "🚀 Starting dashboard..."
$COMPOSE_CMD up -d

# Wait for container to be healthy
echo "⏳ Waiting for dashboard to be ready..."
sleep 5

# Check if container is running
if docker ps | grep -q bob-atm-dashboard; then
    echo ""
    echo "✅ Dashboard is running!"
    echo ""
    echo "📊 Access the dashboard at: http://localhost:8501"
    echo ""
    echo "📝 Useful commands:"
    echo "   • View logs:    $COMPOSE_CMD logs -f"
    echo "   • Stop:         $COMPOSE_CMD down"
    echo "   • Restart:      $COMPOSE_CMD restart"
    echo "   • Rebuild:      $COMPOSE_CMD build --no-cache"
    echo ""
else
    echo ""
    echo "❌ Failed to start dashboard. Check logs with:"
    echo "   $COMPOSE_CMD logs"
    exit 1
fi
