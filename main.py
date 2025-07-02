import telebot
import os, dotenv
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from client import get_referrals, add_referral  
from fastapi import FastAPI, Request
import uvicorn

dotenv.load_dotenv()
bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT", ""))

app = FastAPI()

name = os.getenv("NAME", "TetherSwapBot")
url = os.getenv("URL", "")
username = os.getenv("TELEGRAM_USERNAME")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")  # Set this in your .env


# 🔥 Start command
@bot.message_handler(commands=["start"])
def send_welcome(message):
    # Check for referral in /start command
    args = message.text.split()
    if len(args) > 1:
        ref_by = args[1]
        user_id = str(message.from_user.id)
        if ref_by != user_id:  # Prevent self-referral
            add_referral(user_id, ref_by)
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
        # Connect to backend to get real referral count
        user_id = str(call.from_user.id)
        count = get_referrals(user_id)
        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            f"👥 You have *{count}* successful referrals. Keep it up! 💪",
            parse_mode="Markdown",
        )


@app.post("/")
async def webhook(request: Request):
    if request.headers.get('content-type') == 'application/json':
        json_string = await request.body()
        update = telebot.types.Update.de_json(json_string.decode('utf-8'))
        bot.process_new_updates([update])
        return ""
    else:
        return "", 403


# 🏁 Run the bot with webhook

x = bot.set_webhook(url="https://tetherswap-api.onrender.com")
print(f"Webhook set: {x}")