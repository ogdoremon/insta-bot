import os
import yt_dlp
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Token ko Render ke Environment Variables se uthayenge (Safety ke liye)
TOKEN = os.environ.get("BOT_TOKEN")

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🔥 **Instagram Reel Downloader** 🔥\n\n"
        "Bhai, bas Reel ka link bhejo, main video nikaal kar deta hoon! 🚀"
    )

def download_reel(update: Update, context: CallbackContext):
    url = update.message.text
    
    # Check karna ki link Instagram ka hi hai
    if "instagram.com" not in url:
        update.message.reply_text("Bhai, sahi Instagram Reel link bhejo! ❌")
        return

    update.message.reply_text("Process ho raha hai, thoda ruko... ⏳")
    
    # yt-dlp settings for high quality download
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',
        'quiet': True,
        'no_warnings': True,
        'cookiefile': 'cookies.txt' # Agar cookies ho toh (optional)
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Video Telegram par send karna
        update.message.reply_video(
            video=open('video.mp4', 'rb'),
            caption="Lo bhai, aapki Reel! ✅\n@YourBotName"
        )
        
        # File delete karna taaki Render ki memory full na ho
        if os.path.exists("video.mp4"):
            os.remove("video.mp4")
            
    except Exception as e:
        update.message.reply_text(f"Bhai error aa gaya: {str(e)[:100]}...")

def main():
    if not TOKEN:
        print("Error: BOT_TOKEN nahi mila! Render settings check karo.")
        return

    updater = Updater(TOKEN)
    dp = updater.dispatcher

    # Handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, download_reel))
    
    # Bot start karna
    print("Bot chalu ho gaya hai...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
  
