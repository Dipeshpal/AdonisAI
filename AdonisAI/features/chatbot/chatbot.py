import requests
import numpy as np
import os


def chatbot(message):
    if not os.path.exists("secret_key.txt"):
        return """Please create a secret_key.txt file with your secret key in it.
        secret key for AdonisAI, it's used for security purpose. 
        Get your free key from "https://adonis-ai.herokuapp.com"
        """
    else:
        with open("secret_key.txt", "r") as f:
            secret_key = f.read()

    if os.path.exists('step.npy'):
        step = str(np.load('step.npy'))
    else:
        step = '0'
    url = f"https://adonis-ai.herokuapp.com/chatbot?secret_key={secret_key}&message={message}&step={step}"
    response = requests.get(url)
    res = response.json()
    status = res['status']

    if status:
        step = int(res['response']['data'][0]['step'])
        np.save('step.npy', step)
        return res['response']['data'][0]['res']
    else:
        return res['response'] + '\n' + "Get a new secret key from https://adonis-ai.herokuapp.com"


if __name__ == "__main__":
    for i in range(7):
        print(chatbot(input("Enter your message: ")))
