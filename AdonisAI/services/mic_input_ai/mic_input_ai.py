# Voice Recognition using https://huggingface.co/facebook/wav2vec2-base-960h
import pyaudio
import wave
import librosa
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
import os
from gtts import gTTS
import pyttsx3
from playsound import playsound
from lazyme.string import color_print as cprint


try:
    import torch
except ImportError:
    cprint("No Pytorch Found, Please install if manually from below link", color='yellow', underline=True, bold=True)
    cprint("https://pytorch.org/get-started/locally/", color='blue', underline=True, bold=True)


class MicRecord:
    def __init__(self):
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.CHUNK = 1024
        self.WAVE_OUTPUT_FILENAME = "temp_record.wav"
        if os.path.exists(self.WAVE_OUTPUT_FILENAME):
            os.remove(self.WAVE_OUTPUT_FILENAME)

    def start_recording(self, record_seconds=5, debug=False, greeting=None):
        audio = pyaudio.PyAudio()
        # start Recording
        stream = audio.open(format=self.FORMAT, channels=self.CHANNELS,
                            rate=self.RATE, input=True,
                            frames_per_buffer=self.CHUNK)
        if greeting is not None:
            print(greeting)
            text_to_speech(greeting, lang='en')
        if debug:
            print("recording...")
        frames = []

        for i in range(0, int(self.RATE / self.CHUNK * record_seconds)):
            data = stream.read(self.CHUNK)
            frames.append(data)
        if debug:
            print("finished recording")

        # stop Recording
        stream.stop_stream()
        stream.close()
        audio.terminate()
        waveFile = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(self.CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(self.FORMAT))
        waveFile.setframerate(self.RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()


class SpeechRecognition(MicRecord):
    def __init__(self):
        super().__init__()
        self.tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
        self.model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

    def start_speech_recognition(self, record_seconds=5, debug=False, greeting=None):
        self.start_recording(record_seconds=record_seconds, debug=debug, greeting=greeting)
        print("Recognizing...")
        input_audio, _ = librosa.load(self.WAVE_OUTPUT_FILENAME, sr=16000)
        input_values = self.tokenizer(input_audio, return_tensors="pt").input_values
        logits = self.model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.tokenizer.batch_decode(predicted_ids)[0]
        os.remove(self.WAVE_OUTPUT_FILENAME)
        # if transcription is not None or :
        #     return transcription.lower(), True
        # else:
        #     return None, False
        return None if transcription.lower() == '' else transcription.lower(), None


def text_to_speech(text, backend_tts_api='pyttsx3', lang='en'):
    """
    Convert any text to speech
    You can use GTTS or PYTTSX3 as backend for Text to Speech.
    PYTTSX3 may support different voices (male/female) depends upon your system.
    You can set backend of tts while creating object of JarvisAI class. Default is PYTTSX3.
    :param backend_tts_api: str
        text (String)
    :param text: str
        text (String)
    :param lang: str
        default 'en'
    :return: Bool
        True / False (Play sound if True otherwise write exception to log and return False)
    """
    if backend_tts_api == 'gtts':
        # for gtts Backend
        try:
            myobj = gTTS(text=text, lang=lang, slow=False)
            myobj.save("tmp.mp3")
            playsound("tmp.mp3")
            os.remove("tmp.mp3")
            return True
        except Exception as e:
            print(e)
            print("or You may reached free limit of 'gtts' API. Use 'pyttsx3' as backend for unlimited use.")
            return False
    else:
        # for pyttsx3 Backend
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')

        try:
            if not os.path.exists("configs"):
                os.mkdir("configs")

            voice_file_name = "configs/Edith-Voice.txt"
            if not os.path.exists(voice_file_name):
                cprint("You can try different voices. This is one time setup. You can reset your voice by deleting"
                       "'configs/Edith-Voice.txt' file in your working directory.",
                       color='blue')
                cprint("Your System Support Following Voices- ",
                       color='blue')
                voices_dict = {}
                for index, voice in enumerate(voices):
                    print(f"{index}: ", voice.id)
                    voices_dict[str(index)] = voice.id
                option = input(f"Choose any- {list(voices_dict.keys())}: ")
                with open(voice_file_name, 'w') as f:
                    f.write(voices_dict.get(option, voices[0].id))
                with open(voice_file_name, 'r') as f:
                    voice_property = f.read()
            else:
                with open(voice_file_name, 'r') as f:
                    voice_property = f.read()
        except Exception as e:
            print(e)
            print("Error occurred while creating config file for voices in pyttsx3 in 'text2speech'.",
                  "Contact maintainer/developer of JarvisAI")
        try:
            engine.setProperty('voice', voice_property)
            engine.say(text)
            engine.runAndWait()
            return True
        except Exception as e:
            print(e)
            print("Error occurred while using pyttsx3 in 'text2speech'.",
                  "or Your system may not support pyttsx3 backend. Use 'gtts' as backend.",
                  "Contact maintainer/developer of JarvisAI.")
            return False


if __name__ == '__main__':
    obj = SpeechRecognition()
    transcription = obj.start_speech_recognition()
    print(transcription)
