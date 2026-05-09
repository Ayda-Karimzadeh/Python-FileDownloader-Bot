import telebot
import logging
import os
from telebot import types
import sqlite3
from setup_database import init_db
import re

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

# Bale API URL
telebot.apihelper.API_URL = 'https://tapi.bale.ai/bot{0}/{1}'

API_TOKEN = os.environ.get("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

init_db()

phone_pattern = re.compile(r"^(?:\+98|0)?9\d{9}$")
email_pattern = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
CANCEL_TEXT = "لغو ثبت نام"
ALLOWED_EMAIL_DOMAINS = {"gmail.com", "yahoo.com"}

# Text constants
poshtibani_text = "پشتیبانی"
khadamat_pas_text = "اطلاعات پس از فروش"
mahsolat_text = "محصولات"
nahve_kharid_text = "نحوه خرید"

@bot.message_handler(commands=['start'])
def start_bot(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_poshtibani = types.KeyboardButton("پشتیبانی")
    btn_khadamat_pas = types.KeyboardButton("اطلاعات خدمات پس از فروش")
    btn_mahsolat = types.KeyboardButton("محصولات")
    btn_sabtnam = types.KeyboardButton("ثبت نام")
    btn_nahve_kharid = types.KeyboardButton("نحوه خرید")
    keyboard.add(
        btn_poshtibani,
        btn_khadamat_pas,
        btn_mahsolat,
        btn_sabtnam,
        btn_nahve_kharid
    )

    bot.send_message(message.chat.id, "خوش آمدید", reply_markup=keyboard)

# ---------- Registration flow handlers (outside main handler) ----------

def save_user(chat_id, first_name, last_name, phone, email):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT INTO users (chat_id, first_name, last_name, phone, email)
    VALUES (?, ?, ?, ?, ?)
    """, (chat_id, first_name, last_name, phone, email))

    conn.commit()
    conn.close()


def setup_name(message):
    """
    Starts the registration process by asking for first name.
    """
    sent = bot.send_message(message.chat.id, "نام خود را وارد کنید.")
    # NOTE: register on 'sent' message, not the original
    bot.register_next_step_handler(sent, assign_firstname)

def assign_firstname(message):
    """
    Receives first name and asks for last name.
    """
    first_name = message.text
    sent = bot.send_message(message.chat.id, "نام خانوادگی خود را وارد کنید.")
    bot.register_next_step_handler(sent, assign_last_name, first_name)

def assign_last_name(message, first_name):
    """
    Receives last name and finishes registration.
    """
    last_name = message.text
    sent = bot.send_message(message.chat.id, "شماره موبایل خود را وارد کنید.")
    bot.register_next_step_handler(sent, assign_phone_number, first_name, last_name)

def assign_phone_number(message, first_name, last_name):
    phone_number = message.text
    if not phone_pattern.match(phone_number):
        sent = bot.send_message(
            message.chat.id,
            "شماره موبایل معتبر نیست. لطفا شماره‌ای مثل 09123456789 وارد کنید."
        )
        return bot.register_next_step_handler(
            sent,
            assign_phone_number,
            first_name,
            last_name
        )
    sent = bot.send_message(message.chat.id, "ایمیل خود را وارد کنید.")
    bot.register_next_step_handler(
        sent,
        assign_email,
        first_name,
        last_name,
        phone_number
    )
    
def assign_email(message, first_name, last_name, phone_number):
    email = message.text
    if not email_pattern.match(email):
        sent = bot.send_message(
            message.chat.id,
            "فرمت ایمیل معتبر نیست. لطفا دوباره وارد کنید. (مثال: test@example.com)"
        )
        return bot.register_next_step_handler(
            sent,
            assign_email,
            first_name,
            last_name,
            phone_number
        )

    # Email OK → save user
    save_user(
        chat_id=message.chat.id,
        first_name=first_name,
        last_name=last_name,
        phone=phone_number,
        email=email
    )

    bot.send_message(
        message.chat.id,
        f"شما با نام و نام خانوادگی {first_name} {last_name}، شماره تماس {phone_number} و ایمیل {email} ثبت نام شدید."
    )

# ---------- Main message handler ----------

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "پشتیبانی":
        bot.send_message(message.chat.id, poshtibani_text)

    elif message.text == "اطلاعات خدمات پس از فروش":
        bot.send_message(message.chat.id, khadamat_pas_text)

    elif message.text == "محصولات":
        bot.send_message(message.chat.id, mahsolat_text)

    elif message.text == "ثبت نام":
        # Just call the function with the actual message object
        setup_name(message)

    elif message.text == "نحوه خرید":
        bot.send_message(message.chat.id, nahve_kharid_text)

    else:
        bot.send_message(message.chat.id, 'لطفا از دکمه های مورد نظر استفاده کنید!')

# ---------- Start polling ----------

bot.infinity_polling()
