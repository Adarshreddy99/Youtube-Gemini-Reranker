import os
import requests
import isodate
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()


YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"

def search_youtube_videos(query: str, max_results: int = 20):
    """
    Search YouTube videos by query.
    Filters:
    - Duration between 4 to 20 minutes
    - Published within last 14 days
    Returns up to `max_results` videos with metadata.
    """
    final_results = []
    next_page_token = None
    now = datetime.now(timezone.utc)
    cutoff_date = now - timedelta(days=14)

    while len(final_results) < max_results:
        # Step 1: Search
        search_params = {
            "key": YOUTUBE_API_KEY,
            "q": query,
            "type": "video",
            "part": "id",
            "maxResults": 50,
        }
        if next_page_token:
            search_params["pageToken"] = next_page_token

        search_resp = requests.get(SEARCH_URL, params=search_params).json()
        items = search_resp.get("items", [])
        video_ids = [item.get("id", {}).get("videoId") for item in items if item.get("id", {}).get("videoId")]
        next_page_token = search_resp.get("nextPageToken")

        if not video_ids:
            break

        # Step 2: Get details
        details_params = {
            "key": YOUTUBE_API_KEY,
            "id": ",".join(video_ids),
            "part": "snippet,contentDetails,statistics"
        }
        details_resp = requests.get(VIDEO_URL, params=details_params).json()

        for item in details_resp.get("items", []):
            try:
                duration = isodate.parse_duration(item["contentDetails"]["duration"])
                duration_minutes = int(duration.total_seconds() // 60)
                if not (4 <= duration_minutes <= 20):
                    continue

                published_at = item["snippet"]["publishedAt"]
                published_datetime = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
                if published_datetime < cutoff_date:
                    continue

                video_id = item.get("id")
                if not video_id:
                    continue

                final_results.append({
                    "title": item["snippet"]["title"],
                    "url": f"https://www.youtube.com/watch?v={video_id}",
                    "duration_min": duration_minutes,
                    "published_at": published_at,
                    "views": item["statistics"].get("viewCount", "0")
                })

                if len(final_results) >= max_results:
                    break
            except Exception as e:
                print(f"⚠️ Error processing video: {e}")
                # print(item)  # Debug if needed
                continue

        if not next_page_token:
            break

    return final_results

if __name__ == "__main__":
    query = input("Enter your YouTube search query: ")
    results = search_youtube_videos(query)

    if not results:
        print("❌ No relevant videos found.")
    else:
        print(f"\n✅ Found {len(results)} relevant videos:\n")
        for idx, video in enumerate(results, 1):
            print(f"{idx}. {video['title']}")
            print(f"   URL: {video['url']}")
            print(f"   Duration: {video['duration_min']} mins")
            print(f"   Published at: {video['published_at']}")
            print(f"   Views: {video['views']}")
            print("-" * 40)
