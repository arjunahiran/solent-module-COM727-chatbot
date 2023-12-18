import json
import nltk
import random
import numpy as np

from nltk import tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from keras.models import Sequential
from keras.layers import Dense, Dropout

nltk.download("wordnet")
nltk.download("stopwords")

g_remove_words = ["?", "!", ".", "/", "@", "'s"]
g_stop_words = set(stopwords.words("english"))


def remove_unwanted_words(words, words_to_remove):
    """
    Remove unwanted words from words that are found in words_to_remove.
    """
    cleaned = [word for word in words if word not in words_to_remove]
    return cleaned


def tokenize_and_clean(question):
    """
    Tokenize the given question into words and apply filters to clean them.
    """
    # tokenize the question into words
    question_words = tokenize.word_tokenize(question)

    # convert to lower
    question_words = [word.lower() for word in question_words]

    # lemmatize words
    lemmatizer = WordNetLemmatizer()
    question_words = [lemmatizer.lemmatize(word) for word in question_words]

    # remove unwanted letters, words and stop words
    question_words = remove_unwanted_words(question_words, g_remove_words)
    question_words = remove_unwanted_words(question_words, g_stop_words)

    return question_words


def read_intents(file_path):
    """
    Read an intent file in JSON format and organize data into words, tags,
    questions and a dictionary of responses keyed with tags.
    """
    out_words = []
    out_tags = []
    out_questions = []
    out_responses = {}

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

        for intent in data["intents"]:
            in_tag = intent["tag"].lower()
            in_questions = intent["questions"]
            in_responses = intent["responses"]

            # add tag to the tags list
            out_tags.append(in_tag)

            # add response to the dictionary with tag as the key
            out_responses[in_tag] = in_responses

            for question in in_questions:
                question_words = tokenize_and_clean(question)

                # add words to question list with the tag. skip empty questions
                if len(question_words) > 0 or in_tag == "default":
                    out_questions.append([question_words, in_tag])

                # add words to the overall words list
                out_words.extend(question_words)

    # sort data
    out_words = sorted(set(out_words))
    out_tags = sorted(set(out_tags))
    out_questions = sorted(out_questions)

    return out_words, out_tags, out_questions, out_responses


def generate_training_data(words, tags, questions):
    """
    Generate training data for each question.
    """
    training_data = []

    # empty class labels
    y_empty = [0] * len(tags)

    for row in questions:
        question, tag = (row[0], row[1])

        # generate x data for each question
        x_data = []

        for word in words:
            x_data.append(1) if word in question else x_data.append(0)

        # generate y data for each question
        y_data = list(y_empty)
        y_data[tags.index(tag)] = 1

        training_data.append([x_data, y_data])

    return training_data


def train_chatbot_model(training_data, epochs):
    """
    Train the chatbot model using the given tranning data and
    returns the History object returned by the model fit function.
    """
    # randomly shuffle training data
    random.shuffle(training_data)
    training_data = np.array(training_data, dtype=object)

    x_train = list(training_data[:, 0])
    y_train = list(training_data[:, 1])

    # create the training model
    model = Sequential()
    model.add(Dense(128, input_shape=(len(x_train[0]),), activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(len(y_train[0]), activation="softmax"))

    model.compile(
        loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"]
    )

    # train the model
    history = model.fit(
        np.array(x_train), np.array(y_train), epochs=epochs, batch_size=5, verbose=1
    )

    return history
