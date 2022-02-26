try:
    from features.date_time import date_time
    from features.joke import joke
    from features.launch_app import launch_app
    from features.news import news
    from features.tell_me_about import tell_me_about
    from features.weather import weather
    from features.website_open import website_open
    from features.youtube_play import youtube_play
    from features.whatsapp_message import whatsapp_message
    from features.send_email import send_email
    from features.chatbot import chatbot
except ImportError as e:
    # print("ImportError: {}".format(e))
    from AdonisAI.features.date_time import date_time
    from AdonisAI.features.joke import joke
    from AdonisAI.features.launch_app import launch_app
    from AdonisAI.features.news import news
    from AdonisAI.features.tell_me_about import tell_me_about
    from AdonisAI.features.weather import weather
    from AdonisAI.features.website_open import website_open
    from AdonisAI.features.youtube_play import youtube_play
    from AdonisAI.features.whatsapp_message import whatsapp_message
    from AdonisAI.features.send_email import send_email
    from AdonisAI.features.chatbot import chatbot

dict_of_features = {
    'asking date': date_time.date,
    'asking time': date_time.time,
    'tell me joke': joke.tell_me_joke,
    'tell me news': news.news,
    'tell me weather': weather.get_weather,
    'tell me about': tell_me_about.tell_me_about,
    'open website': website_open.website_opener,
    'play on youtube': youtube_play.yt_play,
    'send whatsapp message': whatsapp_message.send_whatsapp_message,
    'send email': send_email.send_email,
    'conversation or greetings': chatbot.chatbot
}

what_can_i_do = {
    'you can ask me date ': 'Say- "what is the date today"',
    'you can ask me time ': 'Say- "what is the time now"',
    'you can ask me joke ': 'Say- "tell me a joke"',
    'you can ask me news ': 'Say- "tell me news"',
    'you can ask me weather ': 'Say- "what is the weather", "tell me weather", "tell me about weather",'
                               ' "tell me about weather in <city>"',
    'you can ask me about ': 'Say- "tell me about <topic>"',
    'you can open website ': 'Say- "open website <website name>", "open website <website name><.extension>"'
                             '"open website techport.in"',
    'you can play on youtube ': 'Say- "play on youtube <video name>", "play <video name> on youtube"',
    'you can send whatsapp message ': 'Say- "send whatsapp message',
    'you can send email ': 'Say- "send email',
}

if __name__ == '__main__':
    print(', '.join(list(dict_of_features.keys())))
