from google.cloud import firestore
from google.cloud import storage

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
    Uploads a file to a Google Cloud Storage bucket.
    :param bucket_name: Name of the bucket.
    :param source_file_name: Local path to the file.
    :param destination_blob_name: The name of the object in the bucket.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(f"File {source_file_name} uploaded to {destination_blob_name}.")
