import telebot
from telebot import types
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID"))
PORT = int(os.environ.get("PORT", 10000))


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, format, *args):
        pass


def run_http_server():
    server = HTTPServer(("0.0.0.0", PORT), HealthHandler)
    server.serve_forever()


threading.Thread(target=run_http_server, daemon=True).start()

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Приветствую.\n"
        "Я AI-ассистент Кристианны.\n\n"
        "Напишите, пожалуйста, Ваше имя и контакты одной строкой\n"
        "Она обязательно свяжется с Вами в ближайшее время 💖",
        reply_markup=types.ReplyKeyboardRemove()
    )


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text.startswith('/'):
        return

    text = (
        "🔔 <b>Новая заявка!</b>\n\n"
        f"💬 Сообщение: {message.text}\n"
        f"🆔 Telegram ID: <code>{message.chat.id}</code>\n"
        f"🔗 Юзер: @{message.from_user.username or '—'}"
    )
    bot.send_message(ADMIN_ID, text, parse_mode="HTML")
    bot.send_message(message.chat.id, "Благодарю Вас! Ваша заявка отправлена.")


bot.infinity_polling()
