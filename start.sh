#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}    Manifest AI Docker Setup${NC}"
echo -e "${BLUE}========================================${NC}"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}Error: Docker Compose is not available. Please install Docker Compose.${NC}"
    exit 1
fi

# Determine which compose command to use
COMPOSE_CMD="docker-compose"
if docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
fi

echo -e "${YELLOW}Using: $COMPOSE_CMD${NC}"
echo ""

# Stop existing containers if running
echo -e "${YELLOW}Stopping existing containers...${NC}"
$COMPOSE_CMD down

# Pull latest images
echo -e "${YELLOW}Pulling latest Docker images...${NC}"
$COMPOSE_CMD pull

# Build and start services
echo -e "${YELLOW}Building and starting services...${NC}"
$COMPOSE_CMD up --build -d

# Show status
echo ""
echo -e "${GREEN}Services started! Current status:${NC}"
$COMPOSE_CMD ps

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Setup Complete!${NC}"
echo ""
echo -e "${YELLOW}The application will be available at:${NC}"
echo -e "${GREEN}  🌐 Streamlit App: http://localhost:8501${NC}"
echo -e "${GREEN}  🤖 Ollama API: http://localhost:11434${NC}"
echo ""
echo -e "${YELLOW}Note: Initial startup may take 5-10 minutes to download models.${NC}"
echo -e "${YELLOW}Check logs with: $COMPOSE_CMD logs -f${NC}"
echo ""
echo -e "${YELLOW}To stop the services: $COMPOSE_CMD down${NC}"
echo -e "${BLUE}========================================${NC}"