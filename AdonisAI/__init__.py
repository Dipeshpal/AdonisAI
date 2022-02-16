import os
import sys
import random
from joblib import Parallel, delayed, parallel_backend
import phonetics
from fuzzywuzzy import fuzz
from playsound import playsound
from download import download
from CONSTANT import *
from lazyme.string import color_print as cprint
import shutup

shutup.please()

try:
    from services.speech_to_text_google import speech_to_text_google
    from services.text_to_speech import text_to_speech
    from brain_nlu.decision_maker_api import make_decision
    from services.mic_input_ai.mic_input_ai import SpeechRecognition
    from features.date_time import date_time
    from features.joke import joke
    from features.launch_app import launch_app
    from features.news import news
    from features.tell_me_about import tell_me_about
    from features.weather import weather
    from features.website_open import website_open
except ImportError as e:
    # print("ImportError: {}".format(e))
    from AdonisAI.services.speech_to_text_google import speech_to_text_google
    from AdonisAI.services.text_to_speech import text_to_speech
    from AdonisAI.brain_nlu.decision_maker_api import make_decision
    from AdonisAI.services.mic_input_ai.mic_input_ai import SpeechRecognition
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
        print("Initializing Engine...")

    @staticmethod
    def speech_to_text_google(greeting=None, *args, **kwargs):
        """
        Convert speech to text using Google Speech to Text API
        :return: command (str), status (bool)
        """
        return speech_to_text_google.speech_to_text_google(greeting=greeting)

    @staticmethod
    def speech_to_text_ai(speech_recognition_ai_obj, *args, **kwargs):
        """
        Convert speech to text using AI
        :return: command (str), None
        """
        return speech_recognition_ai_obj.start_speech_recognition()

    @staticmethod
    def text_to_speech(text, lang='en', backend_tts_api='pyttsx3', *args, **kwargs):
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
    def text_input(prompt="Enter your command: ", *args, **kwargs):
        """
        Get text input from user
        :param prompt: str
        :return: str
        """
        text = input(prompt)
        return text, True

    @staticmethod
    def text_output(text, *args, **kwargs):
        print(text)
        return True


