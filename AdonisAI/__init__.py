import os
import sys
import random
from joblib import Parallel, delayed, parallel_backend
import phonetics
from fuzzywuzzy import fuzz
import shutup;

shutup.please()
from playsound import playsound
from download import download

try:
    from services.speech_to_text_google import speech_to_text_google
    from services.text_to_speech import text_to_speech
    from brain_nlu.decision_maker_api import make_decision
    from services.mic_input_ai import mic_input_ai
    from features.date_time import date_time
    from features.joke import joke
    from features.launch_app import launch_app
    from features.news import news
    from features.tell_me_about import tell_me_about
    from features.weather import weather
    from features.website_open import website_open
except:
    from AdonisAI.services.speech_to_text_google import speech_to_text_google
    from AdonisAI.services.text_to_speech import text_to_speech
    from AdonisAI.brain_nlu.decision_maker_api import make_decision
    from AdonisAI.services.mic_input_ai import mic_input_ai
    from AdonisAI.features.date_time import date_time
    from AdonisAI.features.date_time import date_time
    from AdonisAI.features.joke import joke
    from AdonisAI.features.launch_app import launch_app
    from AdonisAI.features.news import news
    from AdonisAI.features.tell_me_about import tell_me_about
    from AdonisAI.features.weather import weather
    from AdonisAI.features.website_open import website_open


class InputOutput:
    def __init__(self):
        self.mic_input_ai = mic_input_ai.SpeechRecognition()

    @staticmethod
    def speech_to_text_google(greeting=random.choice(["Hello", "Hi"]) + ',' + ' How may I help you?'):
        """
        Convert speech to text using Google Speech to Text API
        :return: command (str), status (bool)
        """
        return speech_to_text_google.speech_to_text_google(greeting=greeting)

    def speech_to_text_ai(self):
        return self.mic_input_ai.start_speech_recognition()

    @staticmethod
    def text_to_speech(text, lang='en', backend_tts_api='pyttsx3'):
        """
        Convert any text to speech
        You can use GTTS or PYTTSX3 as backend for Text to Speech.
        PYTTSX3 may support different voices (male/female) depends upon your system.
        You can set backend of tts while creating object of JarvisAI class. Default is PYTTSX3.
        :param text: str
            text (String)
        :param lang: str
            default 'en'
        :return: bool
            True / False (Play sound if True otherwise write exception to log and return False)
        """
        backends = ['pyttsx3', 'gtts']
        if backend_tts_api not in backends:
            raise ValueError("Invalid backend_tts_api type. Expected one of: %s" % backends)
        return text_to_speech.text_to_speech(backend_tts_api, text, lang)

    @staticmethod
    def text_input(prompt="Enter your command: "):
        """
        Get text input from user
        :param prompt: str
        :return: str
        """
        text = input(prompt)
        return text, True

    @staticmethod
    def text_output(text):
        print(text)
        return True


