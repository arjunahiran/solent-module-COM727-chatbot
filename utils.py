import json
import nltk

from nltk import tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def remove_unwanted_words(words, words_to_remove):
    """
    Remove unwanted words from words that are found in words_to_remove.
    """
    cleaned = [word for word in words if word not in words_to_remove]
    return cleaned


def read_intents(file_path):
    """
    Read an intent file in JSON format and organize data into words, tags,
    questions and a dictionary of responses keyed with tags.
    """
    out_words = []
    out_tags = []
    out_questions = []
    out_responses = {}

    nltk.download("wordnet")
    nltk.download("stopwords")

    unwanted_words = ["?", "!", ".", "/", "@", "'s"]
    stop_words = set(stopwords.words("english"))

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
                # tokenize the question into words
                question_words = tokenize.word_tokenize(question)

                # convert to lower
                question_words = [word.lower() for word in question_words]

                # lemmatize words
                lemmatizer = WordNetLemmatizer()
                question_words = [lemmatizer.lemmatize(word) for word in question_words]

                # remove unwanted letters, words and stop words
                question_words = remove_unwanted_words(question_words, unwanted_words)
                question_words = remove_unwanted_words(question_words, stop_words)

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
