
import os
import pandas as pd

OUTPUT_FILE = "output/video_results.xlsx"

def save_results_to_excel(query, video_results, best_title):
    """
    Save the query, best Gemini title, and list of video results to Excel.
    Appends to the existing file with a blank row in between runs.
    """
    # Prepare metadata rows
    query_row = pd.DataFrame([{
        "Title": f"User Query: {query}",
        "URL": "",
        "Duration (min)": "",
        "Published Date": "",
        "Views": ""
    }])

    best_title_row = pd.DataFrame([{
        "Title": f"🏆 Gemini Best Title: {best_title}",
        "URL": "",
        "Duration (min)": "",
        "Published Date": "",
        "Views": ""
    }])

    # Prepare video data rows
    video_rows = pd.DataFrame([
        {
            "Title": video["title"],
            "URL": video["url"],
            "Duration (min)": video["duration_min"],
            "Published Date": video["published_at"],
            "Views": video["views"]
        }
        for video in video_results
    ])

    # Blank row for separation
    blank_row = pd.DataFrame([{
        "Title": "", "URL": "", "Duration (min)": "", "Published Date": "", "Views": ""
    }])

    # Final output
    final_df = pd.concat([query_row, best_title_row, video_rows, blank_row], ignore_index=True)

    # Append to file
    if os.path.exists(OUTPUT_FILE):
        existing_df = pd.read_excel(OUTPUT_FILE)
        combined_df = pd.concat([existing_df, final_df], ignore_index=True)
        combined_df.to_excel(OUTPUT_FILE, index=False)
    else:
        final_df.to_excel(OUTPUT_FILE, index=False)
