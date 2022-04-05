import os
import pprint
import re
import sys
import random
from joblib import Parallel, delayed, parallel_backend
import phonetics
from fuzzywuzzy import fuzz
from playsound import playsound
from download import download
from lazyme.string import color_print as cprint
import shutup

shutup.please()

try:
    from CONSTANT import *
    from services.speech_to_text_google import speech_to_text_google
    from services.text_to_speech import text_to_speech
    from brain_nlu.decision_maker_api import make_decision_adonis_sentance_similarity
    from services.mic_input_ai.mic_input_ai import SpeechRecognition
    from services.asr_deepspeech_streaming.streaming import listen as deepspeech_listen, ARGS, vad_audio, model
    from features_default import dict_of_features, what_can_i_do
except ImportError as e:
    # print("ImportError: {}".format(e))
    from AdonisAI.CONSTANT import *
    from AdonisAI.services.speech_to_text_google import speech_to_text_google
    from AdonisAI.services.text_to_speech import text_to_speech
    from AdonisAI.brain_nlu.decision_maker_api import make_decision_adonis_sentance_similarity
    from AdonisAI.services.mic_input_ai.mic_input_ai import SpeechRecognition
    from AdonisAI.features_default import dict_of_features, what_can_i_do
    from AdonisAI.services.asr_deepspeech_streaming.streaming import listen as deepspeech_listen, ARGS, vad_audio, model


