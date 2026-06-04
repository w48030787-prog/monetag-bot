import os
import threading
from flask import Flask, redirect
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8858933328:AAEKrahjKNpp6mP1qDoi1GOlOKiRkxR6xdA")
BASE_URL = os.environ.get("BASE_URL", "https://monetag-bot-production.up.railway.app")
PORT = int(os.environ.get("PORT", 8080))
ADMIN_ID = 8030787672

LINKS = [
    "https://omg10.com/4/11088712",
    "https://omg10.com/4/11088713",
    "https://omg10.com/4/11099320"
]

visited = {}
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "✅"

@flask_app.route("/v1/<int:user_id>")
def visit1(user_id):
    if user_id not in visited:
        visited[user_id] = [False, False, False]
    visited[user_id][0] = True
    return redirect(LINKS[0])

@flask_app.route("/v2/<int:user_id>")
def visit2(user_id):
    if user_id not in visited:
        visited[user_id] = [False, False, False]
    visited[user_id][1] = True
    return redirect(LINKS[1])

@flask_app.route("/v3/<int:user_id>")
def visit3(user_id):
    if user_id not in visited:
        visited[user_id] = [False, False, False]
    visited[user_id][2] = True
    return redirect(LINKS[2])

def get_keyboard(user_id):
    v = visited.get(user_id, [False, False, False])
    keyboard = []
    if not v[0]:
        keyboard.append([InlineKeyboardButton("🔗 الرابط الأول", url=f"{BASE_URL}/v1/{user_id}")])
    if not v[1]:
        keyboard.append([InlineKeyboardButton("🔗 الرابط الثاني", url=f"{BASE_URL}/v2/{user_id}")])
    if not v[2]:
        keyboard.append([InlineKeyboardButton("🔗 الرابط الثالث", url=f"{BASE_URL}/v3/{user_id}")])
    keyboard.append([InlineKeyboardButton("🎯 تحقق من مشاركتي", callback_data="final")])
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    visited[user_id] = [False, False, False]
    await update.message.reply_text(
        "🌟 *أهلاً بك في مسابقة النجوم!*\n\n"
        "للمشاركة اتبع الخطوات:\n\n"
        "1️⃣ اضغط *الرابط الأول* وانتظر *10 ثواني* ⏱\n"
        "2️⃣ اضغط *الرابط الثاني* وانتظر *10 ثواني* ⏱\n"
        "3️⃣ اضغط *الرابط الثالث* وانتظر *10 ثواني* ⏱\n"
        "4️⃣ اضغط *تحقق* ✅\n\n"
        "بالتوفيق! 🍀",
        parse_mode="Markdown",
        reply_markup=get_keyboard(user_id)
    )

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ ما عندك صلاحية!")
        return
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🗑 مسح كل البيانات - مسابقة جديدة", callback_data="clear_all")],
    ])
    await update.message.reply_text(
        "👑 *لوحة التحكم*\n\n"
        f"📊 عدد المشاركين: {len(visited)}",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "clear_all":
        if user_id != ADMIN_ID:
            await query.answer("❌ ما عندك صلاحية!", show_alert=True)
            return
        visited.clear()
        await query.edit_message_text(
            "✅ *تم مسح كل البيانات!*\n\n"
            "المسابقة الجديدة جاهزة 🎉",
            parse_mode="Markdown"
        )
        return

    v = visited.get(user_id, [False, False, False])
    remaining = []
    if not v[0]: remaining.append("الرابط الأول")
    if not v[1]: remaining.append("الرابط الثاني")
    if not v[2]: remaining.append("الرابط الثالث")

    if remaining:
        await query.edit_message_text(
            "⚠️ *باقي عليك:*\n\n" +
            "\n".join([f"🔗 {r}" for r in remaining]) +
            "\n\nادخل الروابط الباقية وانتظر *10 ثواني* ⏱\nثم اضغط تحقق ✅",
            parse_mode="Markdown",
            reply_markup=get_keyboard(user_id)
        )
    else:
        await query.edit_message_text(
            "🎊 *تم تسجيلك بنجاح!*\n\n"
            "مشاركتك في المسابقة مؤكدة ⭐\n"
            "سيتم التواصل معك إذا فزت 🏆",
            parse_mode="Markdown"
        )

def run_flask():
    flask_app.run(host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(CallbackQueryHandler(button))
    print("البوت شغّال ✅")
    app.run_polling()
