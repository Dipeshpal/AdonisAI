import requests
import json


def make_decision(string, classes, multiclass=True):
    url = "https://adonis-ai.herokuapp.com/zero_shot/?secret_key=secret_key"

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


# if __name__ == "__main__":
#     make_decision("string", "class1, class2", multiclass=True)
