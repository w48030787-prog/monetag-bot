import os
import threading
from flask import Flask, redirect
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatMember
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8858933328:AAEKrahjKNpp6mP1qDoi1GOlOKiRkxR6xdA")
BASE_URL = os.environ.get("BASE_URL", "https://monetag-bot-production.up.railway.app")
PORT = int(os.environ.get("PORT", 8080))
ADMIN_ID = 8030787672
CHANNEL = "@NajomComp"

LINKS = [
    "https://omg10.com/4/11088712",
    "https://omg10.com/4/11088713"
]

visited = {}
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "✅"

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

async def is_subscribed(user_id, context):
    try:
        member = await context.bot.get_chat_member(CHANNEL, user_id)
        return member.status in [ChatMember.MEMBER, ChatMember.ADMINISTRATOR, ChatMember.OWNER]
    except:
        return False

def get_keyboard(user_id):
    v = visited.get(user_id, [False, False])
    keyboard = []
    if not v[0]:
        keyboard.append([InlineKeyboardButton("🔗 الرابط الأول", url=f"{BASE_URL}/v1/{user_id}")])
    if not v[1]:
        keyboard.append([InlineKeyboardButton("🔗 الرابط الثاني", url=f"{BASE_URL}/v2/{user_id}")])
    keyboard.append([InlineKeyboardButton("🎯 تحقق من مشاركتي", callback_data="final")])
    return InlineKeyboardMarkup(keyboard)

def sub_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 اشترك في القناة", url=f"https://t.me/NajomComp")],
        [InlineKeyboardButton("✅ اشتركت، تحقق", callback_data="check_sub")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not await is_subscribed(user_id, context):
        await update.message.reply_text(
            "⚠️ *لازم تشترك في القناة أولاً!*\n\n"
            "اشترك في قناتنا ثم اضغط تحقق 👇",
            parse_mode="Markdown",
            reply_markup=sub_keyboard()
        )
        return
    visited[user_id] = [False, False]
    await update.message.reply_text(
        "🌟 *أهلاً بك في مسابقة النجوم!*\n\n"
        "للمشاركة اتبع الخطوات:\n\n"
        "1️⃣ اضغط *الرابط الأول* وانتظر *10 ثواني* ⏱\n"
        "2️⃣ اضغط *الرابط الثاني* وانتظر *10 ثواني* ⏱\n"
        "3️⃣ اضغط *تحقق* ✅\n\n"
        "بالتوفيق! 🍀",
        parse_mode="Markdown",
        reply_markup=get_keyboard(user_id)
    )

async def newcomp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ ما عندك صلاحية!")
        return
    visited.clear()
    await update.message.reply_text(
        "✅ *تم إعادة تعيين المسابقة!*\n\n"
        "كل المشتركين القدامى محذوفين\n"
        "المسابقة الجديدة جاهزة 🎉",
        parse_mode="Markdown"
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "check_sub":
        if not await is_subscribed(user_id, context):
            await query.answer("❌ ما اشتركت بعد في القناة!", show_alert=True)
            return
        visited[user_id] = [False, False]
        await query.edit_message_text(
            "🌟 *أهلاً بك في مسابقة النجوم!*\n\n"
            "للمشاركة اتبع الخطوات:\n\n"
            "1️⃣ اضغط *الرابط الأول* وانتظر *10 ثواني* ⏱\n"
            "2️⃣ اضغط *الرابط الثاني* وانتظر *10 ثواني* ⏱\n"
            "3️⃣ اضغط *تحقق* ✅\n\n"
            "بالتوفيق! 🍀",
            parse_mode="Markdown",
            reply_markup=get_keyboard(user_id)
        )
        return

    v = visited.get(user_id, [False, False])
    if not v[0] and not v[1]:
        await query.edit_message_text(
            "🌟 *أهلاً بك في مسابقة النجوم!*\n\n"
            "للمشاركة اتبع الخطوات:\n\n"
            "1️⃣ اضغط *الرابط الأول* وانتظر *10 ثواني* ⏱\n"
            "2️⃣ اضغط *الرابط الثاني* وانتظر *10 ثواني* ⏱\n"
            "3️⃣ اضغط *تحقق* ✅\n\n"
            "بالتوفيق! 🍀",
            parse_mode="Markdown",
            reply_markup=get_keyboard(user_id)
        )
    elif not v[0]:
        await query.edit_message_text(
            "⚠️ *باقي الرابط الأول!*\n\n"
            "اضغط عليه وانتظر *10 ثواني* ⏱\n"
            "ثم ارجع واضغط تحقق ✅",
            parse_mode="Markdown",
            reply_markup=get_keyboard(user_id)
        )
    elif not v[1]:
        await query.edit_message_text(
            "⚠️ *باقي الرابط الثاني!*\n\n"
            "اضغط عليه وانتظر *10 ثواني* ⏱\n"
            "ثم ارجع واضغط تحقق ✅",
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
    app.add_handler(CommandHandler("newcomp", newcomp))
    app.add_handler(CallbackQueryHandler(button))
    print("البوت شغّال ✅")
    app.run_polling()
