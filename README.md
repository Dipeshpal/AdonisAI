# Adonis

1. What is Adonis?
2.  Prerequisite
3.  Getting Started- How to use it?
4. What it can do (Features it supports)
5.  Future?

## 1. What is Adonis?

Adonis is a Python Module which is able to perform task like Chatbot, Assistant etc. It provides base functionality for any assistant application. This JarvisAI is built using Tensorflow, Pytorch, Transformers and other opensource libraries and frameworks. Well, you can contribute on this project to make it more powerful.

This project is crated only for those who is having interest in building Virtual Assistant. Generally it took lots of time to write code from scratch to build Virtual Assistant. So, I have build an Library called "Adonis", which gives you easy functionality to build your own Virtual Assistant.

**This AI is more powerful and light weight version of https://pypi.org/project/JarvisAI/**

## 2.  Prerequisite

-   To use it only Python (> 3.6) is required.

-   To contribute in project: Python is the only prerequisite for basic scripting, Machine Learning and Deep Learning knowledge will help this model to do task like AI-ML. Read How to contribute section of this page.

## 3.  Getting Started- How to use it?

- Install the latest version-

	`pip install JarvisAI`

	It will install all the required package automatically.

- You need only this piece of code-

	```
	import Adonis  
	
	# You can write any custom function you want
	def some_custom_feature():  
	    return "Hello World"  
	  
	# create dictinoary with respected command and function  
	some_custom_feature_dict = {  
	    "hello": some_custom_feature  
	}  
	  
	# object creation of Adonis and Configure some parameter
	obj = Adonis.AdonisEngine(bot_name='alexa',  
		  input_mechanism=Adonis.InputOutput.speech_to_text_ai,  
		  output_mechanism=[Adonis.InputOutput.text_output, Adonis.InputOutput.text_to_speech],  
		  backend_tts_api='pyttsx3',  
		  custom_features=some_custom_feature_dict,  
		  wake_word_detection_status=True,  
		  wake_word_detection_mechanism=Adonis.InputOutput.speech_to_text_google,  
		  shutdown_command='shutdown')  
	
	# Start Adonis Engine
	obj.engine_start()
	```

	**Whats now?**

	It will start your AI, it will ask you to give input and accordingly it will produce output.
	You can configure `input_mechanism` and `output_mechanism` parameter for voice input/output or text input/output.

	### Parameters-
	
	![enter image description here](https://i.ibb.co/xgYD0R0/Snap.png)

## 4.  What it can do (Features it supports)-

1. Currently it support only english language
2. Supports voice and text input/output.
3. Supports AI based voice input and by using google api voice input.
4. Wake word detection.
5. Able to tell you date and time.

	**Read about parameter for more inpormation**

## 5. Future

**WIP**

# Connect Me-

https://www.instagram.com/dipesh_pal17/


# Donate-

[Donate here ](https://www.buymeacoffee.com/dipeshpal)

**_Feel free to use my code, don't forget to mention credit. All the contributors will get credits in this repo._**

**_Mention below line for credits-_**  


Credits goes to-

https://jarvis-ai-api.herokuapp.com/

https://github.com/Dipeshpal/Jarvis_AI/

https://www.youtube.com/dipeshpal17

https://www.instagram.com/dipesh_pal17/
