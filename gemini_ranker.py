import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name="gemini-2.0-flash-lite")


def pick_best_title(query: str, titles: list[str]) -> str:
    """
    Given a query and a list of video titles, return the single most relevant title.
    """
    if not titles:
        return ""

    prompt = (
        f"You are a helpful assistant. The user searched for:\n\n"
        f"'{query}'\n\n"
        f"Here are some YouTube video titles:\n"
        + "\n".join(f"- {title}" for title in titles) +
        "\n\nPick ONLY the single most relevant title with respect to the query from all the titles given. "
        "Return ONLY the title. No explanations."
    )

    try:
        response = model.generate_content(prompt)
        best_title = response.text.strip()
        return best_title.lstrip("-• ").strip()
    except Exception as e:
        print("Gemini API error:", e)
        return ""
