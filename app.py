import streamlit as st
from PIL import Image
import io
from ocr import perform_ocr
from firestore_utils import fetch_medication_names, fetch_medication_info, upload_to_bucket, translate_text
import os
import uuid
from google.cloud import secretmanager
import json

# Function to fetch and set Google Cloud credentials from Secret Manager
def set_google_credentials_from_secret(secret_id, project_id):
    """
    Fetches the service account key from Google Secret Manager and sets it as GOOGLE_APPLICATION_CREDENTIALS.
    """
    # Create the Secret Manager client
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret
    secret_name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"

    # Access the secret
    response = client.access_secret_version(request={"name": secret_name})
    secret_payload = response.payload.data.decode("UTF-8")
    return secret_payload

    # Save the key.json content to a temporary file
    temp_key_path = "temp_key.json"
    with open(temp_key_path, "w") as key_file:
        key_file.write(secret_payload)
    
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable to the temporary file
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_key_path

# Replace these with your project ID and secret name
PROJECT_ID = "civic-radio-443515-c6"  # actual Google Cloud project ID
SECRET_ID = "service-account-key1"  # name of the secret in Secret Manager

# Call the function to set credentials from Secret Manager
set_google_credentials_from_secret(SECRET_ID, PROJECT_ID)

# Function to process the image
def process_image(image):
    progress = st.progress(0)  # Initialize progress bar
    
    # Save the image temporarily to process it
    image_path = "temp_image.jpg"
    image.save(image_path)
    print(f"Image saved at {image_path}")  # Log the saved image path

    # Upload the image to the Google Cloud Storage bucket
    bucket_name = "temp-prescriptions-bucket"  # Replace with your bucket name
    destination_blob_name = f"uploaded_images/{uuid.uuid4()}.jpg"  # Adjust folder structure if needed
    progress.progress(25)  # Update to 25%
    try:
        print(f"Uploading to bucket {bucket_name} as {destination_blob_name}")
        upload_to_bucket(bucket_name, image_path, destination_blob_name)
        print("Upload completed successfully!")
    except Exception as e:
        print(f"Upload failed: {e}")
        st.error("Failed to upload the image to Google Cloud Storage.")
        return {}

    # Perform OCR to extract text
    progress.progress(50)  # Update to 50%
    extracted_text = perform_ocr(image_path)
    if not extracted_text:
        st.warning("No text was extracted from the image.")
        return {}

    # Fetch medication names from Firestore
    progress.progress(75)  # Update to 75%
    medication_names = fetch_medication_names()
    if not medication_names:
        st.warning("No medication names were fetched from Firestore.")
        return {}

    # Match extracted text to medication names (basic matching logic)
    matched_medications = []
    for word in extracted_text.split():
        word = word.capitalize()
        if word in medication_names:
            matched_medications.append(word)

    # Remove duplicates
    matched_medications = list(set(matched_medications))

    # Fetch detailed information for matched medications
    progress.progress(100)
    medication_info = {}
    for medication_name in matched_medications:
        info = fetch_medication_info(medication_name)
        if info:
            medication_info[medication_name] = info

    return medication_info


# Streamlit interface
st.title("💊 Prescription Image Processing 📷")
st.markdown("Upload a prescription image to extract medication details.")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "pdf"])

# Translation Options in Sidebar
st.sidebar.markdown("### Translation Options 🌐")
language_mapping = {
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Chinese": "zh",
    "Arabic": "ar",
    "Hindi": "hi"
}
selected_language = st.sidebar.selectbox("Choose a language for translation:", options=list(language_mapping.keys()))

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width=175)
    
    if st.button("Submit 🚀"):
        with st.spinner("Processing image... ⏳"):
            try:
                medication_info = process_image(image)
                if medication_info:
                    st.success("Image processed successfully! ✅")
                    for medication, info in medication_info.items():
                        st.subheader(f"Details for {medication}")
                        
                        # Translate each field if a language is selected
                        dosage = info.get('dosage', 'N/A')
                        conditions = ', '.join(info.get('conditions', []))
                        side_effects = ', '.join(info.get('side_effects', []))

                        # Apply translation to each field if a language is selected
                        if selected_language:
                            dosage = translate_text(dosage, language_mapping[selected_language])
                            conditions = translate_text(conditions, language_mapping[selected_language])
                            side_effects = translate_text(side_effects, language_mapping[selected_language])

                        st.write(f"**Dosage**: {dosage}")
                        st.write(f"**Conditions**: {conditions}")
                        st.write(f"**Side Effects**: {side_effects}")
                else:
                    st.error("No medications found in the image.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
else:
    st.info("Please upload an image to get started.")


