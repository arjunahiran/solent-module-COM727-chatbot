import pickle
import utils
import numpy as np

from keras.models import load_model


def run():
    out_dir = "model"

    words = pickle.load(open(f"{out_dir}/words.pkl", "rb"))
    tags = pickle.load(open(f"{out_dir}/tags.pkl", "rb"))
    responses = pickle.load(open(f"{out_dir}/responses.pkl", "rb"))
    model = load_model(f"{out_dir}/chatbot_model.keras")

    tag = utils.predict_tag("morning", words, tags, model)
    response = utils.generate_response(tag, responses)
    print(response)


if __name__ == "__main__":
    run()
