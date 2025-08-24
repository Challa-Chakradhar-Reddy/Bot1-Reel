import instaloader
import os
import re

def fetchReel(url: str) -> str | None:
    try:
        match = re.search(r"(?:reel|p)/([A-Za-z0-9_-]+)", url)
        if not match:
            return None
        
        shortcode = match.group(1)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        download_dir = os.path.join(base_dir, "downloads")
        os.makedirs(download_dir, exist_ok=True)
        
        L = instaloader.Instaloader(dirname_pattern = download_dir,
                                    filename_pattern = "{shortcode}",
                                    download_videos = True,
                                    download_video_thumbnails = False,
                                    save_metadata = False,
                                    post_metadata_txt_pattern = "")
        
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        L.download_post(post, target=shortcode)
        
        for file in os.listdir(download_dir):
              if file.endswith(".mp4"): 
                videoPath = os.path.join(download_dir,file)
                return videoPath
        return None
            
    except Exception as e: 
        print(f"{e}")
        return None