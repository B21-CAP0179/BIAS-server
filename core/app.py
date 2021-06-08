import numpy as np
import requests
import urllib
import os
import tensorflow as tf
from PIL import Image
from keras.preprocessing.image import img_to_array
from flask import Flask, jsonify, request
from flask.wrappers import Request, Response
from os import getcwd
from firebase_admin import credentials, firestore, initialize_app

app = Flask(__name__)

# Initialize Firestore DB
KEY_PATH = os.path.join(getcwd(), "core", "key.json")
cred = credentials.Certificate(KEY_PATH)
default_app = initialize_app(cred)
db = firestore.client()
history_ref = db.collection('history')


def get_model(options):
    label = [True, False]
    target_size = (1,1)
    mode = "L"
    
    # Insert option here
    if options == "covid":
        # Model saved with Keras model.save()
        MODEL_PATH = os.path.join(getcwd(), "core", "keras_models", "covid_model.h5")

        # Set label alphanumerically
        label = ['covid', 'normal']
        target_size = (150, 150)
        mode = 'L'

    elif options  == "pneumonia":
        MODEL_PATH = os.path.join(getcwd(), "core", "keras_models", "pneumonia_model.h5")
        label = ['normal', 'pneumonia']
        target_size = (64, 64)
        mode = "RGB"

    # Load your trained model
    model = tf.keras.models.load_model(MODEL_PATH)

    return model, label, target_size, mode

def preprocess_image(image, target_size, mode):
    '''
    color model docs --> https://pillow.readthedocs.io/en/latest/handbook/concepts.html#concept-modes
    '''
    if image.mode != mode:
        image = image.convert(mode)


    image = image.resize(target_size)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    return image

def url_to_image(url):
    return Image.open(requests.get(url, stream=True).raw)

def get_image_from_firestore(request):
    history_id = request.json['id']
    history = history_ref.document(history_id).get().to_dict()

    image = url_to_image(history['image'])
    return image

def get_model_option_from_firestore(request):
    history_id = request.json['id']
    history = history_ref.document(history_id).get().to_dict()

    return history['predictions']

def save_prediction_to_firestore(json):
    history_id = request.json['id']
    history_ref.document(history_id).update(json)

@app.route("/predict", methods=["POST"])
def predict():
    # get and preprocess image from firestore
    image = get_image_from_firestore(request)

    # model prediction
    for option in get_model_option_from_firestore(request):
        model, label, target_size, mode = get_model(option)
        processed_image = preprocess_image(image, target_size, mode)
        prediction = model.predict(processed_image).tolist()

        save_prediction_to_firestore({
            "result" : {
                option : {
                    label[0]: prediction[0][0],
                    label[1]: prediction[0][1]
                }
            },
            "status" : "done"
        })


    return jsonify({"success": True}), 200