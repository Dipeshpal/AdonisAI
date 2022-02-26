import requests
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


# if __name__ == "__main__":
#     make_decision("string", "class1, class2", multiclass=True)
