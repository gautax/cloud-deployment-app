from google.cloud import vision

def perform_ocr(image_path):
    """
    Perform OCR on the given image to extract text and identify multiple medication names.
    """
    client = vision.ImageAnnotatorClient()
    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if not texts:
        print("No text found in the image.")
        return []

    # Extract the text from the response
    extracted_text = texts[0].description.strip()
    print(f"Full OCR Output:\n{extracted_text}")

    return extracted_text
