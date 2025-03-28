import { useState } from "react";
import axios from "axios";
import "./ImageUpload.css"; // Ensure you have the corresponding CSS file

const ImageUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) return alert("Please select an image.");

    const formData = new FormData();
    formData.append("file", selectedFile);

    setLoading(true);
    try {
      const { data } = await axios.post("http://localhost:8000/predict", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setPrediction(data);
    } catch (error) {
      alert("Error in prediction. Check console.");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-container">
      <div className="file-input-wrapper">
        <input 
          type="file" 
          id="file-input"
          accept="image/*" 
          onChange={handleFileChange} 
          className="file-input" 
        />
        <label htmlFor="file-input" className="file-label">
          Choose Image
        </label>
        {selectedFile && (
          <div className="selected-file">
            Selected: {selectedFile.name}
          </div>
        )}
      </div>

      <button 
        onClick={handleUpload} 
        className="upload-button"
        disabled={loading}
      >
        {loading ? (
          <span className="loading-dots">Predicting...</span>
        ) : (
          "Upload & Predict"
        )}
      </button>

      {prediction && (
        <div className="result-box">
          <p><strong>Class:</strong> {prediction.class}</p>
          <p><strong>Confidence:</strong> {Math.round(prediction.confidence * 100)}%</p>
        </div>
      )}
    </div>
  );
};

export default ImageUpload;
