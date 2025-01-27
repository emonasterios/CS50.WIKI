#!/bin/bash

# Navigate to the project directory
cd ~/CS50.WIKI

# Check if gcloud CLI is installed, otherwise, exit
if ! command -v gcloud &> /dev/null
then
    echo "gcloud command not found. Please install Google Cloud SDK."
    exit 1
fi

# Verify the presence of manage.py
if [ ! -f "manage.py" ]; then
  echo "Error: manage.py not found in the project directory."
  exit 1
fi

# Verify the presence of a Dockerfile
if [ ! -f "Dockerfile" ]; then
  echo "Error: Dockerfile not found in the project directory."
  exit 1
fi

# Verify that there is a requirements.txt
if [ ! -f "requirements.txt" ]; then
    echo "Error: requirements.txt not found in the project directory."
    exit 1
fi

# Verify the virtual environment is activated, and if not, activate it.
if [ -z "$VIRTUAL_ENV" ]; then
  echo "Virtual environment not active, activating..."
  python3 -m venv --symlinks venv
  source venv/bin/activate
fi
# Obtain the Project ID
PROJECT_ID=$(gcloud projects list --format="value(PROJECT_ID)")

if [[ -z "$PROJECT_ID" ]]; then
  echo "Error: Unable to obtain project id from gcloud"
  exit 1
fi

echo "Using Project ID: $PROJECT_ID"

# Build the Docker image
echo "Building Docker image..."
docker build -t wiki-image .

# Check that the image was built using `docker images`
if ! docker images wiki-image &> /dev/null
then
    echo "Error: Docker image was not created successfully"
    exit 1
fi
echo "Docker image built successfully!"

# Deploy the application to Cloud Run
echo "Deploying to Cloud Run..."
gcloud run deploy wiki-app --source . --allow-unauthenticated --project "$PROJECT_ID"

echo "Deployment Complete. Use the URL provided by Cloud Run to test the application"