import threading
from flask import Flask, request, redirect
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8068190455:AAFJKFYSf18-2H_1eI9NuGzmg-pw8ErUyQg"
AD_URL = "https://omg10.com/4/11066405"
BASE_URL = "https://mybot-production-2e24.up.railway.app"


VIDEO_IDS = [
    "BAACAgUAAxkBAAMKahgbcjVv9yClr5Qd-fRAg2Hd7N4AAlIgAALQOMFUPtnSjm7SsOY7BA",
    "BAACAgUAAxkBAAMNahgbclIDAyx4eiiPKm6NPHESiQQAAlMgAALQOMFU4tbMl9d4h787BA",
    "BAACAgUAAxkBAAMOahgbcl32NYMjDpeyrohkxPcYyEMAAlQgAALQOMFUIGg2NqjNJdA7BA",
    "BAACAgUAAxkBAAMPahgbciTfgSEw6f-Dc0vlL5yXJogAAlEgAALQOMFU7q3JTMdL59w7BA",
    ]
    
visited_users = set()

flask_app = Flask(__name__)

@flask_app.route("/visit")
def visit():
    user_id = request.args.get("user_id")
    if user_id:
        visited_users.add(int(user_id))
    return redirect(AD_URL)

@flask_app.route("/")
def home():
    return "Bot is running!", 200

def run_flask():
    flask_app.run(host="0.0.0.0", port=8080)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    keyboard = [
        [InlineKeyboardButton("Visit Link", url=f"{BASE_URL}/visit?user_id={user_id}")],
        [InlineKeyboardButton("Get My Videos", callback_data="send_video")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Tap Visit Link first, then tap Get My Videos!",
        reply_markup=reply_markup
    )

async def send_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    if user_id not in visited_users:
        await query.answer("Please tap Visit Link first!", show_alert=True)
        return
    visited_users.discard(user_id)
    await query.answer("Sending your videos...")
    for video_id in VIDEO_IDS:
        await query.message.reply_video(
            video=video_id,
            caption="Enjoy!"
        )

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(send_video, pattern="^send_video$"))
    app.run_polling()