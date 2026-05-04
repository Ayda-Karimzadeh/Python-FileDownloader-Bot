import telebot
import os
from gtts import gTTS

telebot.apihelper.API_URL = 'https://tapi.bale.ai/bot{0}/{1}'

API_TOKEN = os.environ.get("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

if not os.path.exists("downloads"):
    os.makedirs("downloads")

DOWNLOAD_DIR = "downloads/"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,'send me a text in English, then i read it for you ')

@bot.message_handler(func= lambda message:True)
def text_to_speach(message):
    text = message.text
    file_name = "voices/output.mp3"
    output = gTTS(text=text, lang="en")
    output.save(file_name)
    bot.send_voice(chat_id=message.chat.id, reply_to_message_id=message.id, voice=open(file_name,"rb"))
    os.remove(file_name)

bot.infinity_polling()