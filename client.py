from google.cloud import dialogflow
import os
from random import randrange
import json


def detect_intent_texts(project_id, session_id, texts, language_code):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    sesson_path = "Session path: {}\n".format(session)

    text_input = dialogflow.TextInput(
        text=texts, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    answer = response.query_result.query_text
    confidence = (response.query_result.intent.display_name,response.query_result.intent_detection_confidence)
    print("=" * 20)


    if response.webhook_status.message == 'Webhook execution successful':
        message = list(response.query_result.fulfillment_messages.pb)
        message = list(message[0].text.text)
        for i in message:
            print(i + "\n")
        return True
    else:
        print("Response:\t{}\n".format(
            response.query_result.fulfillment_text))
        return False



def load_credentials():
    with open('config.json') as f:
        config = json.load(f)

    project_id = config['project_id']
    language_code = config['language_code']
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config['cred_file']
    return project_id, language_code


def main():
    # Define the auth scopes to request.
    project_id, language_code = load_credentials()
    session_id = randrange(0, 9999)

    finished = False
    step = 0

    while not finished:
        if step == 0:
            detect_intent_texts(project_id, session_id,
                                "hello", language_code)
            step += 1

        next_input = str(user_input())
        finished = detect_intent_texts(project_id, session_id, next_input, language_code)
        step += 1


def user_input():
    question = input("Input:\t\t")
    return question


if __name__ == '__main__':
    main()
