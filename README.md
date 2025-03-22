# Prescription Reader AI

## Overview

The **Prescription Reader AI** is an AI-powered application that digitizes handwritten prescriptions. It uses **Google Cloud Vision API** to extract text and matches it with a database to provide accurate medication details in the user’s preferred language.

## Features

- **OCR-Based Prescription Reading**: Extracts medication names from handwritten prescriptions.
- **Google Cloud Vision API Integration**: Uses advanced AI to recognize text from images.
- **Firestore Database**: Compares extracted medication names with a cloud-stored database.
- **Multi-Language Support**: Provides additional drug information in the preferred language.
- **Streamlit Web Interface**: User-friendly interface for uploading prescriptions and retrieving results.

## Tech Stack

- **Backend**: Python, Flask
- **Frontend**: Streamlit
- **Cloud Services**: Google Cloud Vision API, Firestore DB
- **Containerization**: Docker
- **Deployment**: Google Cloud Run

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/gautax/cloud-deployment-app.git
cd cloud-deployment-app
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Google Cloud Credentials

1. Create a service account and download the JSON key file.
2. Set the environment variable:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key.json"
   ```

### 4. Run the Application Locally

```bash
streamlit run app.py
```

## Docker Instructions

### Build the Docker Image

```bash
docker build -t prescription-app .
```

### Run the Docker Container

```bash
docker run -p 8080:8080 \
   -e GOOGLE_APPLICATION_CREDENTIALS="/app/key.json" \
   -v "$(pwd)/key.json:/app/key.json" \
   prescription-app
```

## Deploying to Google Cloud Run

### 1. Authenticate with Google Cloud

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### 2. Build and Push Image to Google Container Registry

```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/prescription-app
```

### 3. Deploy to Cloud Run

```bash
gcloud run deploy prescription-app \
   --image gcr.io/YOUR_PROJECT_ID/prescription-app \
   --platform managed \
   --region europe-west1 \
   --allow-unauthenticated
```

## Usage

1. Upload a scanned prescription image.
2. The AI extracts and identifies medication names.
3. Matches the extracted data with a verified database.
4. Displays the correct medication details in your preferred language.

## Contributing

Feel free to submit pull requests, raise issues, and improve the project!

## License

This project is licensed under the MIT License.

## Contact

For inquiries, reach out on [LinkedIn](https://www.linkedin.com/in/yahya-menkari-a16b06324/) or open an issue in the repository.

