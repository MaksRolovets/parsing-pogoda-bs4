from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import requests
from block import list, TOKEN
from bs4 import BeautifulSoup

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


url = 'https://ru.meteotrend.com/'
head = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 OPR/96.0.0.0'
}

@dp.message_handler(commands='start')
async def start(message):
    await bot.send_message(message.from_user.id, 'Введите белорусский город:')
    

@dp.message_handler()
async def info(message):

    try:
        city = message.text
        link = url + list[message.text.title()]

        req = requests.get(link, headers=head) # гет запрос сайта

        with open('data.html', 'w', encoding='utf-8') as file: # сохранение файла
            file.write(req.text)

        with open('data.html', encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        weatcher = soup.find('div', {'class':'wdesc', 'class':'section detailed'}).find('a', attrs={'name':'weather_2'}).find_all('b') #Поиск данных
        col = []
        for i in weatcher:
            col.append(i.text)
        pogoda = weatcher[col.index('день') + 3].text
        weather = weatcher[col.index('день') + 6].text
        temp_day = weatcher[col.index('день') + 2].text
        temp_north = weatcher[col.index('ночь') + 1].text
        await bot.send_message(message.from_user.id, f'Город: {city}\nВетер: {weather}\nПогода: {pogoda}\nНочью: {temp_north} °C\nДнем: {temp_day}')
    except:
        await message.answer(text='Введите корректно беларуский город!')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)