class InputOutput:
    def __init__(self, ARGS, vad_audio, model):
        print("Initializing Engine...")
        self.ARGS = ARGS
        self.vad_audio = vad_audio
        self.model = model

    @staticmethod
    def speech_to_text_deepspeech_streaming(deepspeech_listen_obj, greeting=None, *args, **kwargs):
        if greeting is not None:
            text_to_speech.text_to_speech(text=greeting, backend_tts_api='pyttsx3', lang='en')
        asr_deepspeech_stream = next(deepspeech_listen_obj)
        return asr_deepspeech_stream, None

    @staticmethod
    def speech_to_text_google(greeting=None, *args, **kwargs):
        """
        Convert speech to text using Google Speech to Text API
        :return: command (str), status (bool)
        """
        return speech_to_text_google.speech_to_text_google(greeting=greeting)

    @staticmethod
    def speech_to_text_ai(speech_recognition_ai_obj, greeting=None, *args, **kwargs):
        """
        Convert speech to text using AI
        :return: command (str), None
        """
        return speech_recognition_ai_obj.start_speech_recognition(greeting=greeting)

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
                 backend_tts_api: str, bot_name: str = 'adonis',
                 wake_word_detection_status: bool = True, shutdown_command: str = 'shutdown', secret_key: str = None):
        """
        Engine class for AdonisAI
        :param bot_name: str
        :param input_mechanism: object
            valid values (Either one of below)-
                AdonisAI.InputOutput.speech_to_text_google
                AdonisAI.InputOutput.speech_to_text_ai
                AdonisAI.InputOutput.text_input
                AdonisAI.InputOutput.speech_to_text_deepspeech_streaming
        :param output_mechanism: list of object/objects
            valid values (Either one of below or both)-
                [AdonisAI.InputOutput.text_output]
                [AdonisAI.InputOutput.text_to_speech]
                [AdonisAI.InputOutput.text_output, InputOutput.text_to_speech]
        :param wake_word_detection_mechanism: object
            valid values (Either one of below)-
                AdonisAI.InputOutput.speech_to_text_google
                AdonisAI.InputOutput.speech_to_text_ai
                AdonisAI.InputOutput.speech_to_text_deepspeech_streaming
        :param backend_tts_api: str
            valid values (Either one of below)-
                'pyttsx3'
                'gtts'
        :param wake_word_detection_status: bool
            True / False
        :param shutdown_command: str
            shutdown command
        :param secret_key: str
            Secret key for AdonisAI, it's used for security purpose. Get your free key from "https://adonis-ai.herokuapp.com"
        """
        self.ARGS = ARGS
        self.vad_audio = vad_audio
        self.model = model
        self.deepspeech_listen_obj = deepspeech_listen(ARGS, vad_audio, model)

        super().__init__(self.ARGS, self.vad_audio, self.model)
        self.speech_recognition_ai_obj = SpeechRecognition()
        self.bot_name = bot_name
        self.input_mechanism = input_mechanism
        self.output_mechanism = output_mechanism
        self.backend_tts_api = backend_tts_api
        self.custom_features = {}
        self.wake_word_detection_status = wake_word_detection_status
        self.shutdown_command = shutdown_command
        self.wake_word_detection_mechanism = wake_word_detection_mechanism
        self.validate_combination()

        if not os.path.exists("secret_key.txt"):
            with open("secret_key.txt", "w") as f:
                f.write(secret_key)
        else:
            with open("secret_key.txt", "w+") as f:
                self.old_secret_key = f.read()
                if self.old_secret_key != secret_key:
                    f.write(secret_key)


    def validate_combination(self):
        """
        Validate combination of input and output mechanism
        :return: bool
        """
        if self.backend_tts_api not in ['pyttsx3', 'gtts']:
            raise ValueError("Invalid backend_tts_api type. Expected one of: %s" % ['pyttsx3', 'gtts'])
        if self.wake_word_detection_status:
            if self.wake_word_detection_mechanism not in [InputOutput.speech_to_text_google,
                                                          InputOutput.speech_to_text_ai,
                                                          InputOutput.speech_to_text_deepspeech_streaming]:
                raise ValueError("Invalid wake_word_detection_mechanism type. Expected one of: %s" % [
                    'Adonis.InputOutput.speech_to_text_google',
                    'Adonis.InputOutput.speech_to_text_ai',
                    'Adonis.InputOutput.speech_to_text_deepspeech_streaming'])

        if self.input_mechanism not in [InputOutput.speech_to_text_google,
                                        InputOutput.speech_to_text_ai,
                                        InputOutput.text_input,
                                        InputOutput.speech_to_text_deepspeech_streaming]:
            raise ValueError("Invalid input_mechanism type. Expected one of: %s" % [
                'Adonis.InputOutput.speech_to_text_google',
                'Adonis.InputOutput.speech_to_text_ai',
                'Adonis.InputOutput.text_input',
                'Adonis.InputOutput.speech_to_text_deepspeech_streaming'])
        for _ in self.output_mechanism:
            if _ not in [InputOutput.text_output, InputOutput.text_to_speech]:
                raise ValueError("Invalid output_mechanism type. Expected one of: %s" % [
                    'Adonis.InputOutput.text_output', 'Adonis.InputOutput.text_to_speech'])

    @staticmethod
    def check_registered_command():
        """
        Check if registered command list
        :return: list
        """
        return list(dict_of_features.keys())

    def register_feature(self, feature_obj: object, feature_command: str):
        if feature_command in list(dict_of_features.keys()):
            raise ValueError(f"Feature command '{feature_command}' already registered. Change the command name.")
        dict_temp = {
            feature_command: feature_obj
        }
        self.custom_features.update(dict_temp)
        dict_of_features.update(self.custom_features)

    def features_lookup(self, feature_command: str):
        """
        Create features
        :return: object
        """
        return dict_of_features.get(feature_command, None)

    def play_wake_up_sound(self):
        if not os.path.exists('wake_up.wav'):
            path = download('https://github.com/Dipeshpal/AdonisAI/raw/main/AdonisAI/utils/wake_up.wav',
                            'wake_up.wav', progressbar=True)
        playsound('wake_up.wav')

    def manage_tasks(self):
        try:
            # get input from user according to the input mechanism
            inp = self.input_mechanism(speech_recognition_ai_obj=self.speech_recognition_ai_obj,
                                       deepspeech_listen_obj=self.deepspeech_listen_obj,
                                       greeting='Waiting for your command-')
            print('You said (Command): ', inp[0] if inp is not None else None)
            if inp[0] is None:
                return None, 'No input detected.'
            else:
                inp = inp[0]

            if re.search('what can you do', inp, re.IGNORECASE) is not None:
                pprint.pprint(what_can_i_do)
                li = '\n'.join(list(what_can_i_do.keys()))
                call_out = 'You can say the following commands: ' + li
            else:
                # find action according to input
                # if self.custom_features is None:
                des = make_decision_adonis_sentance_similarity(inp, ','.join(dict_of_features.keys()))
                pred_class, acc = des['data'][0]['label'], des['data'][0]['confidences'][0]['confidence']
                action = self.features_lookup(pred_class.lower())

                # perform action
                if action is not None:
                    call_out = action(inp)
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
            print(e)
            return False, e

    def run(self):
        while True:
            if self.wake_word_detection_status:
                print("Listening for wake word...")
                wake_word, _ = self.wake_word_detection_mechanism(
                    speech_recognition_ai_obj=self.speech_recognition_ai_obj,
                    deepspeech_listen_obj=self.deepspeech_listen_obj)
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
    # RULES (Optional)-
    # It must contain parameter 'feature_command' \
    # (What ever input you provide when AI ask for input will be passed to this function)
    # Return is optional
    # If you want to provide return value it should only return text (str)

    def pprint(
            feature_command="custom feature (What ever input you provide when AI ask for input\
             will be passed to this function)"):
        # write your code here to do something with the command
        # perform some tasks
        # return is optional
        return feature_command + ' Executed'


    obj = AdonisEngine(bot_name='alexa',
                       input_mechanism=InputOutput.speech_to_text_deepspeech_streaming,
                       output_mechanism=[InputOutput.text_output, InputOutput.text_to_speech],
                       backend_tts_api='pyttsx3',
                       wake_word_detection_status=True,
                       wake_word_detection_mechanism=InputOutput.speech_to_text_deepspeech_streaming,
                       shutdown_command='shutdown',
                       secret_key="Secret key for AdonisAI, it's used for security purpose. Get your free key from https://adonis-ai.herokuapp.com")
    # Check existing list of commands, Existing command you can not use while registering your function
    print(obj.check_registered_command())

    # Register your function (Optional)
    obj.register_feature(feature_obj=pprint, feature_command='custom feature')

    # Start AI in background. It will always run forever until you don't stop it manually.
    obj.engine_start()
