import instaloader
import os
import re
import time
import logging

# Setup logger
logger = logging.getLogger(__name__)

# Directory for downloads & session
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")
SESSION_FILE = os.path.join(BASE_DIR, "session-instaloader")

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def fetchReel(url: str) -> str | None:
    try:
        logger.info(f"🔗 Fetching reel from URL: {url}")

        # Extract shortcode from reel URL
        match = re.search(r"(?:reel|p|reels)/([A-Za-z0-9_-]+)", url)
        if not match:
            logger.warning("❌ No shortcode found in URL")
            return None
        shortcode = match.group(1)
        logger.info(f"✅ Extracted shortcode: {shortcode}")

        # Load credentials from environment
        username = os.getenv("INSTAGRAM_USER")
        password = os.getenv("INSTAGRAM_PASS")
        if not username or not password:
            logger.error("❌ Instagram credentials not found in environment variables")
            raise ValueError("Missing INSTAGRAM_USER or INSTAGRAM_PASS in environment")

        # Configure instaloader
        L = instaloader.Instaloader(
            dirname_pattern=DOWNLOAD_DIR,
            filename_pattern="{shortcode}",
            download_videos=True,
            download_video_thumbnails=False,
            save_metadata=False,
            post_metadata_txt_pattern=""
        )

        # Try to load session file (avoids relogin)
        if os.path.exists(SESSION_FILE):
            try:
                L.load_session_from_file(username, SESSION_FILE)
                logger.info("✅ Loaded Instagram session from file")
            except Exception as e:
                logger.warning(f"⚠️ Failed to load session, logging in again: {e}")
                L.login(username, password)
                L.save_session_to_file(SESSION_FILE)
        else:
            # First login
            logger.info("🔑 Logging into Instagram...")
            L.login(username, password)
            L.save_session_to_file(SESSION_FILE)
            logger.info("✅ Logged in and saved session")

        # Fetch and download post
        logger.info(f"📥 Downloading post with shortcode: {shortcode}")
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        L.download_post(post, target=shortcode)

        # Clean up and find latest mp4
        mp4_files = [f for f in os.listdir(DOWNLOAD_DIR) if f.endswith(".mp4")]
        if not mp4_files:
            logger.error("❌ No .mp4 files found after download")
            return None
        mp4_files.sort(key=lambda f: os.path.getmtime(os.path.join(DOWNLOAD_DIR, f)), reverse=True)
        video_path = os.path.join(DOWNLOAD_DIR, mp4_files[0])

        logger.info(f"✅ Download complete. Video saved at {video_path}")

        # Add safe delay (8 sec default)
        time.sleep(8)

        return video_path

    except Exception as e:
        logger.error(f"❌ Error fetching reel: {e}", exc_info=True)
        raise   # let the handler catch it
