@echo off
echo ========================================
echo     Manifest AI Docker Setup
echo ========================================

:: Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo Error: Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

:: Check if Docker Compose is available
docker-compose --version >nul 2>&1
if not errorlevel 1 (
    set COMPOSE_CMD=docker-compose
) else (
    docker compose version >nul 2>&1
    if not errorlevel 1 (
        set COMPOSE_CMD=docker compose
    ) else (
        echo Error: Docker Compose is not available. Please install Docker Compose.
        pause
        exit /b 1
    )
)

echo Using: %COMPOSE_CMD%
echo.

:: Stop existing containers if running
echo Stopping existing containers...
%COMPOSE_CMD% down

:: Pull latest images
echo Pulling latest Docker images...
%COMPOSE_CMD% pull

:: Build and start services
echo Building and starting services...
%COMPOSE_CMD% up --build -d

:: Show status
echo.
echo Services started! Current status:
%COMPOSE_CMD% ps

echo.
echo ========================================
echo Setup Complete!
echo.
echo The application will be available at:
echo   🌐 Streamlit App: http://localhost:8501
echo   🤖 Ollama API: http://localhost:11434
echo.
echo Note: Initial startup may take 5-10 minutes to download models.
echo Check logs with: %COMPOSE_CMD% logs -f
echo.
echo To stop the services: %COMPOSE_CMD% down
echo ========================================
pause