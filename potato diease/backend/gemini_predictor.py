import os
import mimetypes
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def predict_leaf_description(image_path: str) -> str:
    """
    Sends the image to Gemini Vision and returns a structured
    response with Status, Orientation, Crop and Disease.
    Supports PNG, JPEG, JPG, etc.
    """
    with open(image_path, "rb") as f:
        img_bytes = f.read()

    # Automatically detect MIME type (e.g., image/png, image/jpeg)
    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError("Unsupported file type or not an image.")

    prompt = (
        "You are a plant pathology expert. Analyze the image and respond "
        "in exactly this format (no extra text):\n"
        
        "Status: Real or Fake\n"
        "Orientation: [e.g. Upright, Upside-down, Tilted]\n"
        "Crop: [Crop name]\n "
        "Possible dieases :['mention the top 5 dieases for this plant crop']\n"
        "Disease: [Disease name or if diease =='none' say 'None' ]\n"
        "also in the last return a contor box on the image where diease is been predicted"
        
    )

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([
        prompt,
        {"mime_type": mime_type, "data": img_bytes}
    ])

    return response.text
