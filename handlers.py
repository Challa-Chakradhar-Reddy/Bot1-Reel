from telegram import Update
from telegram.ext import CallbackContext
from instagram import fetchReel
from delete import deleteDownloads
import logging

logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("👋 Send me an Instagram Reel URL and I’ll fetch the video for you!")

def handleMessage(update: Update, context: CallbackContext) -> None:
    url = update.message.text.strip()

    # Basic validation (avoid crashes if someone sends random text)
    if not url.startswith("http"):
        update.message.reply_text("⚠️ Please send a valid Instagram Reel URL.")
        return

    update.message.reply_text("⏳ Fetching reel... This may take a few seconds...")

    try:
        videoPath = fetchReel(url)

        if videoPath:
            with open(videoPath, "rb") as video:
                update.message.reply_video(
                    video=video,
                    caption="Here’s your reel 🎥"
                )
            # ✅ Cleanup after sending
            deleteDownloads()
        else:
            update.message.reply_text(
                "⚠️ Couldn’t fetch this reel. Instagram may be blocking access or the URL is invalid."
            )

    except Exception as e:
        logger.error(f"Error fetching reel: {e}", exc_info=True)
        update.message.reply_text("❌ An error occurred while fetching the reel. Please try again later.")
