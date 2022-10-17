import telebot

from telebot import types
import random
import psycopg2
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()
env_path = Path(".")/'.env'
load_dotenv(dotenv_path=env_path)

token=os.getenv("TOKEN") 

bot = telebot.TeleBot(token)
conn = psycopg2.connect(host="159.223.20.145", dbname="server", user="server", password="codabra")
db = conn.cursor()


@bot.message_handler(content_types=['text'])
def idle (message):
    if message.text == '/start' and checkuser(message.from_user.id) == False:
        bot.send_message(message.from_user.id, "Welcome to the game, give name to your character")
        bot.register_next_step_handler(message, givename)
    if message.text == '/text':
        getstats(message.from_user.id)
    if message.text == '/text2':
        getenemyes(message.from_user.id)



def givename(message):
    name = message.text
    db.execute("INSERT INTO persona (user_id, name) VALUES (%s,%s)", (message.from_user.id,name))
    conn.commit()
    bot.send_message(message.from_user.id, "hi" + name + ". Welcome to the world, for сontinuation write command /game" )

def checkuser(id):
    db.execute("SELECT * FROM persona WHERE user_id = %s", (id,))
    if db.fetchone() is None:
        return False
    else:
        return True
def getstats(id):
    db.execute("SELECT * FROM persona WHERE user_id = %s", (id,))
    answer = db.fetchone()


    bot.send_message(id,
f"""
hi - {answer[7]}, its your tab:
❤️hp - {answer[1]}
😅damage - {answer[2]}
🙈save - {answer[3]}
🤠residents - {answer[4]}
🌚secrecy - {answer[5]}
👊🦶attack - {answer[6]}
""")
def getenemyes(id):
    db.execute( "SELECT * FROM enemy")
    answer = db.fetchall()
    text = 'this is all information of enemy'


    for enemy in answer:
        print(enemy)
        text += f"""
---
🌚Name - {enemy[5]} / 😅damage - {enemy[2]} / 🙈save - {enemy[3]} / 😑visibility - {enemy[4]}21


---
"""
    bot.send_message(id, text)


bot.polling(none_stop=True, interval=0)

