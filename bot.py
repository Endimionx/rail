
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from ai_model import predict_next

BOT_TOKEN = os.getenv("BOT_TOKEN")

user_draws = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Selamat datang di Bot Prediksi Togel AI!\n"
        "Ketik /input 1234,5678,9012 untuk memberi data.\n"
        "Ketik /prediksi untuk melihat angka prediksi."
    )

async def input_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = update.message.text.split(" ", 1)[1]
        draws = [int(x.strip()) for x in args.split(",") if x.strip().isdigit()]
        user_draws[update.effective_chat.id] = draws
        await update.message.reply_text(f"✅ Data {len(draws)} angka berhasil disimpan.")
    except:
        await update.message.reply_text("❌ Format salah. Contoh: /input 1234,4567,8910")

async def prediksi_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    draws = user_draws.get(update.effective_chat.id)
    if not draws:
        await update.message.reply_text("⚠️ Silakan input angka dulu dengan /input")
        return
    pred, alt = predict_next(draws)
    if pred is None:
        await update.message.reply_text("⚠️ Minimal 5 angka diperlukan untuk prediksi.")
    else:
        msg = f"🎯 Prediksi AI: {pred}\n🔁 Alternatif: {', '.join(alt)}"
        await update.message.reply_text(msg)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("input", input_handler))
    app.add_handler(CommandHandler("prediksi", prediksi_handler))
    print("Bot berjalan...")
    app.run_polling()
