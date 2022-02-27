from pprint import pprint

import requests
import textdistance
import json
import os


def make_decision(string, classes, multiclass=True):
    if not os.path.exists("secret_key.txt"):
        return """Please create a secret_key.txt file with your secret key in it.
        secret key for AdonisAI, it's used for security purpose.
        Get your free key from "https://adonis-ai.herokuapp.com"
        """
    else:
        with open("secret_key.txt", "r") as f:
            secret_key = f.read()
    url = f"https://adonis-ai.herokuapp.com/zero_shot/?secret_key={secret_key}"

    payload = json.dumps({
        "string": string,
        "classes": classes,
        "multiple_classes": multiclass
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()


# def make_decision_nlp(string, classes):
#     answer = []
#     answer_ = {}
#     answer_li = []
#     for clas in classes.split(","):
#         acc = textdistance.jaccard(string, clas)
#         answer_li.append({'label': clas, 'confidence': acc})
#         answer.append({'label': clas.strip(), 'confidence': acc})
#         answer_[clas] = acc
#     response = dict()
#     response["data"] = [{'label': max(answer_, key=answer_.get).strip(),
#                          'confidences': answer}]
#     return response


def make_decision_adonis_sentance_similarity(string, classes):
    if not os.path.exists("secret_key.txt"):
        return """Please create a secret_key.txt file with your secret key in it.
           secret key for AdonisAI, it's used for security purpose.
           Get your free key from "https://adonis-ai.herokuapp.com"
           """
    else:
        with open("secret_key.txt", "r") as f:
            secret_key = f.read()
    url = f'https://adonis-ai.herokuapp.com/sentance_similarity?secret_key={secret_key}'

    payload = json.dumps({
        "string": string,
        "classes": classes,
        "multiple_classes": True
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()


if __name__ == "__main__":
    inp = input("Enter your string: ")
    clss = "asking date, asking time, tell me joke, tell me news, tell me weather, tell me about, open website, play on youtube, send whatsapp message, send email"
    # pprint(make_decision(inp, clss, multiclass=True))
    pprint(make_decision_adonis_sentance_similarity(inp, clss))
