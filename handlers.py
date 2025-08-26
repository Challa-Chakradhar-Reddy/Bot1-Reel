from telegram import Update
from telegram.ext import CallbackContext
from instagram import fetchReel
from delete import deleteDownloads

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("👋 Send me an Instagram Reel URL and I’ll fetch the video for you!")

def handleMessage(update: Update, context: CallbackContext) -> None:
    url = update.message.text.strip()
    update.message.reply_text("⏳ Fetching reel...")

    try:
        videoPath = fetchReel(url)
        if videoPath:
            with open(videoPath, "rb") as video:
                update.message.reply_video(video=video, caption="Here's your reel 🎥")
            deleteDownloads()  # clean up files after sending
        else:
            update.message.reply_text("⚠️ Couldn’t fetch this reel. Instagram may be blocking access or the URL is invalid.")
    except Exception as e:
        update.message.reply_text(f"❌ Error: {e}")
