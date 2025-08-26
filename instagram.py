import instaloader
import os
import re
import time

# Directory for downloads & session
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")
SESSION_FILE = os.path.join(BASE_DIR, "session-instaloader")

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def fetchReel(url: str) -> str | None:
    try:
        # Extract shortcode from reel URL
        match = re.search(r"(?:reel|p)/([A-Za-z0-9_-]+)", url)
        if not match:
            return None
        shortcode = match.group(1)

        # Load credentials from environment
        username = os.getenv("INSTAGRAM_USER")
        password = os.getenv("INSTAGRAM_PASS")

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
                print("✅ Loaded Instagram session")
            except Exception as e:
                print(f"⚠️ Failed to load session: {e}")
                L.login(username, password)
                L.save_session_to_file(SESSION_FILE)
        else:
            # First login
            L.login(username, password)
            L.save_session_to_file(SESSION_FILE)

        # Fetch and download post
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        L.download_post(post, target=shortcode)

        # Clean up and find latest mp4
        mp4_files = [f for f in os.listdir(DOWNLOAD_DIR) if f.endswith(".mp4")]
        if not mp4_files:
            return None
        mp4_files.sort(key=lambda f: os.path.getmtime(os.path.join(DOWNLOAD_DIR, f)), reverse=True)
        video_path = os.path.join(DOWNLOAD_DIR, mp4_files[0])

        # Add safe delay (8 sec default)
        time.sleep(8)

        return video_path

    except Exception as e:
        print(f"❌ Error: {e}")
        return None
