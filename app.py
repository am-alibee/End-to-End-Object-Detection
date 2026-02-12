import os
import shutil
import subprocess
from flask import Flask, request, jsonify, render_template, Response
from flask_cors import CORS, cross_origin

from signLanguage.pipeline.training_pipeline import TrainPipeline
from signLanguage.logger import logging
from signLanguage.utils import decodeImage, encodeImageIntoBase64

import pathlib
import platform

if platform.system() == "Windows":
    pathlib.PosixPath = pathlib.WindowsPath


app = Flask(__name__)
CORS(app)

class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"

clApp = ClientApp()

# ---------- Home route ---------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/train")
def trainRoute():
    try:
        obj = TrainPipeline()
        obj.run_pipeline()
        return "Training Successful!"
    except Exception as e:
        logging.exception(e)
        return Response("Training Failed")

@app.route("/predict", methods=["POST"])
@app.route("/predict/", methods=["POST"])
@cross_origin()
def predictRoute():
    try:
        image = request.json["image"]
        decodeImage(image, clApp.filename)

        # -------------------------
        # Find latest artifact folder
        # -------------------------
        artifact_dir = "artifacts"
        latest_folder = sorted(os.listdir(artifact_dir))[-1]

        # Build weights path
        weights_path = os.path.join(
            artifact_dir,
            latest_folder,
            "model_trainer",
            "best.pt"
        )

        # -------------------------
        # Run YOLO detection ------
        # -------------------------
        command = (
            "python", 
            "yolov5/detect.py",
            "--weights", weights_path,
            "--img", "416",
            "--conf", "0.01",
            "--source", "data/inputImage.jpg",
            "--exist-ok"
        )

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            logging.info(result.stderr)
            return Response("Detection Failed")

        # -------------------------
        # Encode output image
        # -------------------------
        output_image_path = "yolov5/runs/detect/exp/inputImage.jpg"
        opencodedbase64 = encodeImageIntoBase64(output_image_path)

        # Cleanup
        shutil.rmtree("yolov5/runs", ignore_errors=True)

        return jsonify({"image": opencodedbase64.decode("utf-8")})

    except KeyError:
        return Response("Key error: 'image' key not found in JSON")

    except Exception as e:
        logging.exception(e)
        return Response("Invalid Input")
    
@app.route("/live", methods=["GET"])
@cross_origin()
def predictLive():
    try:

        # Find latest artifact folder
        # -------------------------
        artifact_dir = "artifacts"
        latest_folder = sorted(os.listdir(artifact_dir))[-1]

        weights_path = os.path.join(
            artifact_dir,
            latest_folder,
            "model_trainer",
            "best.pt"
        )

        command = [
            "python", 
            "yolov5/detect.py",
            "--weights", weights_path,
            "--img", "416",
            "--conf", "0.01",
            "--source", "0",
            "--exist-ok"
        ]

        subprocess.run(command)
        return "Camera Starting"
    
    except Exception as e:
        print(e)
        return Response("Value not found inside json data")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
