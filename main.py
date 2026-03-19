import os
import yt_dlp
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Token Render ke Environment Variables se aayega
TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bhai, Instagram Reel link bhejo! 🚀")

async def download_reel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "instagram.com" not in url:
        return
    
    await update.message.reply_text("Download ho raha hai... ⏳")
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        # Download logic
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).download([url]))
        
        # Video send karna
        await update.message.reply_video(video=open('video.mp4', 'rb'), caption="Lo bhai! ✅")
        
        # File delete karna
        if os.path.exists("video.mp4"):
            os.remove("video.mp4")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)[:100]}")

if __name__ == '__main__':
    if not TOKEN:
        print("Token nahi mila! Check Render Env Vars.")
    else:
        # Naya tareeka bot start karne ka (v20+)
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_reel))
        
        print("Bot chalu ho gaya...")
        app.run_polling()
        
