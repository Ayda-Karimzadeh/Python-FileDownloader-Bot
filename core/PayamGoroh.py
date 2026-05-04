import telebot
import os
import logging

logger = telebot.logger

telebot.apihelper.API_URL = 'https://tapi.bale.ai/bot{0}/{1}'

API_TOKEN = os.environ.get("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(func=lambda message : message.chat.types in ["supergroup", "group"])
def send_welcome(message):
    logger.info("group triggered")
@bot.message_handler(func=lambda message:message.chat.type in ["private"])
def handle_message(message):
    logger.info("private triggered")