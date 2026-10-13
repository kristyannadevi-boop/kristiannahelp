import telebot
from telebot import types
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID"))

bot = telebot.TeleBot(BOT_TOKEN)
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Оставить заявку")
    bot.send_message(
        message.chat.id,
        "Привет! 👋\nЗдесь ты можешь оставить заявку.\nНажми кнопку ниже, чтобы начать.",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.text == "Оставить заявку")
def ask_name(message):
    user_data[message.chat.id] = {}
    bot.send_message(message.chat.id, "Как тебя зовут?", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, ask_contact)

def ask_contact(message):
    user_data[message.chat.id]['name'] = message.text
    bot.send_message(message.chat.id, "Оставь контакт для связи (телефон, @ник или email):")
    bot.register_next_step_handler(message, ask_request)

def ask_request(message):
    user_data[message.chat.id]['contact'] = message.text
    bot.send_message(message.chat.id, "Что тебя интересует? Опиши коротко:")
    bot.register_next_step_handler(message, finish)

def finish(message):
    user_data[message.chat.id]['request'] = message.text
    data = user_data[message.chat.id]

    text = (
        "🔔 <b>Новая заявка!</b>\n\n"
        f"👤 Имя: {data['name']}\n"
        f"📞 Контакт: {data['contact']}\n"
        f"📝 Запрос: {data['request']}\n"
        f"🆔 Telegram ID: <code>{message.chat.id}</code>\n"
        f"🔗 Юзер: @{message.from_user.username or '—'}"
    )
    bot.send_message(ADMIN_ID, text, parse_mode="HTML")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Оставить заявку")
    bot.send_message(
        message.chat.id,
        "✅ Спасибо! Заявка отправлена, я свяжусь с тобой скоро.",
        reply_markup=markup
    )
    user_data.pop(message.chat.id, None)

bot.infinity_polling()
