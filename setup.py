import setuptools
from setuptools import find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AdonisAI",
    version="1.7",
    author="Dipesh",
    author_email="dipeshpal17@gmail.com",
    description="AdonisAI is python library to build your own AI virtual assistant with natural language processing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dipeshpal/Adonis",
    include_package_data=True,
    packages=find_namespace_packages(include=['AdonisAI.*', 'AdonisAI']),
    install_requires=['pyaudio', 'SpeechRecognition', 'gtts', 'lazyme', 'torch', 'joblib',
                      'phonetics', 'fuzzywuzzy', 'requests', 'librosa', 'transformers', 'lazyme', 'playsound==1.2.2',
                      'pyttsx3', 'python-Levenshtein', 'shutup', 'download', 'pyjokes', 'spacy',
                      'beautifulsoup4==4.9.3', 'wikipedia', 'deepspeech', 'deepspeech-gpu', 'webrtcvad', 'halo',
                      'scipy', 'pywhatkit', 'flask', 'regex', 'numpy', 'textdistance[extras]',
                      'opencv-python==4.5.5.64', 'pyscreenshot==3.0', 'speedtest-cli==2.1.3', 'pytube==12.0.0',
                      'pycountry==22.3.5'],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    project_urls={
        'Documentation': 'https://github.com/Dipeshpal/Jarvis_AI',
        'Donate': 'https://www.buymeacoffee.com/dipeshpal',
        'Say Thanks!': 'https://youtube.com/techportofficial',
        'Source': 'https://github.com/Dipeshpal/Jarvis_AI',
    },
)
