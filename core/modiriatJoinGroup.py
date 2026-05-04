import telebot
import os
import logging

logger = telebot.logger

telebot.apihelper.API_URL = 'https://tapi.bale.ai/bot{0}/{1}'

API_TOKEN = os.environ.get("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

@bot.chat_join_request_handler()
def join_request_handler(request):
    logger.info(request)
    bot.approve_chat_join_request(request.chat.id, request.from_user.id)
    # bot.decline_chat_join_request
bot.infinity_polling()