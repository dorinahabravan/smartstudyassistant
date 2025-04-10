import os
import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")


def fetch_resources_google(query: str, max_results: int = 5):
    """
    Fetches learning resource links using Google Programmable Search Engine.
    Returns a list of URLs.
    """
    if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
        print("❌ Missing Google API Key or CSE ID.")
        return []

    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CSE_ID,
        "q": f"{query} tutorial",
        "num": max_results
    }

    response = requests.get("https://www.googleapis.com/customsearch/v1", params=params)

    if response.status_code != 200:
        print(f"❌ Google CSE Error: {response.json().get('error', {}).get('message', 'Unknown error')}")
        return []

    data = response.json()
    links = [item["link"] for item in data.get("items", []) if "link" in item]
    return links
