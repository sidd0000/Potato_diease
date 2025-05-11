from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
import socket

# Get local IP
def get_local_ip():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

LOCAL_IP = get_local_ip()

# FastAPI App
app = FastAPI()

# Allow CORS for Expo (React Native) and local frontend
origins = [
    f"http://10.12.36.162:8081",  # Expo
    f"http://10.12.36.162:8000",  # API running locally
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model
MODEL = tf.keras.models.load_model("./potatoes.h5", compile=False)

# Ensure it's compiled correctly
MODEL.compile(
    optimizer="adam",
    loss=tf.keras.losses.CategoricalCrossentropy(reduction="sum_over_batch_size"),
    metrics=["accuracy"]
)

# Class labels
CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]

@app.get("/ping")
async def ping():
    return {"message": "Hello, I am alive"}

def read_file_as_image(data) -> np.ndarray:
    """Convert uploaded file to a NumPy array"""
    image = Image.open(BytesIO(data)).convert("RGB")
    image = image.resize((256, 256))
    image = np.array(image) / 255.0
    return image

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """Process image and return prediction"""
    try:
        image = read_file_as_image(await file.read())
        img_batch = np.expand_dims(image, axis=0)
        predictions = MODEL.predict(img_batch)

        predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
        confidence = float(np.max(predictions[0]))

        return {"class": predicted_class, "confidence": confidence}

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
