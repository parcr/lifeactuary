@echo off
REM MkDocs Build and Serve Script for lifeActuary Documentation (Windows)

echo lifeActuary Documentation Build Script
echo ======================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is required but not installed.
    exit /b 1
)

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo Error: pip is required but not installed.
    exit /b 1
)

if "%1"=="install" goto install
if "%1"=="build" goto build
if "%1"=="serve" goto serve
if "%1"=="deploy" goto deploy
goto usage

:install
echo Installing MkDocs requirements...
pip install -r ../requirements-docs.txt
if errorlevel 1 (
    echo Error: Failed to install requirements.
    exit /b 1
)
echo Requirements installed successfully.
goto end

:build
echo Building documentation...
mkdocs build
if errorlevel 1 (
    echo Error: Failed to build documentation.
    exit /b 1
)
echo Documentation built successfully.
echo Output location: ../site/
goto end

:serve
echo Starting local documentation server...
echo Documentation will be available at: http://localhost:8000
echo Press Ctrl+C to stop the server.
mkdocs serve
goto end

:deploy
echo Deploying to GitHub Pages...
mkdocs gh-deploy
if errorlevel 1 (
    echo Error: Failed to deploy documentation.
    exit /b 1
)
echo Documentation deployed successfully.
goto end

:usage
echo Usage: %0 {install^|build^|serve^|deploy}
echo.
echo Commands:
echo   install  - Install MkDocs and required dependencies
echo   build    - Build the documentation
echo   serve    - Serve documentation locally for development
echo   deploy   - Deploy documentation to GitHub Pages
echo.
echo Examples:
echo   %0 install    # First time setup
echo   %0 serve      # Development server
echo   %0 build      # Build for production
echo   %0 deploy     # Deploy to GitHub Pages
exit /b 1

:end