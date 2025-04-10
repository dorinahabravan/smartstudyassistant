import os
import requests
import json
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from backend.app.database import SessionLocal
from backend.app.models.init import Topics

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")


def fetch_google_results(query: str, num_results: int = 5):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CSE_ID,
        "q": f"{query} tutorial",
        "num": num_results
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if "items" not in data:
            print(f"❌ Google CSE Error: {data.get('error', {}).get('message', 'Unknown error')}")
            return []

        links = [item["link"] for item in data["items"][:num_results]]
        return links

    except Exception as e:
        print(f"❌ Exception occurred: {str(e)}")
        return []


def fetch_and_attach_resources():
    db: Session = SessionLocal()
    topics = db.query(Topics).all()

    for topic in topics:
        print(f"\n📘 Topic: {topic.title}")
        links = fetch_google_results(topic.title)
        if links:
            topic.resources = json.dumps(links)
            db.commit()
            print("✅ Resources attached.")
        else:
            print("⚠️ No results found.")

    db.close()
    print("\n🎉 All topics enriched using Google Programmable Search Engine!")


if __name__ == "__main__":
    fetch_and_attach_resources()
