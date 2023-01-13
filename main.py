import telebot
import requests


token = input('Введите токен')
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['help'])
def send_greeting_message(message):
    bot.reply_to(message, f'Я погодний бот! Привіт, {message.from_user.first_name}')


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    if message.text.lower() == 'привіт':
        bot.send_message(message.from_user.id, 'Привіт!')
    else:
        city = message.text
        weather_app_id = '1bc2725658a868da54023ace08dc2e54'
        try:
            result = requests.get('http://api.openweathermap.org/data/2.5/find',
                                  params={'q': city,
                                          'type': 'like',
                                          'units': 'metric',
                                          'APPID': weather_app_id})
            data = result.json()
            city_id = data['list'][0]['id']

            result = requests.get('http://api.openweathermap.org/data/2.5/weather',
                                  params={'id': city_id,
                                          'units': 'metric',
                                          'lang': 'ua',
                                          'APPID': weather_app_id})
            data = result.json()
            conditions = data['weather'][0]['description']
            temp = str(data['main']['temp'])
            bot.send_message(message.from_user.id,
                             'Умови: ' + conditions + '\nТемпература: ' + temp)
        except Exception as e:
            print(e)


bot.polling(none_stop=True)
