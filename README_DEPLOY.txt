Deployment scaffold generated.

Files created:
 - app.py
 - requirements.txt
 - Dockerfile

Artifacts required (must exist in same dir):
 - anopheles_fnn_model.keras
 - label_encoder.pkl
 - scaler.pkl
 - model_config.json

Quick local test (python environment with dependencies):
  pip install -r requirements.txt
  python app.py
  # then from another shell:
  curl -X POST -F "file=@example.wav" http://127.0.0.1:5000/predict

Build Docker image (if you have Docker installed):
  docker build -t anopheles-api:latest .
  docker run -p 5000:5000 anopheles-api:latest

Suggested cloud deploy:
 - Push Docker image to a registry (Docker Hub / GCR / ECR) then use Cloud Run / Render / AWS ECS / GKE.
 - Or deploy code directly to Heroku by adding a Procfile:
     web: gunicorn app:app --bind 0.0.0.0:$PORT
   and then `git push heroku main` (Heroku python buildpack will install requirements).

Notes:
 - The feature extraction in extract_features_from_wav_bytes is a placeholder using MFCC mean.
   Replace with the identical preprocessing you used during training (windowing, mel, padding, etc).
 - Ensure model_config.json contains keys like "sr" and "n_mfcc" and any other hyperparams your preprocessing needs.