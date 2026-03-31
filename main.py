import os
import time
import yt_dlp
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    filters,
    ContextTypes
)

TOKEN = "8760344330:AAG4KQOaRo_JJNJC8r5Tg88lFHDM4PSABSs"

user_last_request = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ابعت لينك الفيديو و اهدي علي نفسك 🙄👇")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not url.startswith("http"):
        await update.message.reply_text("❌ ابعت لينك صح يخالي")
        return

    now = time.time()
    last = user_last_request.get(update.message.chat_id, 0)

    if now - last < 5:
        await update.message.reply_text("استنى شوية يبووي 😅")
        return

    user_last_request[update.message.chat_id] = now

    await update.message.reply_text("⏳ جاري التحميل...")

    filename = None

    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'video.%(ext)s',
            'quiet': True
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
        except:
            ydl_opts['format'] = 'worst'
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

        # 👇 مهم: ده جوه try
        ext = filename.split('.')[-1].lower()

        with open(filename, 'rb') as file:
            if ext in ['jpg', 'jpeg', 'png', 'webp']:
                await update.message.reply_photo(photo=file)
            else:
                await update.message.reply_video(video=file)

    except Exception as e:
        await update.message.reply_text(f"❌ حصل خطأ:\n{e}")

    finally:
        if filename and os.path.exists(filename):
            os.remove(filename)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

print("Bot is running...")
app.run_polling()
