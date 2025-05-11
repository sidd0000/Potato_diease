# backend/leaf_utils.py

from PIL import Image
import uuid
import os

def save_image(upload_file):
    """
    Save an incoming Werkzeug FileStorage to disk and return its filepath.
    """
    ext = os.path.splitext(upload_file.filename)[1] or ".png"
    filename = f"{uuid.uuid4()}{ext}"
    folder = "temp_images"
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)

    image = Image.open(upload_file.stream)
    image.save(path)

    return path
