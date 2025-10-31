from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import librosa
import soundfile as sf
import io, pickle, json

# Load model & utilities
MODEL_PATH = "anopheles_fnn_model.keras"
LABEL_PATH = "label_encoder.pkl"
SCALER_PATH = "scaler.pkl"
CONFIG_PATH = "model_config.json"

model = tf.keras.models.load_model(MODEL_PATH)
label_encoder = pickle.load(open(LABEL_PATH, "rb"))
scaler = pickle.load(open(SCALER_PATH, "rb"))
model_config = json.load(open(CONFIG_PATH, "r"))

app = Flask(__name__)

def extract_features_from_wav_bytes(wav_bytes):
    """Extract MFCC features from uploaded WAV."""
    data, sr = sf.read(io.BytesIO(wav_bytes))
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)
    target_sr = model_config.get("sr", 22050)
    if sr != target_sr:
        data = librosa.resample(data, orig_sr=sr, target_sr=target_sr)
    n_mfcc = model_config.get("n_mfcc", 40)
    mfcc = librosa.feature.mfcc(y=data, sr=target_sr, n_mfcc=n_mfcc)
    return np.mean(mfcc, axis=1)

@app.route("/")
def home():
    return jsonify({"status": "API running"})

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    wav_bytes = request.files["file"].read()

    feats = extract_features_from_wav_bytes(wav_bytes)
    x = np.array(feats).reshape(1, -1)
    x = scaler.transform(x)
    preds = model.predict(x)

    idx = int(np.argmax(preds))
    label = label_encoder.inverse_transform([idx])[0]
    score = float(np.max(preds))

    return jsonify({"label": label, "score": round(score, 3)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