class AdonisEngine(InputOutput):
    def __init__(self, input_mechanism: object, output_mechanism: list, wake_word_detection_mechanism: object,
                 backend_tts_api: str, custom_features: dict = None, bot_name='adonis', wake_word_detection_status=True,
                 shutdown_command='shutdown'):
        """
        Engine class for AdonisAI
        :param bot_name: str
        :param input_mechanism: object
            valid values (Either one of below)-
                AdonisAI.InputOutput.speech_to_text_google
                AdonisAI.InputOutput.speech_to_text_ai
                AdonisAI.InputOutput.text_input
        :param output_mechanism: object
            valid values (Either one of below or both)-
                [AdonisAI.InputOutput.text_output]
                [AdonisAI.InputOutput.text_to_speech]
                [AdonisAI.InputOutput.text_output, InputOutput.text_to_speech]
        :param wake_word_detection_mechanism: object
            valid values (Either one of below)-
                AdonisAI.InputOutput.speech_to_text_google
                AdonisAI.InputOutput.speech_to_text_ai
        :param backend_tts_api: str
            valid values (Either one of below)-
                'pyttsx3'
                'gtts'
        :param custom_features: dict
        :param wake_word_detection: bool
        """
        super().__init__()
        self.bot_name = bot_name
        self.input_mechanism = input_mechanism
        self.output_mechanism = output_mechanism
        self.backend_tts_api = backend_tts_api
        self.custom_features = custom_features
        self.wake_word_detection_status = wake_word_detection_status
        self.shutdown_command = shutdown_command
        self.wake_word_detection_mechanism = wake_word_detection_mechanism

    def features_lookup(self, feature, inp):
        """
        Create features
        :return: object
        """
        dict_of_features = {
            'asking date': [date_time.date, None],
            'asking time': [date_time.time, None],
            'tell me joke': [joke.tell_me_joke, None],
            'tell me news': [news.news, None],
            'tell me weather': [weather.get_weather, inp],
        }
        if self.custom_features is not None:
            if self.custom_features.get(feature, None) is not None:
                return self.custom_features.get(feature)
            else:
                return dict_of_features.get(feature, None)
        return dict_of_features.get(feature, None)

    def run(self):
        if self.input_mechanism == InputOutput.speech_to_text_ai:
            inp = self.speech_to_text_ai()
        elif self.input_mechanism == InputOutput.speech_to_text_google:
            inp = self.speech_to_text_google()[0]
        else:
            inp = self.input_mechanism()[0]
        if self.custom_features is None:
            des = make_decision(inp, ','.join(['asking date', 'asking time', 'out of scope', 'greetings']),
                                multiclass=True)
            pred_class, acc = des['data'][0]['label'], des['data'][0]['confidences'][0]['confidence']
            action = self.features_lookup(pred_class.lower(), inp)
        else:
            action = self.features_lookup(inp, inp)
            if action is None and inp is not None and len(inp):
                des = make_decision(inp, ','.join(['asking date', 'asking time', 'out of scope', 'greetings',
                                                   'tell me weather', 'tell me joke', 'tell me news']),
                                    multiclass=True)
                pred_class, acc = des['data'][0]['label'], des['data'][0]['confidences'][0]['confidence']
                action = self.features_lookup(pred_class.lower(), inp)

        if action is not None:
            if action[1] is not None:
                call_out = action[0](inp)
            else:
                call_out = action[0]()
        else:
            print("You Said: %s" % inp)
            call_out = "Sorry, I don't understand your command."

        for output in self.output_mechanism:
            if call_out is not None:
                if output == InputOutput.text_to_speech:
                    output(call_out, lang='en', backend_tts_api=self.backend_tts_api)
                else:
                    output(call_out)

    def wake_word_detection(self):
        """
        Python multi-threading function to run AdonisAI Engine forever
        :return: None
        """

        def play_wake_up_sound():
            if not os.path.exists('wake_up.wav'):
                path = download('https://github.com/Dipeshpal/AdonisAI/raw/main/AdonisAI/utils/wake_up.wav',
                                'wake_up.wav', progressbar=True)
            playsound('wake_up.mp3')

        while True:
            print("Listening for wake word...")
            if self.wake_word_detection_mechanism == InputOutput.speech_to_text_google:
                text = self.speech_to_text_google(greeting=None)[0]
                if text is None:
                    text = ''
            else:
                text = self.mic_input_ai.start_speech_recognition()
            code1 = phonetics.metaphone(text)
            code2 = phonetics.metaphone(self.bot_name)
            accuracy = fuzz.ratio(code1, code2)
            print("You Said: %s" % text)
            if accuracy > 50:
                print("Wake word detected...")
                play_wake_up_sound()
                Parallel(n_jobs=1)([delayed(self.run)()])

            code1 = phonetics.metaphone(text)
            code2 = phonetics.metaphone('stop')
            accuracy = fuzz.ratio(code1, code2)
            if accuracy > 50:
                print("Stop word detected...")
                print(f"{self.bot_name} Engine stopping...")
                sys.exit()

    def engine_start(self):
        if self.wake_word_detection:
            Parallel(n_jobs=1)([delayed(self.wake_word_detection)()])
        else:
            Parallel(n_jobs=1)([delayed(self.run)()])


if __name__ == '__main__':
    def pprint():
        return None


    di = {
        "hello": [pprint, None]
    }
    obj = AdonisEngine(bot_name='alexa',
                       input_mechanism=InputOutput.speech_to_text_ai,
                       output_mechanism=[InputOutput.text_output, InputOutput.text_to_speech],
                       backend_tts_api='pyttsx3',
                       custom_features=di,
                       wake_word_detection_status=True,
                       wake_word_detection_mechanism=InputOutput.speech_to_text_google,
                       shutdown_command='shutdown')
    obj.engine_start()
