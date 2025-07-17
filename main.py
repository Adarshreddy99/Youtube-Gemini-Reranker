# main.py

from youtube_search import search_youtube_videos
from gemini_ranker import pick_best_title
from helpers import save_results_to_excel

def process_query(query: str):
    """
    Processes a YouTube search query and returns only the best video (dict).
    
    Steps:
    - Search YouTube (20 results, filtered).
    - Rank using Gemini.
    - Save all results to Excel.
    
    Returns:
        best_video (dict): Full metadata of Gemini-picked best video.
        best_title (str): Title of best video.
    """
    if not query or not query.strip():
        raise ValueError("Empty query provided.")

    video_results = search_youtube_videos(query)
    if not video_results:
        return None, "No relevant videos found."

    titles = [video["title"] for video in video_results]
    best_title = pick_best_title(query, titles)

    # Find the best video from results
    best_video = next((v for v in video_results if v["title"].strip() == best_title), None)

    save_results_to_excel(query, video_results, best_title)

    return best_video, video_results


# Optional CLI usage
if __name__ == "__main__":
    user_query = input("🔍 Enter your YouTube search query: ").strip()
    try:
        best_video, best_title = process_query(user_query)

        if not best_video:
            print("❌ No relevant videos found.")
        else:
            print(f"\n🏆 Gemini's Pick: {best_title}")
            print(f"📺 Title: {best_video['title']}")
            print(f"🔗 URL: {best_video['url']}")
            print(f"🕒 Duration: {best_video['duration_min']} min")
            print(f"📅 Published: {best_video['published_at']}")
            print(f"👁️ Views: {best_video['views']}")

    except Exception as e:
        print(f"Error: {e}")