class AdonisEngine(InputOutput, SpeechRecognition):
    def __init__(self, input_mechanism: object, output_mechanism: list, wake_word_detection_mechanism: object,
                 backend_tts_api: str, custom_features: dict = None, bot_name: str = 'adonis',
                 wake_word_detection_status: bool = True, shutdown_command: str = 'shutdown'):
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
        self.speech_recognition_ai_obj = SpeechRecognition()
        self.bot_name = bot_name
        self.input_mechanism = input_mechanism
        self.output_mechanism = output_mechanism
        self.backend_tts_api = backend_tts_api
        self.custom_features = custom_features
        self.wake_word_detection_status = wake_word_detection_status
        self.shutdown_command = shutdown_command
        self.wake_word_detection_mechanism = wake_word_detection_mechanism
        self.validate_combination()

    def validate_combination(self):
        """
        Validate combination of input and output mechanism
        :return: bool
        """
        if self.backend_tts_api not in ['pyttsx3', 'gtts']:
            raise ValueError("Invalid backend_tts_api type. Expected one of: %s" % ['pyttsx3', 'gtts'])
        if self.wake_word_detection_status:
            if self.wake_word_detection_mechanism not in [InputOutput.speech_to_text_google,
                                                          InputOutput.speech_to_text_ai]:
                raise ValueError("Invalid wake_word_detection_mechanism type. Expected one of: %s" % [
                    'Adonis.InputOutput.speech_to_text_google', 'Adonis.InputOutput.speech_to_text_ai'])

        if self.input_mechanism not in [InputOutput.speech_to_text_google, InputOutput.speech_to_text_ai,
                                        InputOutput.text_input]:
            raise ValueError("Invalid input_mechanism type. Expected one of: %s" % [
                'Adonis.InputOutput.speech_to_text_google', 'Adonis.InputOutput.speech_to_text_ai',
                'Adonis.InputOutput.text_input'])
        for _ in self.output_mechanism:
            if _ not in [InputOutput.text_output, InputOutput.text_to_speech]:
                raise ValueError("Invalid output_mechanism type. Expected one of: %s" % [
                    'Adonis.InputOutput.text_output', 'Adonis.InputOutput.text_to_speech'])

    def features_lookup(self, feature, *args, **kwargs):
        """
        Create features
        :return: object
        """
        dict_of_features = {
            'asking date': [date_time.date, args, kwargs],
            'asking time': [date_time.time, args, kwargs],
            'tell me joke': [joke.tell_me_joke, args, kwargs],
            'tell me news': [news.news, args, kwargs],
            'tell me weather': [weather.get_weather, args, kwargs],
        }
        if self.custom_features is not None:
            if self.custom_features.get(feature, None) is not None:
                return self.custom_features.get(feature)
            else:
                return dict_of_features.get(feature, None)
        return dict_of_features.get(feature, None)

    def play_wake_up_sound(self):
        if not os.path.exists('wake_up.wav'):
            path = download('https://github.com/Dipeshpal/AdonisAI/raw/main/AdonisAI/utils/wake_up.wav',
                            'wake_up.wav', progressbar=True)
        playsound('wake_up.wav')

    def manage_tasks(self):
        try:
            # get input from user according to the input mechanism
            inp = self.input_mechanism(speech_recognition_ai_obj=self.speech_recognition_ai_obj)[0]
            print('You said (Command): ', inp[0] if inp is not None else None)
            if inp is None:
                return None, 'No input detected.'

            # find action according to input
            if self.custom_features is None:
                des = make_decision(inp, ','.join(CLASSES),
                                    multiclass=True)
                pred_class, acc = des['data'][0]['label'], des['data'][0]['confidences'][0]['confidence']
                action = self.features_lookup(pred_class.lower(), inp)
            else:
                action = self.features_lookup(inp, inp)
                if action is None and inp is not None and len(inp):
                    des = make_decision(inp, ','.join(CLASSES+list(self.custom_features.keys())), multiclass=True)
                    pred_class, acc = des['data'][0]['label'], des['data'][0]['confidences'][0]['confidence']
                    action = self.features_lookup(pred_class.lower(), inp)

            # perform action
            if action is not None:
                if action[1] is not None:
                    call_out = action[0](action[1], action[2])
                else:
                    call_out = action[0]()
            else:
                call_out = "Sorry, I don't understand your command."

            # call out action result according to the output mechanism
            for output in self.output_mechanism:
                if call_out is not None:
                    if output == InputOutput.text_to_speech:
                        output(text=call_out, lang='en', backend_tts_api=self.backend_tts_api)
                    else:
                        output(call_out)
            return True, 'Task Done'
        except Exception as e:
            return False, e

    def run(self):
        while True:
            if self.wake_word_detection_status:
                print("Listening for wake word...")
                wake_word, _ = self.wake_word_detection_mechanism(speech_recognition_ai_obj=self.speech_recognition_ai_obj)
                print("You Said: %s" % wake_word)
                if wake_word is not None:
                    code1 = phonetics.metaphone(wake_word)
                    code2 = phonetics.metaphone(self.bot_name)
                    accuracy = fuzz.ratio(code1, code2)
                    # print("You Said: %s" % wake_word)
                    if accuracy > 50:
                        print("Wake word detected...")
                        self.play_wake_up_sound()
                        # data = Parallel(n_jobs=1)([delayed(self.manage_tasks)()])
                        data = self.manage_tasks()
                        # print(data)
            else:
                # data = Parallel(n_jobs=1)([delayed(self.manage_tasks)()])
                data = self.manage_tasks()
                # print(data)

    def engine_start(self):
        self.run()


if __name__ == '__main__':
    def pprint(*args, **kwargs):
        return None


    di = {
        # "command": [function, *args, **kwargs],
        "hello": [pprint, None, None]
    }
    obj = AdonisEngine(bot_name='alexa',
                       input_mechanism=InputOutput.speech_to_text_ai,
                       output_mechanism=[InputOutput.text_output, InputOutput.text_to_speech],
                       # output_mechanism=[InputOutput.text_output],
                       backend_tts_api='pyttsx3',
                       custom_features=di,
                       wake_word_detection_status=False,
                       wake_word_detection_mechanism=InputOutput.speech_to_text_ai,
                       shutdown_command='shutdown')
    obj.engine_start()
