try:
    from features_default.date_time import date_time
    from features_default.joke import joke
    from features_default.launch_app import launch_app
    from features_default.news import news
    from features_default.tell_me_about import tell_me_about
    from features_default.weather import weather
    from features_default.website_open import website_open
except ImportError as e:
    # print("ImportError: {}".format(e))

    from AdonisAI.features.date_time import date_time
    from AdonisAI.features.joke import joke
    from AdonisAI.features.launch_app import launch_app
    from AdonisAI.features.news import news
    from AdonisAI.features.tell_me_about import tell_me_about
    from AdonisAI.features.weather import weather
    from AdonisAI.features.website_open import website_open

dict_of_features = {
    'asking date': date_time.date,
    'asking time': date_time.time,
    'tell me joke': joke.tell_me_joke,
    'tell me news': news.news,
    'tell me weather': weather.get_weather,
    'tell me about': tell_me_about.tell_me_about,
    'open website': website_open.website_opener,
}
