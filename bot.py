import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8858933328:AAEKrahjKNpp6mP1qDoi1GOlOKiRkxR6xdA")

LINKS = [
    "https://omg10.com/4/11088712",
    "https://omg10.com/4/11088713"
]

user_visited = {}

def get_keyboard(user_id):
    v = user_visited.get(user_id, [False, False])
    keyboard = [
        [InlineKeyboardButton("🔗 رابط 1" + (" ✅" if v[0] else ""), url=LINKS[0])],
        [InlineKeyboardButton("✅ دخلت رابط 1" if not v[0] else "☑️ تم رابط 1", callback_data="v1")],
        [InlineKeyboardButton("🔗 رابط 2" + (" ✅" if v[1] else ""), url=LINKS[1])],
        [InlineKeyboardButton("✅ دخلت رابط 2" if not v[1] else "☑️ تم رابط 2", callback_data="v2")],
        [InlineKeyboardButton("🎯 تحقق النهائي", callback_data="final")],
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_visited[user_id] = [False, False]
    await update.message.reply_text(
        "🎉 للمشاركة في المسابقة:\n\n"
        "1️⃣ ادخل رابط 1 واضغط دخلت\n"
        "2️⃣ ادخل رابط 2 واضغط دخلت\n"
        "3️⃣ اضغط تحقق النهائي ✅",
        reply_markup=get_keyboard(user_id)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if user_id not in user_visited:
        user_visited[user_id] = [False, False]

    if query.data == "v1":
        user_visited[user_id][0] = True
        await query.edit_message_reply_markup(get_keyboard(user_id))

    elif query.data == "v2":
        user_visited[user_id][1] = True
        await query.edit_message_reply_markup(get_keyboard(user_id))

    elif query.data == "final":
        v = user_visited.get(user_id, [False, False])
        if not v[0] and not v[1]:
            await query.answer("❌ ما دخلت أي رابط!", show_alert=True)
        elif not v[0]:
            await query.answer("❌ باقي رابط 1!", show_alert=True)
        elif not v[1]:
            await query.answer("❌ باقي رابط 2!", show_alert=True)
        else:
            await query.edit_message_text("🎊 تم تسجيلك في المسابقة! بالتوفيق ⭐")

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    print("البوت شغّال ✅")
    app.run_polling()
