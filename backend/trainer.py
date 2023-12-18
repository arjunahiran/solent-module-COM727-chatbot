import os
import pickle
import utils


def run():
    """
    Run the trainer
    """
    print("Starting the trainer...")

    file_path = "intents.json"

    # read the intent file into words
    print("Reading the intents...")
    words, tags, questions, responses = utils.read_intents(file_path)

    # generate training data
    print("Generating training data...")
    training_data = utils.generate_training_data(words, tags, questions)

    # train the model
    print("Traning the model...")
    model, history = utils.train_chatbot_model(training_data, epochs=200)

    # save the model
    out_dir = "model"

    print("Saving the model...")

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    pickle.dump(words, open(f"{out_dir}/words.pkl", "wb"))
    pickle.dump(tags, open(f"{out_dir}/tags.pkl", "wb"))
    pickle.dump(responses, open(f"{out_dir}/responses.pkl", "wb"))

    model.save(f"{out_dir}/chatbot_model.keras", history)

    print("Training COMPLETE!")


if __name__ == "__main__":
    run()
