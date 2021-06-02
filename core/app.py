import base64
import numpy as np
import io
import os
import tensorflow as tf
from PIL import Image
from keras.preprocessing.image import img_to_array
from flask import Flask, jsonify, request
from flask.wrappers import Request, Response
from os import getcwd

app = Flask(__name__)


def get_model(options):
    global model
    # Model saved with Keras model.save()
    if options == "covid":
        MODEL_PATH = os.path.join(getcwd(), "core", "keras_models", "covid_model.h5")

    # Load your trained model
    model = tf.keras.models.load_model(MODEL_PATH)

def preprocess_image(image, target_size):
    if image.mode != 'RGB':
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    return image

@app.route('/')
@app.route('/index')
def index():
    return 'Hello world!'

@app.route("/predict/cxr/covid/", methods=["POST"])
def predict():
    message = request.get_json(force=True)
    encoded = message["image"]
    decoded = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(decoded))
    processed_image = preprocess_image(image, target_size=(150, 150))

    get_model("covid")
    prediction = model.predict(processed_image).tolist()

    response = {
        "prediction": {
            "Covid": prediction[0][0],
            "Normal": prediction[0][1]
        }
    }

    return jsonify(response)