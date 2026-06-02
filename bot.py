import os
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import asyncio
import threading

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8858933328:AAEKrahjKNpp6mP1qDoi1GOlOKiRkxR6xdA")

LINKS = [
    "https://omg10.com/4/11088712",
    "https://omg10.com/4/11088713"
]

visited = {}

flask_app = Flask(__name__)

@flask_app.route("/v1/<int:user_id>")
def visit1(user_id):
    if user_id not in visited:
        visited[user_id] = [False, False]
    visited[user_id][0] = True
    return redirect(LINKS[0])

@flask_app.route("/v2/<int:user_id>")
def visit2(user_id):
    if user_id not in visited:
        visited[user_id] = [False, False]
    visited[user_id][1] = True
    return redirect(LINKS[1])

from flask import redirect

def get_keyboard(user_id, base_url):
    v = visited.get(user_id, [False, False])
    keyboard = [
        [InlineKeyboardButton("🔗 الرابط الأول" + (" ✅" if v[0] else ""), url=f"{base_url}/v1/{user_id}")],
        [InlineKeyboardButton("🔗 الرابط الثاني" + (" ✅" if v[1] else ""), url=f"{base_url}/v2/{user_id}")],
        [InlineKeyboardButton("🎯 تحقق من مشاركتي", callback_data="final")],
    ]
    return InlineKeyboardMarkup(keyboard)

BASE_URL = os.environ.get("BASE_URL", "http://localhost:5000")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    visited[user_id] = [False, False]
    await update.message.reply_text(
        "🌟 *أهلاً بك في مسابقة النجوم!*\n\n"
        "للمشاركة اتبع الخطوات:\n\n"
        "1️⃣ اضغط *الرابط الأول* وانتظر\n"
        "2️⃣ اضغط *الرابط الثاني* وانتظر\n"
        "3️⃣ اضغط *تحقق* ✅\n\n"
        "بالتوفيق! 🍀",
        parse_mode="Markdown",
        reply_markup=get_keyboard(user_id, BASE_URL)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    v = visited.get(user_id, [False, False])

    if not v[0] and not v[1]:
        await query.answer("❌ ما دخلت أي رابط بعد!", show_alert=True)
    elif not v[0]:
        await query.answer("❌ باقي الرابط الأول!", show_alert=True)
    elif not v[1]:
        await query.answer("❌ باقي الرابط الثاني!", show_alert=True)
    else:
        await query.edit_message_text(
            "🎊 *تم تسجيلك بنجاح!*\n\n"
            "مشاركتك في المسابقة مؤكدة ⭐\n"
            "سيتم التواصل معك إذا فزت 🏆",
            parse_mode="Markdown"
        )

def run_flask():
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    print("البوت شغّال ✅")
    app.run_polling()
