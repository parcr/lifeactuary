#!/bin/bash

# MkDocs Build and Serve Script for lifeActuary Documentation

echo "lifeActuary Documentation Build Script"
echo "======================================"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Check if pip is available
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "Error: pip is required but not installed."
    exit 1
fi

# Function to install requirements
install_requirements() {
    echo "Installing MkDocs requirements..."
    
    if command -v pip3 &> /dev/null; then
        pip3 install -r ../requirements-docs.txt
    else
        pip install -r ../requirements-docs.txt
    fi
    
    if [ $? -eq 0 ]; then
        echo "Requirements installed successfully."
    else
        echo "Error: Failed to install requirements."
        exit 1
    fi
}

# Function to build documentation
build_docs() {
    echo "Building documentation..."
    mkdocs build
    
    if [ $? -eq 0 ]; then
        echo "Documentation built successfully."
        echo "Output location: ../site/"
    else
        echo "Error: Failed to build documentation."
        exit 1
    fi
}

# Function to serve documentation locally
serve_docs() {
    echo "Starting local documentation server..."
    echo "Documentation will be available at: http://localhost:8000"
    echo "Press Ctrl+C to stop the server."
    mkdocs serve
}

# Function to deploy to GitHub Pages
deploy_docs() {
    echo "Deploying to GitHub Pages..."
    mkdocs gh-deploy
    
    if [ $? -eq 0 ]; then
        echo "Documentation deployed successfully."
    else
        echo "Error: Failed to deploy documentation."
        exit 1
    fi
}

# Parse command line arguments
case "$1" in
    install)
        install_requirements
        ;;
    build)
        build_docs
        ;;
    serve)
        serve_docs
        ;;
    deploy)
        deploy_docs
        ;;
    *)
        echo "Usage: $0 {install|build|serve|deploy}"
        echo ""
        echo "Commands:"
        echo "  install  - Install MkDocs and required dependencies"
        echo "  build    - Build the documentation"
        echo "  serve    - Serve documentation locally for development"
        echo "  deploy   - Deploy documentation to GitHub Pages"
        echo ""
        echo "Examples:"
        echo "  $0 install    # First time setup"
        echo "  $0 serve      # Development server"
        echo "  $0 build      # Build for production"
        echo "  $0 deploy     # Deploy to GitHub Pages"
        exit 1
        ;;
esac