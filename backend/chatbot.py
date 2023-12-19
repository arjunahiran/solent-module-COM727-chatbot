import pickle
import utils
import numpy as np

from flask import Flask
from keras.models import load_model

# load the chatbot model
out_dir = "model"

words = pickle.load(open(f"{out_dir}/words.pkl", "rb"))
tags = pickle.load(open(f"{out_dir}/tags.pkl", "rb"))
responses = pickle.load(open(f"{out_dir}/responses.pkl", "rb"))
model = load_model(f"{out_dir}/chatbot_model.keras")

# create a flask api service
app = Flask(__name__)


@app.route("/api/<question>")
def chatbot_api(question):
    """
    Chatbot api service. Service is available at http://127.0.0.1:5000/api/<question>
    for example:

    http://127.0.0.1:5000/api/good%20morning
    """

    # predict a tag for the given question
    tag = utils.predict_tag(question, words, tags, model)

    # generate the response for the predicted tag
    response = utils.generate_response(tag, responses)

    return {
        "question": question,
        "response": response,
    }
