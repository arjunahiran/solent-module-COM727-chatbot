import sys

sys.path.append("../")

from utils import *


def result(passed):
    """
    Print the result of the test.
    """
    print("> Passed") if passed else print("> Failed")


def printfmt(msg, value):
    """
    Print a simple formated string
    """
    print("{0:10} : {1}".format(msg, value))


def test_remove_unwanted_words():
    """
    Test remove_unwanted_words function.
    """
    print(f"### {test_remove_unwanted_words.__name__}:")

    word_list = ["hi", "hello", "man", "gate", "book"]
    word_list_to_remove = ["hi", "man", "book"]
    word_list_exp = ["hello", "gate"]

    output = remove_unwanted_words(word_list, word_list_to_remove)

    printfmt("Expected", word_list_exp)
    printfmt("Outcome", output)

    result(output == word_list_exp)


def test_read_intents():
    """
    Test read_intents function.
    """
    print(f"### {test_read_intents.__name__}:")

    file_path = "test_intents.json"

    # test intents file
    test_intents_data = {
        "intents": [
            {
                "tag": "test.greetings",
                "questions": ["Hello", "Hey!", "What's up", "Good morning"],
                "responses": ["Hello!", "Hey!", "What can I do for you?"],
            },
            {
                "tag": "Default",
                "questions": [""],
                "responses": [
                    "Please ask me anything.",
                    "How can I help you?",
                ],
            },
        ]
    }

    # write test intents data to a file
    with open(file_path, "w", encoding="utf-8") as test_file:
        json.dump(test_intents_data, test_file, indent=2)

    words, tags, questions, responses = read_intents(file_path)

    printfmt("Words", words)
    printfmt("Tags", tags)
    printfmt("Questions", questions)
    printfmt("Responses", responses)

    tags_exp = ["default", "test.greetings"]

    result(tags == tags_exp)


def test_generate_training_data():
    """
    Test test_generate_training_data function.
    """
    print(f"### {test_generate_training_data.__name__}:")

    file_path = "test_intents.json"

    # test intents file
    test_intents_data = {
        "intents": [
            {
                "tag": "test.greetings",
                "questions": ["Hello", "Hey!", "What's up", "Good morning"],
                "responses": ["Hello!", "Hey!", "What can I do for you?"],
            },
            {
                "tag": "Default",
                "questions": [""],
                "responses": ["Please ask me anything."],
            },
        ]
    }

    # write test intents data to a file
    with open(file_path, "w", encoding="utf-8") as test_file:
        json.dump(test_intents_data, test_file, indent=2)

    words, tags, questions, responses = read_intents(file_path)

    printfmt("Words", words)
    printfmt("Tags", tags)
    printfmt("Questions", questions)
    printfmt("Responses", responses)

    training_data = generate_training_data(words, tags, questions)

    for data in training_data:
        printfmt("Data", data)

    training_data_exp = [
        [[0, 0, 0, 0], [1, 0]],
        [[1, 0, 0, 1], [0, 1]],
        [[0, 1, 0, 0], [0, 1]],
        [[0, 0, 1, 0], [0, 1]],
    ]

    result(training_data == training_data_exp)


def test_train_chatbot_model():
    """
    Test test_train_chatbot_model function.
    """
    print(f"### {test_train_chatbot_model.__name__}:")

    training_data = [
        [[0, 0, 0, 0], [1, 0]],
        [[1, 0, 0, 1], [0, 1]],
        [[0, 1, 0, 0], [0, 1]],
        [[0, 0, 1, 0], [0, 1]],
    ]

    model, _ = train_chatbot_model(training_data, epochs=10)

    result(model != None)


def test_predict_tag():
    """
    Test test_predict_tag function.
    """
    print(f"### {test_predict_tag.__name__}:")

    file_path = "test_intents.json"

    # test intents file
    test_intents_data = {
        "intents": [
            {
                "tag": "test.greetings",
                "questions": ["Hello", "Hey!", "What's up", "Good morning"],
                "responses": ["Hello!", "Hey!", "What can I do for you?"],
            },
            {
                "tag": "Default",
                "questions": [""],
                "responses": ["Please ask me anything."],
            },
        ]
    }

    # write test intents data to a file
    with open(file_path, "w", encoding="utf-8") as test_file:
        json.dump(test_intents_data, test_file, indent=2)

    # read the intents file
    words, tags, questions, responses = read_intents(file_path)

    # train the model
    training_data = generate_training_data(words, tags, questions)
    model, _ = train_chatbot_model(training_data, epochs=10)

    tag = predict_tag("morning", words, tags, model)

    result(tag == "test.greetings")


def test_generate_response():
    """
    Test test_generate_response function.
    """
    print(f"### {test_generate_response.__name__}:")

    responses = {
        "test.greetings": ["Hello!", "Hey!", "What can I do for you?"],
        "default": ["Please ask me anything."],
    }

    response = generate_response("test.greetings", responses)
    printfmt("Response", response)

    result(
        response == "Hello!"
        or response == "Hey!"
        or response == "What can I do for you?"
    )


def test():
    """
    Test all functions.
    """
    print(f"{' Testing: START ':=^30}")
    test_remove_unwanted_words()
    test_read_intents()
    test_generate_training_data()
    test_train_chatbot_model()
    test_predict_tag()
    test_generate_response()
    print(f"{' Testing: END ':=^30}")


if __name__ == "__main__":
    test()
