import streamlit as st
from PIL import Image
import io
from ocr import perform_ocr
from firestore_utils import fetch_medication_names, fetch_medication_info, upload_to_bucket

# Function to process the image
def process_image(image):
    progress = st.progress(0)  # Initialize progress bar
    
    # Save the image temporarily to process it
    image_path = "temp_image.jpg"
    image.save(image_path)

    # Upload the image to the Google Cloud Storage bucket
    bucket_name = "temp-prescriptions-bucket"  # Replace with your bucket name
    destination_blob_name = f"uploaded_images/{image.filename}"  # Adjust folder structure if needed
    progress.progress(25)  # Update to 25%
    upload_to_bucket(bucket_name, image_path, destination_blob_name)

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

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    if st.button("Submit 🚀"):
        with st.spinner("Processing image... ⏳"):
            try:
                medication_info = process_image(image)
                if medication_info:
                    st.success("Image processed successfully! ✅")
                    for medication, info in medication_info.items():
                        st.subheader(f"Details for {medication}")
                        st.write(f"**Dosage**: {info.get('dosage', 'N/A')}")
                        st.write(f"**Conditions**: {', '.join(info.get('conditions', []))}")
                        st.write(f"**Side Effects**: {', '.join(info.get('side_effects', []))}")
                else:
                    st.error("No medications found in the image.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
else:
    st.info("Please upload an image to get started.")
