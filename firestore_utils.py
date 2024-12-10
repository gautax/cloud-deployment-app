from google.cloud import firestore
from google.cloud import storage
from google.cloud import translate_v2 as translate


def fetch_medication_names():
    """
    Fetch all medication names from Firestore.
    """
    db = firestore.Client()
    medications = [doc.to_dict()['name'] for doc in db.collection("medications").stream()]
    return medications

def fetch_medication_info(medication_name):
    """
    Fetch detailed information about a medication from Firestore.
    """
    db = firestore.Client()
    medications_ref = db.collection("medications").where("name", "==", medication_name).stream()
    
    for doc in medications_ref:
        return doc.to_dict()
    
    return None
# Blob Storage

def upload_to_bucket(bucket_name, source_file_name, destination_blob_name):
    """
    Uploads a file to the specified Google Cloud Storage bucket.
    """
    try:
        # Initialize the Google Cloud Storage client
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        # Upload the file
        blob.upload_from_filename(source_file_name)
        print(f"File {source_file_name} uploaded to {destination_blob_name} in bucket {bucket_name}.")
    except Exception as e:
        print(f"An error occurred while uploading to bucket: {e}")
        raise
def translate_text(text, target_language):
    """
    Translates text into the target language.
    """
    try:
        # Initialize the Translation client
        translate_client = translate.Client()

        # Perform translation
        result = translate_client.translate(text, target_language=target_language)
        return result['translatedText']
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        raise
