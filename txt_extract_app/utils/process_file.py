from pdf2image import convert_from_path
import pytesseract
import os
from django.conf import settings

def handle_uploaded_file(f, file_name):
    # Set the path to the tesseract executable
    pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_PATH

    path = './pdf-store/'   # Path to store the pdf file temporarily
    if not os.path.exists(path):
        os.makedirs(path)

    path += file_name
    # Write the pdf file to the path
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    # Convert the pdf file to image
    pages = convert_from_path(path, 350)
    text = ''
    for page in pages:
        text += str(pytesseract.image_to_string(page))

    # Delete the pdf file
    os.remove(path)
    return text