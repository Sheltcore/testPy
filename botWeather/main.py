import telebot
#Библиотека реквест позволяет отправлять данные по URL адресу и получать ответ
import requests
import json

#в bot указываем token нашего бота
bot = telebot.TeleBot('7565521168:AAG9NkHxV44m082qxhPWgAkZdSVFN84KT-k')
#в API указываем ключ, который создали на сайте openweathermap
API = '65f09205d56999a07c95333958b7d31b'

#Создаем декоратор, который обрабатывает команду старт
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, рад тебя видеть! Напиши название города')

#Создаем декоратор, который отслеживает отправляемый текст пользователя. (Не видео/картинку, а текст)
@bot.message_handler(content_types=['text'])
def get_weather(message):
    #strip помогает удалить пробелы до и после строки
    city = message.text.strip().lower()
    #В переменную RES присваиваем значение API call с сайта, где добавлены параметры city и API
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    #проверка отправляемого текста. Статус 200 - это всегда успешная обработка URL-страницы
    if res.status_code == 200:
        #Объявляем переменную data, в которую записывается json объект
        data = json.loads(res.text)
        #Извлекаем необходимые значения из JSON объекта
        temp = data['main']['temp']
        tempnin = data['main']['temp_min']
        tempmax = data['main']['temp_max']
        #Ответ бота
        bot.reply_to(message, f'Сейчас погода: {temp}°C\n'
                              f'Минимальная температура сегодня: {tempnin}°C\n'
                              f'Максимальная температура сегодня: {tempmax}°C\n')
        #тернрарное выражение, которое проверяет по температуре погоду и высылает соответствующее IMG
        image = 'images.jpeg' if temp > 5.0 else '5538410.png'
        #Открываем файл с картинкой
        file = open('./' + image, 'rb')
        #отправка фото
        bot.send_photo(message.chat.id, file)
    else:
        bot.reply_to(message, f'Город указан неверно, повторите попытку')
bot.polling(none_stop=True)