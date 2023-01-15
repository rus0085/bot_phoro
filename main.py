
import random
import os
import telebot
import sqlite3
from telebot import types

connector = sqlite3.connect('info_users_photo.db')
cursor = connector.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users(
       userid INT ,
       name TEXT,
       age TEXT,
       photo TEXT,
       average INT,
       shoot INT);
    """)
connector.commit()



info_sql = ['','','','','','']

images = dict()
token = '*******************'
bot = telebot.TeleBot(token)

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton("Профиль")
btn2 = types.KeyboardButton("Угадывать")
markup.add(btn1, btn2)



@bot.message_handler(commands=["start"])
def get_name(message):


      connector = sqlite3.connect('info_users_photo.db')
      cursor = connector.cursor()
      res = cursor.execute("SELECT userid FROM users WHERE userid =?",(message.from_user.id,))

      if bool(len(res.fetchall()))  :

          bot.send_message(message.from_user.id, "Вы уже есть в нашей базе, выберите кнопки ниже", reply_markup=markup)
      else:
          send3 = bot.send_message(message.from_user.id, "Здраствуйте, как вас зовут?")
          bot.register_next_step_handler(send3, get_text_messages)



def get_text_messages(message):
    info_sql[1] = message.text
    send2 = bot.send_message(message.from_user.id, "Пришлите ваше фото")
    bot.register_next_step_handler(send2, on_photo)

def on_photo(message):
    info3 = str(message.chat.id)
    info_sql[0]=info3.replace(',','')
    images [str(message.chat.id)] = []
    document_id = message.photo[-1].file_id
    file_info = bot.get_file(document_id)
    send_1 = bot.send_message(message.chat.id, 'Сколько лет вам на фото?')

    dowloaded_file_photo = bot.download_file(file_info.file_path)
    info_sql[3] = str(file_info.file_path)

    src = 'all_photo/' + file_info.file_path
    with open(src, 'wb') as new_file:
        new_file.write(dowloaded_file_photo)
    print(file_info.file_path)



    bot.register_next_step_handler(send_1, age)





def age(message):

    age_number = message.text
    info_sql[2]= str(age_number)
    info_sql[4] = 0
    info_sql[5] = 0
    bot.send_message(message.from_user.id, "Фото загружено")
    connector = sqlite3.connect('info_users_photo.db')
    cursor = connector.cursor()
    cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?,?,?);", info_sql)
    # Сохраняем изменения
    connector.commit()

    bot.send_message(message.from_user.id, "Теперь можете приступить к угадыванию, нажав на кнопку ниже или перейти в профиль",reply_markup=markup )



@bot.message_handler(content_types=['text'])
def menu(message):
    connector = sqlite3.connect('info_users_photo.db')
    cursor = connector.cursor()
    a = message.from_user.id
    cursor.execute(f"SELECT * FROM users WHERE userid = {a}")
    bet = cursor.fetchall()
    summ = 0
    i = 0
    for i in range(len(bet)) :
        summ = summ+ int(bet[i][5])
        i+=1
    summ = summ/i
    if message.text == "Профиль":
        bot.send_message(message.from_user.id, f'''Привет {bet[0][1]}!
В среднем в дают {summ}''')
    elif message.text == "Угадывать":
        ugaday(message)


def update_data(message,data2):
    print(2)
    bot.send_message(message.from_user.id, "Возраст человека : " + data2)


def ugaday(message):
        connector = sqlite3.connect('info_users_photo.db')
        cursor = connector.cursor()
        cursor.execute("SELECT photo, age FROM users ORDER BY RANDOM() LIMIT 1")
        data1 = cursor.fetchone()
        data = str(data1[0])
        data2 = str(data1[1])
        data = data.replace("'", '')
        data = data.replace(',', '')
        data = data.replace('(', '')
        data = data.replace(')', '')
        photo = open('all_photo/' + data, 'rb')
        bot.send_photo(message.from_user.id, photo)
        send4 = bot.send_message(message.from_user.id, "Сколько лет человеку на фото?")
        bot.register_next_step_handler(send4, update_data, data2)

if 1:
    bot.infinity_polling()
