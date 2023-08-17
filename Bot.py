import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
import webbrowser
from  selenium import webdriver

bot = telebot.TeleBot('6660244432:AAELaBprXA3gbQjmIvWWKIWGC5j9jT6UeBw',)

@bot.message_handler(commands = ['start'])
def start(message):
    mess = f'Привет, {message.from_user.first_name}'
    bot.send_message(message.chat.id, mess)

# @bot.message_handler(commands=['matches'])
# def site(message):
#     webbrowser.open('https://hltv.org/matches')


@bot.message_handler(commands=['CS'])
def web(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width= 2 )
    gamesr8 = types.KeyboardButton('gamers8')
    gamesr1 = types.KeyboardButton('gamers8/1')
    gamers2 = types. KeyboardButton ('gamers8/2')
    markup.add(gamesr8,gamesr1, gamers2)
    bot.send_message(message.chat.id, 'Выбирай', reply_markup=markup)

@bot.message_handler(func=lambda message:message.text in ['gamers8','gamers8/1','gamers8/2'])
def on_click(message):
    if message.text == 'gamers8':
        bot.send_message(message.chat.id, 'https://twitch.tv/gamers8gg')
    elif message.text == 'gamers8/2':
        bot.send_message(message.chat.id, 'https://twitch.tv/gamers8gg_b')
    elif message.text == 'gamers8/1':
        bot.send_message(message.chat.id, 'https://twitch.tv/gamers8gg_c')

@bot.message_handler(commands=['match'])
def matches(message):
    url = 'https://hltv.org/matches'
    response = requests.get(url)
    if response.status_code == 200:
       soup = BeautifulSoup(response.text, 'html.parser')
       match_elements = soup.find_all('div', class_='match')
       options = webdriver.ChromeOptions()
       options.add_argument('--headless')
       driver = webdriver.Chrome(executable_path=r'C:\Users\Seva\AppData\Roaming\Local\chromedriver-win64\chromedriver.exe', options=options)
       for match in match_elements:
         team1 = match.find('div', class_='team').text.strip()
         team2 = match.find('div', class_='team').find_next('div', class_='team').text.strip()
         time = match.find('div', class_='time').text.strip()
         print(f'Team1:{team1}')
         print(f'Team2:{team2}')
         print(f'Time:{time}')
         print('=' * 40)

         match_url = match.find('a')['href']
         driver.get(match_url)
         driver.save_screenshot(f'screenshot_{team1}_vs_{team2}.png')

       driver.quit()
    else:
        print('Ошибка')



# @bot.message_handler(commands=['get_info'])
# def get_info(message):
#     url = 'https://www.hltv.org/matches'
#     response = requests.get(url)
#     response.raise_for_status()
#     if response.status_code == 200:
#         data = response.text
#         bot.send_message(message.chat.id,data)
#     else:
#         bot.send_message(message.chat.id, 'не фартануло')







bot.polling(none_stop = True)