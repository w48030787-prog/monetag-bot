import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8858933328:AAEKrahjKNpp6mP1qDoi1GOlOKiRkxR6xdA")

LINKS = [
    "https://omg10.com/4/11088712",
    "https://omg10.com/4/11088713"
]

visited_users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔗 رابط 1", url=LINKS[0])],
        [InlineKeyboardButton("🔗 رابط 2", url=LINKS[1])],
        [InlineKeyboardButton("✅ تحقق", callback_data="verify")],
    ]
    await update.message.reply_text(
        "🎉 للمشاركة في المسابقة:\n\n1️⃣ ادخل الرابطين\n2️⃣ اضغط تحقق ✅",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    visited_users.add(user_id)
    await query.edit_message_text("✅ تم تسجيلك في المسابقة! بالتوفيق 🎊")

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(verify, pattern="^verify$"))
    print("البوت شغّال ✅")
    app.run_polling()
