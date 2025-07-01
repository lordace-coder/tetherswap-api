import telebot
import os, dotenv
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

dotenv.load_dotenv()
bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT", ""))

name = os.getenv("NAME", "TetherSwapBot")
url = os.getenv("URL", "https://x-payee.com")
username = os.getenv("TELEGRAM_USERNAME")


# 🔥 Start command
@bot.message_handler(commands=["start"])
def send_welcome(message):
    text = (
        f"👋 Hey there, welcome to *{name}*! 🚀\n\n"
        "This is your trusted Telegram bot for swapping *Pi Network tokens ↔ USDT* 💱.\n"
        "Fast, secure, and built just for you. 😎\n\n"
        "What would you like to do?"
    )
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🔗 Get Referral Link", callback_data="get_ref"),
        InlineKeyboardButton("👥 Check Referrals", callback_data="check_ref"),
        InlineKeyboardButton(
            "💱 TetherSwap",
            web_app=WebAppInfo(url=url),
        ),
    )
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")


# ⚙️ Handle callback actions
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    if call.data == "get_ref":
        ref_link = f"https://t.me/{username}?start={call.from_user.id}"
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, f"🔗 Your referral link:\n{ref_link}")

    elif call.data == "check_ref":
        # Dummy reply — you'd replace this with real logic tied to a database
        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            "👥 You have *3* successful referrals. Keep it up! 💪",
            parse_mode="Markdown",
        )


# 🏁 Run the bot with polling
if __name__ == "__main__":
    bot.infinity_polling()
