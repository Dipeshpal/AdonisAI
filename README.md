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

	`pip install AdonisAI`

	It will install all the required package automatically.

- You need only this piece of code-
	```
	# create your own function
	
	# RULES (Optional)-
		# It must contain parameter 'feature_command' (What ever input you provide when AI ask for input will be passed to this function)
		# Return is optional
		# If you want to provide return value it should only return text (str)
	
	def pprint(  
	        feature_command="custom feature (What ever input you provide when AI ask for input will be passed to this function)"):  
	 
	    # write your code here to do something with the command  
	    # perform some tasks 
	    # return is optional  
	    return feature_command + ' Executed'  
	  
	obj = AdonisEngine(bot_name='alexa',  
					   input_mechanism=InputOutput.speech_to_text_ai,  
					   output_mechanism=[InputOutput.text_output, InputOutput.text_to_speech],  
					   backend_tts_api='pyttsx3',  
					   wake_word_detection_status=True,  
					   wake_word_detection_mechanism=InputOutput.speech_to_text_ai,  
					   shutdown_command='shutdown')  
	
	# Check existing list of commands, Existing command you can not use while registering your function
	print(obj.check_registered_command())  
	
	# Register your function (Optional)
	obj.register_feature(feature_obj=pprint, feature_command='custom feature')  
	
	# Start AI in background. It will always run forever until you don't stop it manually.
	obj.engine_start()
	```

	**Whats now?**

	It will start your AI, it will ask you to give input and accordingly it will produce output.
	You can configure `input_mechanism` and `output_mechanism` parameter for voice input/output or text input/output.

	### Parameters-
	
	![enter image description here](https://i.ibb.co/jT3K3H7/raycast-untitled.png)

## 4.  What it can do (Features it supports)-

1. Currently it support only english language
2. Supports voice and text input/output.
3. Supports AI based voice input and by using google api voice input.


	### 4.1. Supported Commands-

	![enter image description here](https://i.ibb.co/2kPzTLv/raycast-untitled-3.png)


## 5. Future

**WIP**

# Connect me-

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
